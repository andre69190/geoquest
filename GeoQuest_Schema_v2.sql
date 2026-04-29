-- ============================================================
-- GeoQuest – Supabase Schema v2
-- Covers Phases 3-13: Passport, Mastery, League, Payment,
--                     Daily Challenges, Admin Bypass
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- 0. EXTENSIONS
-- ────────────────────────────────────────────────────────────
create extension if not exists "uuid-ossp";
create extension if not exists pgcrypto;


-- ────────────────────────────────────────────────────────────
-- 1. PROFILES  (one row per auth.users row)
-- ────────────────────────────────────────────────────────────
create table if not exists public.profiles (
  id               uuid primary key references auth.users(id) on delete cascade,
  username         text unique,
  avatar_url       text,

  -- scoring
  total_score      bigint  not null default 0,
  best_streak      int     not null default 0,

  -- currency / premium
  geo_coins        int     not null default 0,
  is_premium       boolean not null default false,
  premium_until    timestamptz,
  payment_method   text,                   -- 'stripe' | 'paypal' | 'mock'
  payment_ref      text,                   -- external transaction id

  -- league system (Phase 7)
  current_league   text    not null default 'Bronze',  -- Bronze/Silver/Gold/Platinum/Diamond
  league_points    int     not null default 0,
  season_number    int     not null default 1,

  -- admin flag (Phase 9)
  is_admin         boolean not null default false,

  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

-- keep updated_at fresh
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists profiles_updated_at on public.profiles;
create trigger profiles_updated_at
  before update on public.profiles
  for each row execute procedure public.touch_updated_at();


-- ────────────────────────────────────────────────────────────
-- 2. AUTO-CREATE PROFILE ON SIGN-UP
-- ────────────────────────────────────────────────────────────
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer as $$
begin
  insert into public.profiles (id, username)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1))
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();


-- ────────────────────────────────────────────────────────────
-- 3. PASSPORT STAMPS  (Phase 4)
-- ────────────────────────────────────────────────────────────
-- One row per (user, country_code).
-- mastery_level: 0=visited, 1=Bronze, 2=Silver, 3=Gold
create table if not exists public.passport_stamps (
  id             uuid primary key default uuid_generate_v4(),
  user_id        uuid not null references public.profiles(id) on delete cascade,
  country_code   char(2) not null,            -- ISO 3166-1 alpha-2, lower-case
  visits         int  not null default 1,
  perfect_rounds int  not null default 0,
  mastery_level  smallint not null default 0, -- 0-3
  first_seen_at  timestamptz not null default now(),
  updated_at     timestamptz not null default now(),
  unique (user_id, country_code)
);

drop trigger if exists stamps_updated_at on public.passport_stamps;
create trigger stamps_updated_at
  before update on public.passport_stamps
  for each row execute procedure public.touch_updated_at();

-- Helper function: upsert a stamp and recompute mastery
create or replace function public.upsert_stamp(
  p_user_id        uuid,
  p_country_code   char(2),
  p_perfect        boolean default false
)
returns public.passport_stamps language plpgsql security definer as $$
declare
  rec public.passport_stamps;
  new_mastery smallint;
begin
  insert into public.passport_stamps (user_id, country_code, visits, perfect_rounds)
  values (p_user_id, p_country_code, 1, case when p_perfect then 1 else 0 end)
  on conflict (user_id, country_code) do update
    set visits         = passport_stamps.visits + 1,
        perfect_rounds = passport_stamps.perfect_rounds + (case when p_perfect then 1 else 0 end)
  returning * into rec;

  -- mastery thresholds: Bronze≥3v, Silver≥10v+3p, Gold≥25v+10p
  new_mastery := 0;
  if rec.visits >= 3 then new_mastery := 1; end if;
  if rec.visits >= 10 and rec.perfect_rounds >= 3 then new_mastery := 2; end if;
  if rec.visits >= 25 and rec.perfect_rounds >= 10 then new_mastery := 3; end if;

  if new_mastery <> rec.mastery_level then
    update public.passport_stamps
    set mastery_level = new_mastery
    where id = rec.id
    returning * into rec;
  end if;

  return rec;
end;
$$;


