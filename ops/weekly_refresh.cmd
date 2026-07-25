@echo off
rem ModelWire weekly refresh. Registered in Task Scheduler as "ModelWire Weekly Refresh" (Mon 10:17).
rem FIX 2026-07-07: the previous version hardcoded a non-ASCII (Korean) path in `cd /d`. Under the
rem Task Scheduler codepage that cd FAILED silently, so every step ran in C:\Windows\System32 (the
rem wrong directory): Codex refused ("not a git repo") and did nothing, and headless Claude could not
rem find its order files and WANDERED into an unrelated project. Root-cause fix below:
rem   1) cd via the script's own location (%~dp0) - Windows resolves it correctly regardless of codepage.
rem   2) this file is now 100%% ASCII (no Korean anywhere) so cmd.exe cannot mis-decode it.
rem   3) hard guards: if cd fails or the order file is missing, write an ALERT and abort - never improvise.
cd /d "%~dp0.." || (echo CD FAILED > "%~dp0ALERT-cd-failed.txt" & exit /b 1)
echo Working dir: %CD%
if not exist "UPDATE_ORDER.md" (echo UPDATE_ORDER.md not found in %CD% - wrong dir, aborting > "ops\ALERT-refresh-wrongdir.txt" & exit /b 1)

echo ===== %date% %time% UPDATE (codex) =====
call "C:\Users\USER\AppData\Roaming\npm\codex.cmd" exec --sandbox danger-full-access -c model_reasoning_effort="medium" "Read UPDATE_ORDER.md in the current directory and execute it fully. Work autonomously until the Definition of done is met." < NUL

echo ===== %date% %time% VERIFY (claude) =====
call "C:\Users\USER\AppData\Roaming\npm\claude.cmd" -p --dangerously-skip-permissions "Read VERIFY_ORDER.md in the current working directory and execute it fully. IMPORTANT: if VERIFY_ORDER.md does not exist in the current directory, STOP immediately and do nothing - do NOT search elsewhere and do NOT work on any other project."

echo ===== %date% %time% DIGEST (send only if fresh changes) =====
py scripts\send_digest.py --if-changes

echo ===== %date% %time% AUDIT OUTREACH (claude) =====
call "C:\Users\USER\AppData\Roaming\npm\claude.cmd" -p --dangerously-skip-permissions "Read AUDIT_OUTREACH_ORDER.md in the current working directory and execute it fully. IMPORTANT: if AUDIT_OUTREACH_ORDER.md does not exist in the current directory, STOP immediately and do nothing - do NOT search elsewhere and do NOT work on any other project."
echo ===== %date% %time% DONE =====
