@echo off
setlocal
wsl.exe bash -lc "cd /home/dowsmasternode/repos/work-codex/nrg-bloom/codex-output-hub && ./start_hub.sh"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8771/codex-output-hub/index.html"
endlocal
