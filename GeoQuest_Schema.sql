-- ════════════════════════════════════════════════════════════
-- GeoQuest – Supabase Schema
-- Ausführen in: Supabase Dashboard → SQL Editor
-- ════════════════════════════════════════════════════════════

-- Profil (erweitert auth.users)
create table if not exists public.profiles (
  id           uuid references auth.users(id) on delete cascade primary key,
  username     text unique,
  total_score  bigint  default 0,
  games_played int     default 0,
  created_at   timestamptz default now()
);
alter table public.profiles enable row level security;
create policy "Eigenes Profil lesen"  on public.profiles for select using (auth.uid() = id);
create policy "Eigenes Profil ändern" on public.profiles for update using (auth.uid() = id);
create policy "Profil anlegen"        on public.profiles for insert with check (auth.uid() = id);

-- Profil automatisch anlegen wenn User sich registriert
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer as $$
begin
  insert into public.profiles(id) values(new.id);
  return new;
end;
$$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- ── Spielsitzungen ────────────────────────────────────────
create table if not exists public.game_sessions (
  id           uuid    default gen_random_uuid() primary key,
  user_id      uuid    references auth.users(id) on delete cascade,
  mode         text    not null,          -- 'city' | 'flag'
  score        int     not null,
  best_streak  int     not null default 0,
  rounds       int     not null default 10,
  accuracy     numeric(5,2),
  pop_filter   int     default 0,
  username     text,                      -- denormalisiert für schnelle Leaderboard-Queries
  created_at   timestamptz default now()
);
alter table public.game_sessions enable row level security;
create policy "Session anlegen"     on public.game_sessions for insert with check (auth.uid() = user_id);
create policy "Eigene Sessions"     on public.game_sessions for select using (auth.uid() = user_id);
create policy "Leaderboard lesen"   on public.game_sessions for select using (true);

-- ── Reisepass-Stempel ────────────────────────────────────
create table if not exists public.stamps (
  id            serial primary key,
  country_code  char(2)  unique not null,
  country_name  text     not null,
  continent     text     not null,
  rarity        text     default 'common'  -- common | rare | epic | legendary
);
alter table public.stamps enable row level security;
create policy "Stempel lesen" on public.stamps for select using (true);

create table if not exists public.user_stamps (
  user_id      uuid references auth.users(id) on delete cascade,
  stamp_id     int  references public.stamps(id),
  collected_at timestamptz default now(),
  primary key (user_id, stamp_id)
);
alter table public.user_stamps enable row level security;
create policy "Eigene Stempel"     on public.user_stamps for select using (auth.uid() = user_id);
create policy "Stempel sammeln"    on public.user_stamps for insert with check (auth.uid() = user_id);

-- ── Leaderboard View (Top 20 pro Modus, letzte 7 Tage) ────
create or replace view public.leaderboard_weekly as
  select
    user_id,
    coalesce(p.username, 'Anonymous') as username,
    mode,
    max(score)                        as best_score,
    max(best_streak)                  as best_streak,
    count(*)::int                     as games_played,
    rank() over (partition by mode order by max(score) desc) as rank
  from public.game_sessions gs
  left join public.profiles p on p.id = gs.user_id
  where gs.created_at > now() - interval '7 days'
  group by gs.user_id, p.username, gs.mode;

-- ── Stempel-Seed (Top-Länder nach Seltenheit) ─────────────
insert into public.stamps (country_code, country_name, continent, rarity) values
  ('jp','Japan','Asia','rare'),
  ('us','United States','North America','common'),
  ('de','Germany','Europe','common'),
  ('br','Brazil','South America','common'),
  ('cn','China','Asia','common'),
  ('in','India','Asia','common'),
  ('gb','United Kingdom','Europe','common'),
  ('fr','France','Europe','common'),
  ('au','Australia','Oceania','rare'),
  ('ng','Nigeria','Africa','common'),
  ('za','South Africa','Africa','rare'),
  ('eg','Egypt','Africa','common'),
  ('ru','Russia','Europe','common'),
  ('tr','Turkey','Europe','common'),
  ('kr','South Korea','Asia','rare'),
  ('mx','Mexico','North America','common'),
  ('ar','Argentina','South America','common'),
  ('id','Indonesia','Asia','common'),
  ('pk','Pakistan','Asia','common'),
  ('bd','Bangladesh','Asia','common'),
  ('nz','New Zealand','Oceania','epic'),
  ('sg','Singapore','Asia','epic'),
  ('ch','Switzerland','Europe','rare'),
  ('no','Norway','Europe','rare'),
  ('is','Iceland','Europe','legendary')
on conflict do nothing;
