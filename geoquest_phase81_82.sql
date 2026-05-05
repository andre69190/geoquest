-- ============================================================
-- GeoQuest — Phase 81 + 82 SQL Migration
-- Run this once in the Supabase SQL Editor
-- ============================================================

-- ============================================================
-- PHASE 81: Titel-System
-- ============================================================

-- 1. Add current_title column to profiles
ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS current_title TEXT NOT NULL DEFAULT 'Erkunder';

-- ============================================================
-- PHASE 82: Cross-Device Sync
-- ============================================================

-- 2. Add stats columns to profiles
ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS stats_history   JSONB NOT NULL DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS stats_mastery   JSONB NOT NULL DEFAULT '{}'::jsonb,
  ADD COLUMN IF NOT EXISTS last_daily_date TEXT  NOT NULL DEFAULT '';

-- ============================================================
-- PHASE 81: Wöchentliches Leaderboard (auto-reset jeden Montag)
--
-- Die View filtert game_sessions auf die AKTUELLE Kalenderwoche
-- via date_trunc('week', NOW()).
-- Jeden Montag um 00:00 UTC startet die Rangliste automatisch
-- bei 0 für alle — kein Cron-Job nötig.
-- ============================================================

-- Drop old view if it exists (may have different column set)
DROP VIEW IF EXISTS leaderboard_weekly;

-- Recreate with weekly filter + current_title
CREATE VIEW leaderboard_weekly AS
SELECT
  gs.user_id,
  p.username,
  p.current_title,
  gs.mode,
  SUM(gs.score)                                                          AS weekly_score,
  MAX(gs.score)                                                          AS best_score,
  COUNT(*)                                                               AS games_played,
  RANK() OVER (
    PARTITION BY gs.mode
    ORDER BY SUM(gs.score) DESC
  )                                                                      AS rank
FROM game_sessions gs
JOIN profiles p ON p.id = gs.user_id
WHERE
  gs.created_at >= date_trunc('week', NOW())          -- current Monday 00:00 UTC
  AND gs.created_at <  date_trunc('week', NOW()) + INTERVAL '7 days'    -- next Monday
  AND p.username IS NOT NULL
  AND p.username <> ''
GROUP BY gs.user_id, p.username, p.current_title, gs.mode;

-- Grant read access to authenticated users
GRANT SELECT ON leaderboard_weekly TO authenticated;

-- ============================================================
-- Optional: index to speed up the weekly window scan
-- (create once; safe to re-run)
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_game_sessions_created_at
  ON game_sessions (created_at);

CREATE INDEX IF NOT EXISTS idx_game_sessions_mode
  ON game_sessions (mode, created_at);
