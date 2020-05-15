
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
REM python Jenkins_simulator_v6.py
python run.py
exit
