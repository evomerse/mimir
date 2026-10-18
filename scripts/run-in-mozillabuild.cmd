@echo off
rem Lance un script bash dans le shell MozillaBuild :
rem   run-in-mozillabuild.cmd /c/mimir/scripts/bootstrap-windows.sh [arguments]
C:\mozilla-build\start-shell.bat -no-start -defterm -c "bash %~1 %~2"
