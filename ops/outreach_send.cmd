@echo off
rem FactQuire outreach dispatch: send queued items in the US-morning window.
rem Registered in Windows Task Scheduler as "FactQuire Outreach Send" (Tuesdays 23:00 KST).
rem FIX 2026-07-25: hardcoded non-ASCII E:\ path removed (drive dead + codepage cd bug, see weekly_refresh.cmd).
cd /d "%~dp0.." || (echo CD FAILED > "%~dp0ALERT-cd-failed.txt" & exit /b 1)
if not exist "SEND_ORDER.md" (echo SEND_ORDER.md not found in %CD% - wrong dir, aborting > "ops\ALERT-outreach-wrongdir.txt" & exit /b 1)
echo ===== %date% %time% OUTREACH DISPATCH (claude) =====
call "C:\Users\USER\AppData\Roaming\npm\claude.cmd" -p --dangerously-skip-permissions "Read SEND_ORDER.md in this directory and execute it fully. Work autonomously until the protocol is complete." >> ops\outreach\dispatch.log 2>&1
echo ===== %date% %time% DONE =====