-- ────────────────────────────────────────────────────────────
-- 4. SCORES / GAME SESSIONS
-- ────────────────────────────────────────────────────────────
create table if not exists public.game_sessions (
  id          uuid primary key default uuid_generate_v4(),
  user_id     uuid references public.profiles(id) on delete set null,
  mode        text not null,          -- 'flags','capitals','rivers', etc.
  difficulty  text not null default 'casual',  -- 'casual'|'hardcore'
  score       int  not null default 0,
  correct     int  not null default 0,
  rounds      int  not null default 0,
  streak_best int  not null default 0,
  duration_s  int,                    -- seconds taken
  played_at   timestamptz not null default now()
);

create index if not exists idx_sessions_user on public.game_sessions(user_id);
create index if not exists idx_sessions_played on public.game_sessions(played_at desc);


-- ────────────────────────────────────────────────────────────
-- 5. LEAGUE TABLE  (Phase 7)
-- ────────────────────────────────────────────────────────────
-- View: top 30 players ordered by league_points this season,
--       promotion zone (top 5) and relegation zone (bottom 5).
create or replace view public.league_leaderboard as
select
  p.id,
  p.username,
  p.avatar_url,
  p.current_league,
  p.league_points,
  p.season_number,
  row_number() over (
    partition by p.season_number
    order by p.league_points desc
  ) as rank
from public.profiles p
where p.season_number = (select max(season_number) from public.profiles);


-- Stored proc: end-of-season promotion / relegation
-- Promote top 5 → next league, relegate bottom 5 → previous league.
create or replace function public.process_season_end()
returns void language plpgsql security definer as $$
declare
  league_order text[] := array['Bronze','Silver','Gold','Platinum','Diamond'];
  cur_season   int;
begin
  cur_season := (select max(season_number) from public.profiles);

  -- promote top 5
  with ranked as (
    select id, current_league,
           row_number() over (order by league_points desc) as rn
    from public.profiles
    where season_number = cur_season
  )
  update public.profiles p
  set current_league = league_order[
    least(array_position(league_order, r.current_league) + 1, array_length(league_order,1))
  ],
  league_points  = 0,
  season_number  = cur_season + 1
  from ranked r
  where p.id = r.id and r.rn <= 5;

  -- relegate bottom 5 (excluding already-updated rows)
  with ranked as (
    select id, current_league,
           row_number() over (order by league_points asc) as rn
    from public.profiles
    where season_number = cur_season   -- still old season
  )
  update public.profiles p
  set current_league = league_order[
    greatest(array_position(league_order, r.current_league) - 1, 1)
  ],
  league_points  = 0,
  season_number  = cur_season + 1
  from ranked r
  where p.id = r.id and r.rn <= 5;

  -- everyone else: advance season, reset points
  update public.profiles
  set league_points = 0,
      season_number = cur_season + 1
  where season_number = cur_season;
end;
$$;


-- ────────────────────────────────────────────────────────────
-- 6. DAILY CHALLENGES  (Phase 7)
-- ────────────────────────────────────────────────────────────
create table if not exists public.daily_challenges (
  id            uuid primary key default uuid_generate_v4(),
  challenge_date date not null unique,
  mode          text not null,
  seed          int  not null,        -- RNG seed for reproducible questions
  bonus_coins   int  not null default 50,
  created_at    timestamptz not null default now()
);

-- Track which users completed which daily challenges
create table if not exists public.daily_completions (
  id            uuid primary key default uuid_generate_v4(),
  user_id       uuid not null references public.profiles(id) on delete cascade,
  challenge_id  uuid not null references public.daily_challenges(id) on delete cascade,
  score         int  not null default 0,
  completed_at  timestamptz not null default now(),
  unique (user_id, challenge_id)
);

create index if not exists idx_daily_comp_user on public.daily_completions(user_id);


-- ────────────────────────────────────────────────────────────
-- 7. COIN TRANSACTIONS  (Phase 9)
-- ────────────────────────────────────────────────────────────
create table if not exists public.coin_transactions (
  id          uuid primary key default uuid_generate_v4(),
  user_id     uuid not null references public.profiles(id) on delete cascade,
  delta       int  not null,          -- positive = credit, negative = debit
  reason      text not null,          -- 'game_reward'|'purchase'|'admin_grant'|'daily_bonus'
  ref_id      uuid,                   -- optional: game_session id or purchase id
  created_at  timestamptz not null default now()
);

create index if not exists idx_coins_user on public.coin_transactions(user_id);

-- Trigger: keep profiles.geo_coins in sync automatically
create or replace function public.sync_coin_balance()
returns trigger language plpgsql security definer as $$
begin
  update public.profiles
  set geo_coins = geo_coins + new.delta
  where id = new.user_id;
  return new;
end;
$$;

