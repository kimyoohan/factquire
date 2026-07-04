@echo off
rem ModelWire weekly refresh: Codex re-collects, Claude cross-verifies and pushes on pass.
rem Registered in Windows Task Scheduler as "ModelWire Weekly Refresh" (Mondays 10:17).
cd /d "E:\0.세계1등기업\modelwire"
echo ===== %date% %time% UPDATE (codex) =====
call "C:\Users\USER\AppData\Roaming\npm\codex.cmd" exec --sandbox danger-full-access -c model_reasoning_effort="medium" "Read UPDATE_ORDER.md in this directory and execute it fully. Work autonomously until the Definition of done is met." < NUL
echo ===== %date% %time% VERIFY (claude) =====
call "C:\Users\USER\AppData\Roaming\npm\claude.cmd" -p --dangerously-skip-permissions "Read VERIFY_ORDER.md in this directory and execute it fully. Work autonomously until the protocol is complete."
echo ===== %date% %time% DONE =====
