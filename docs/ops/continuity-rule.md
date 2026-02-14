# Continuity Rule (Auto Pivot)

## Objective
When a project is blocked or paused, immediately switch to at least 2 alternative monetizable tracks.

## Trigger Conditions
A project is considered stalled if any of these happen:
1. No merged progress for 3 consecutive days.
2. Build/test blocked by external dependency for >24h.
3. No sponsor/integration lead response for 7 days.

## Auto-Pivot Actions
1. Freeze current track and log blocker in `docs/ops/blockers.md`.
2. Activate next 2 tracks from `docs/pipeline/fallback-queue.csv`.
3. Deliver one visible output per active track within 48h:
   - code commit, or
   - release/demo, or
   - sponsor-facing artifact.
4. Post progress note in repo README/weekly update.

## Priority Order
- Keep at most 2 active tracks at a time.
- Prefer tracks with:
  1. fastest path to demo,
  2. highest sponsor conversion,
  3. reusable assets from existing code.

## KPI Guardrail
- Minimum weekly output:
  - 2 commits across active tracks
  - 1 sponsor-facing update
  - 10 outreach messages