drop trigger if exists after_coin_tx on public.coin_transactions;
create trigger after_coin_tx
  after insert on public.coin_transactions
  for each row execute procedure public.sync_coin_balance();


-- ────────────────────────────────────────────────────────────
-- 8. PURCHASES  (Phase 9 – mock payment)
-- ────────────────────────────────────────────────────────────
create table if not exists public.purchases (
  id             uuid primary key default uuid_generate_v4(),
  user_id        uuid not null references public.profiles(id) on delete cascade,
  product        text not null,       -- 'premium_monthly'|'premium_yearly'|'coins_500'| etc.
  amount_cents   int  not null,
  currency       char(3) not null default 'EUR',
  provider       text not null default 'mock', -- 'stripe'|'paypal'|'mock'
  provider_ref   text,
  status         text not null default 'pending', -- 'pending'|'completed'|'refunded'
  created_at     timestamptz not null default now(),
  completed_at   timestamptz
);

create index if not exists idx_purchases_user on public.purchases(user_id);


-- ────────────────────────────────────────────────────────────
-- 9. ROW-LEVEL SECURITY
-- ────────────────────────────────────────────────────────────

-- profiles
alter table public.profiles enable row level security;

create policy "profiles: users read own row"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles: users update own row"
  on public.profiles for update
  using (auth.uid() = id);

-- leaderboard is public read (uses a view, so policies on profiles apply)
-- Additional policy so anyone can read profiles for leaderboard display:
create policy "profiles: public read username + points"
  on public.profiles for select
  using (true);   -- restrict columns via a separate secure view if needed


-- passport_stamps
alter table public.passport_stamps enable row level security;

create policy "stamps: owner full access"
  on public.passport_stamps for all
  using (auth.uid() = user_id);


-- game_sessions
alter table public.game_sessions enable row level security;

create policy "sessions: owner full access"
  on public.game_sessions for all
  using (auth.uid() = user_id);


-- daily_challenges (public read, admin write)
alter table public.daily_challenges enable row level security;

create policy "daily: public read"
  on public.daily_challenges for select using (true);

create policy "daily: admin write"
  on public.daily_challenges for all
  using (exists (
    select 1 from public.profiles
    where id = auth.uid() and is_admin = true
  ));


-- daily_completions
alter table public.daily_completions enable row level security;

create policy "daily_comp: owner full access"
  on public.daily_completions for all
  using (auth.uid() = user_id);


-- coin_transactions
alter table public.coin_transactions enable row level security;

create policy "coins: owner read"
  on public.coin_transactions for select
  using (auth.uid() = user_id);

create policy "coins: service insert"
  on public.coin_transactions for insert
  with check (auth.uid() = user_id);


-- purchases
alter table public.purchases enable row level security;

create policy "purchases: owner read"
  on public.purchases for select
  using (auth.uid() = user_id);

create policy "purchases: owner insert"
  on public.purchases for insert
  with check (auth.uid() = user_id);


-- ────────────────────────────────────────────────────────────
-- 10. ADMIN BYPASS HELPER  (Phase 9)
-- ────────────────────────────────────────────────────────────
-- Call this from a Supabase Edge Function or the app's
-- server-side admin route to elevate an account.
create or replace function public.admin_grant_premium(
  p_user_id   uuid,
  p_coins     int default 999999,
  p_months    int default 12
)
returns void language plpgsql security definer as $$
begin
  update public.profiles
  set is_premium    = true,
      premium_until = now() + (p_months || ' months')::interval,
      geo_coins     = p_coins,
      is_admin      = true
  where id = p_user_id;
end;
$$;


-- ────────────────────────────────────────────────────────────
-- 11. USEFUL INDEXES
-- ────────────────────────────────────────────────────────────
create index if not exists idx_profiles_league
  on public.profiles(season_number, league_points desc);

create index if not exists idx_stamps_user_cc
  on public.passport_stamps(user_id, country_code);

create index if not exists idx_stamps_mastery
  on public.passport_stamps(mastery_level);


-- ────────────────────────────────────────────────────────────
-- 12. SEED: first daily challenge
-- ────────────────────────────────────────────────────────────
insert into public.daily_challenges (challenge_date, mode, seed, bonus_coins)
values (current_date, 'flags', floor(random()*100000)::int, 100)
on conflict (challenge_date) do nothing;


-- Done ✓
-- Run this entire file in your Supabase SQL Editor or via:
--   supabase db push
-- Make sure to set SUPABASE_URL and SUPABASE_ANON_KEY in your app.
