@echo off
setlocal

for /f "usebackq delims=" %%i in (`wsl.exe bash -lc "wslpath -w \"$(tr -d '\r\n' < /home/dowsmasternode/repos/work-codex/nrg-bloom/content-engine/generated/latest/LATEST.txt)\""`) do set "CONTENT_DIR=%%i"
for /f "usebackq delims=" %%i in (`wsl.exe bash -lc "wslpath -w \"$(tr -d '\r\n' < /home/dowsmasternode/repos/work-codex/nrg-bloom/capital-engine/generated/latest/LATEST.txt)\""`) do set "CAPITAL_DIR=%%i"
for /f "usebackq delims=" %%i in (`wsl.exe bash -lc "wslpath -w \"$(tr -d '\r\n' < /home/dowsmasternode/repos/work-codex/nrg-bloom/authority-engine/generated/latest/LATEST.txt)\""`) do set "AUTHORITY_DIR=%%i"
for /f "usebackq delims=" %%i in (`wsl.exe bash -lc "wslpath -w /home/dowsmasternode/repos/work-codex/nrg-bloom/content-intelligence"`) do set "INTEL_DIR=%%i"
for /f "usebackq delims=" %%i in (`wsl.exe bash -lc "wslpath -w /home/dowsmasternode/repos/work-codex/nrg-bloom/capital-engine/facts/facts-and-numbers-claim-audit-2026-03-26.md"`) do set "AUDIT_FILE=%%i"

start "" explorer.exe "%CONTENT_DIR%"
start "" explorer.exe "%CAPITAL_DIR%"
start "" explorer.exe "%AUTHORITY_DIR%"
start "" explorer.exe "%INTEL_DIR%"
start "" "%AUDIT_FILE%"

endlocal
