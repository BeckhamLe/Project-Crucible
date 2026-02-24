# Crucible Handoff

Write the HANDOFF.md for the next agent session. Run this before context clears. ~1 minute.

## Steps

1. **Read current state** from these files (they are your source of truth):
   - `docs/CRUCIBLE.md` — active phase, agent assignments
   - `docs/AGENT.md` — gotchas, conventions, decisions
   - `findings/hypotheses.md` — which hypotheses are tested/untested
   - `findings/log.md` — latest run results (read the LAST entry only)

2. **Write `HANDOFF.md`** at the project root. Replace the entire file with this structure:

   ```markdown
   # Project Crucible — Handoff

   > Next agent: read this first, then follow the reading order below.

   ## Current State (updated: YYYY-MM-DD)
   - **Phase**: [PoC / Full Experiment / Analysis / Write-Up]
   - **Last completed**: [one line — what just happened]
   - **Next task**: [one specific action the next agent should do]
   - **Blockers**: [any open questions or issues, or "None"]
   - **Open PRs**: [list any unmerged PRs with URLs]

   ## Read These Files (in order)
   1. `docs/CRUCIBLE.md` — active state, agent assignments
   2. `docs/AGENT.md` — gotchas, conventions, anti-patterns, decisions log
   3. `findings/hypotheses.md` — what's been tested, what's queued
   4. `findings/log.md` — read only the latest entry unless you need full history

   ## What the Next Agent Should Do
   [2-5 bullet points with specific actions. Include which files to modify, what config to create, what to run. Be concrete enough that the agent can start immediately without asking questions.]

   ## What NOT to Do
   [List anything the next agent should avoid — failed approaches, known dead ends, things that look tempting but don't work]

   ## Session History (one line per session)
   - Session N: [brief summary of what happened]
   ```

3. **Preserve the Session History section** — read the existing HANDOFF.md first (if it exists) and carry forward all previous session entries. Add the current session as a new line.

4. **Commit and push** HANDOFF.md to the current branch or main (whichever is checked out). Use commit message: "Update handoff for next session"

5. **Output**: "Handoff written. Next agent should read HANDOFF.md first."

## Important
- This file gets REPLACED each time, not appended. Only Session History accumulates.
- The "Next task" must be specific. Not "continue working" — say exactly what to build/run/fix.
- The "What NOT to Do" section prevents the next agent from repeating mistakes. Fill it in.
- Keep it under 80 lines. The next agent's context window is precious.
