-- ============================================================
-- GeoQuest Security Hardening SQL  (Phase 31)
-- Run this in the Supabase SQL Editor
-- ============================================================


-- ────────────────────────────────────────────────────────────
-- 1. ADMIN TRIGGER
--    Replaces frontend admin@geoquest.local backdoor.
--    Runs server-side on INSERT into auth.users.
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION handle_admin_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER          -- runs as DB owner, not client
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
-- 2. RPC: add_score
--    Called by JS instead of direct profiles.update().
--    Validates caller is who they claim to be (auth.uid()).
--    Enforces sane score bounds (anti-cheat).
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION add_score(
  p_user_id uuid,
  p_score   int,
  p_coins   int DEFAULT 0
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_caller uuid := auth.uid();
BEGIN
  -- Caller must be authenticated and match the claimed user_id
  IF v_caller IS NULL OR v_caller <> p_user_id THEN
    RAISE EXCEPTION 'Unauthorized: caller % tried to update user %', v_caller, p_user_id;
  END IF;

  -- Sanity-check score bounds (one round max ≈ 500 pts × 3× HC × streak)
  IF p_score < 0 OR p_score > 50000 THEN
    RAISE EXCEPTION 'Score % out of allowed range', p_score;
  END IF;

  IF p_coins < 0 OR p_coins > 500 THEN
    RAISE EXCEPTION 'Coins % out of allowed range', p_coins;
  END IF;

  UPDATE public.profiles
  SET
    total_score  = COALESCE(total_score,  0) + p_score,
    games_played = COALESCE(games_played, 0) + 1,
    geo_coins    = COALESCE(geo_coins,    0) + p_coins
  WHERE id = p_user_id;
END;
$$;

-- Allow authenticated users to call it
REVOKE ALL ON FUNCTION add_score(uuid, int, int) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION add_score(uuid, int, int) TO authenticated;


-- ────────────────────────────────────────────────────────────
-- 3. RLS POLICIES — profiles table
--    Users may only read/update their own row.
--    Direct UPDATE of total_score / geo_coins from client
--    is still possible until you add the restrictive policy
--    below — uncomment when ready to enforce RPC-only writes.
-- ────────────────────────────────────────────────────────────

-- Enable RLS (idempotent)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- SELECT: own row only
DROP POLICY IF EXISTS "profiles_select_own" ON public.profiles;
CREATE POLICY "profiles_select_own"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

-- UPDATE: own row only
DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
CREATE POLICY "profiles_update_own"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- INSERT: only via handle_new_user trigger (SECURITY DEFINER)
DROP POLICY IF EXISTS "profiles_insert_own" ON public.profiles;
CREATE POLICY "profiles_insert_own"
  ON public.profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- ── Optional: once you switch entirely to rpc('add_score'),
--    uncomment to block direct column writes to score fields:
--
-- DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;
-- CREATE POLICY "profiles_update_own"
--   ON public.profiles FOR UPDATE
--   USING (auth.uid() = id)
--   WITH CHECK (
--     auth.uid() = id
--     -- only allow safe fields; score fields must go via RPC
--     AND (total_score  IS NOT DISTINCT FROM (SELECT total_score  FROM public.profiles WHERE id = auth.uid()))
--     AND (games_played IS NOT DISTINCT FROM (SELECT games_played FROM public.profiles WHERE id = auth.uid()))
--   );


-- ────────────────────────────────────────────────────────────
-- 4. RLS — game_sessions table
-- ────────────────────────────────────────────────────────────

ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "sessions_insert_own" ON public.game_sessions;
CREATE POLICY "sessions_insert_own"
  ON public.game_sessions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "sessions_select_own" ON public.game_sessions;
CREATE POLICY "sessions_select_own"
  ON public.game_sessions FOR SELECT
  USING (auth.uid() = user_id);


-- ────────────────────────────────────────────────────────────
-- 5. RLS — user_stamps table
-- ────────────────────────────────────────────────────────────

ALTER TABLE public.user_stamps ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "stamps_own" ON public.user_stamps;
CREATE POLICY "stamps_own"
  ON public.user_stamps
  USING      (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);


-- ────────────────────────────────────────────────────────────
-- 6. Leaderboard view — exposes only safe columns
--    (no email, no internal fields)
-- ────────────────────────────────────────────────────────────

CREATE OR REPLACE VIEW public.leaderboard AS
SELECT
  id,
  username,
  total_score,
  games_played,
  is_premium
FROM public.profiles
WHERE username IS NOT NULL
ORDER BY total_score DESC;

-- Read-only for authenticated users
REVOKE ALL ON public.leaderboard FROM PUBLIC;
GRANT SELECT ON public.leaderboard TO authenticated, anon;
