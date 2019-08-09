@echo off
SET script_dir=%~dp0
SET start_dir=%script_dir%\..\Test\WEB_UI\NOVA_UI

cd %start_dir%
python run_start.py %model% %rg_port% %cm_port% %reboot%
