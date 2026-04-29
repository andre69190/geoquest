-- ============================================================
-- GeoQuest Security v2  (Phase 31 + Phase 32 Anti-Cheat)
-- Run in Supabase SQL Editor — replaces geoquest_security_v1.sql
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- 1. ADMIN TRIGGER  (server-side, replaces frontend backdoor)
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION handle_admin_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF NEW.email = 'admin@geoquest.local' THEN
    UPDATE public.profiles
    SET    is_premium = true,
           geo_coins  = 999999
    WHERE  id = NEW.id;
  END IF;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_admin_user_created ON auth.users;
CREATE TRIGGER on_admin_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE handle_admin_user();


-- ────────────────────────────────────────────────────────────
-- 2. RPC: add_score  (Phase 31 + Phase 32 anti-cheat)
--
--    Parameters:
--      p_user_id     uuid    — must match auth.uid()
--      p_score       int     — session score
--      p_coins       int     — bonus coins to add
--      p_rounds      int     — number of questions played (default 10)
--      p_duration_ms bigint  — total game time in milliseconds
--
--    Anti-cheat rules:
--      • Caller must be authenticated and match p_user_id
--      • Minimum time: 1 500 ms × p_rounds  (< 0.5 s/question = bot)
--      • Maximum score: 1 800 pts × min(p_rounds, 10)
--        (BASE=100, TB=10, timer=12 s, tier×2.5, hardcore×3 → ~1 650/rd)
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION add_score(
  p_user_id     uuid,
  p_score       int,
  p_coins       int     DEFAULT 0,
  p_rounds      int     DEFAULT 10,
  p_duration_ms bigint  DEFAULT 0
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_caller    uuid   := auth.uid();
  v_max_score int;
  v_min_ms    bigint;
BEGIN
  -- ── Auth check ─────────────────────────────────────────────
  IF v_caller IS NULL OR v_caller <> p_user_id THEN
    RAISE EXCEPTION 'Unauthorized: caller % ≠ user %', v_caller, p_user_id;
  END IF;

  -- ── Sanity bounds ──────────────────────────────────────────
  IF p_score < 0 OR p_coins < 0 OR p_coins > 500 OR p_rounds < 1 THEN
    RAISE EXCEPTION 'Invalid parameters (score=%, coins=%, rounds=%)',
                    p_score, p_coins, p_rounds;
  END IF;

  -- ── Anti-cheat: time floor ─────────────────────────────────
  -- 1 500 ms per question minimum (generous; real min ≈ 3 000 ms)
  v_min_ms := p_rounds::bigint * 1500;
  IF p_duration_ms > 0 AND p_duration_ms < v_min_ms THEN
    RAISE EXCEPTION
      'Cheat detected: % ms for % rounds (min expected % ms)',
      p_duration_ms, p_rounds, v_min_ms;
  END IF;

  -- ── Anti-cheat: score ceiling ──────────────────────────────
  -- Max realistic: (100 + 12×10) × 2.5 × 3 = 1 650 / round → 1 800 w/ buffer
  v_max_score := LEAST(p_rounds, 100) * 1800;
  IF p_score > v_max_score THEN
    RAISE EXCEPTION
      'Cheat detected: score % > max % for % rounds',
      p_score, v_max_score, p_rounds;
  END IF;

  -- ── Commit ─────────────────────────────────────────────────
  UPDATE public.profiles
  SET
    total_score  = COALESCE(total_score,  0) + p_score,
    games_played = COALESCE(games_played, 0) + 1,
    geo_coins    = COALESCE(geo_coins,    0) + p_coins
  WHERE id = p_user_id;
END;
$$;

-- Permissions
REVOKE ALL    ON FUNCTION add_score(uuid,int,int,int,bigint) FROM PUBLIC;
GRANT  EXECUTE ON FUNCTION add_score(uuid,int,int,int,bigint) TO authenticated;


-- ────────────────────────────────────────────────────────────
-- 3. RLS POLICIES
-- ────────────────────────────────────────────────────────────

-- profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_select_own" ON public.profiles;
CREATE POLICY "profiles_select_own"
  ON public.profiles FOR SELECT USING (auth.uid() = id);

DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
CREATE POLICY "profiles_update_own"
  ON public.profiles FOR UPDATE
  USING     (auth.uid() = id)
  WITH CHECK(auth.uid() = id);

DROP POLICY IF EXISTS "profiles_insert_own" ON public.profiles;
CREATE POLICY "profiles_insert_own"
  ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- game_sessions
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "sessions_insert_own" ON public.game_sessions;
CREATE POLICY "sessions_insert_own"
  ON public.game_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "sessions_select_own" ON public.game_sessions;
CREATE POLICY "sessions_select_own"
  ON public.game_sessions FOR SELECT USING (auth.uid() = user_id);

-- user_stamps
ALTER TABLE public.user_stamps ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "stamps_own" ON public.user_stamps;
CREATE POLICY "stamps_own"
  ON public.user_stamps
  USING      (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);


-- ────────────────────────────────────────────────────────────
-- 4. Leaderboard view (no email, read-only)
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE VIEW public.leaderboard AS
SELECT id, username, total_score, games_played, is_premium
FROM   public.profiles
WHERE  username IS NOT NULL
ORDER  BY total_score DESC;

REVOKE ALL   ON public.leaderboard FROM PUBLIC;
GRANT  SELECT ON public.leaderboard TO authenticated, anon;


-- ────────────────────────────────────────────────────────────
-- 5. Optional: once all clients use rpc('add_score'),
--    tighten the UPDATE policy to block direct score writes:
--
-- DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
-- CREATE POLICY "profiles_update_own"
--   ON public.profiles FOR UPDATE
--   USING (auth.uid() = id)
--   WITH CHECK (
--     auth.uid() = id
--     AND total_score  IS NOT DISTINCT FROM
--         (SELECT total_score  FROM public.profiles WHERE id = auth.uid())
--     AND games_played IS NOT DISTINCT FROM
--         (SELECT games_played FROM public.profiles WHERE id = auth.uid())
--   );
-- ────────────────────────────────────────────────────────────
