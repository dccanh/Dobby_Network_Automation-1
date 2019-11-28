@echo off

SET stage=Ph1
SET version=v1
SET serial_number=0001
SET serial_port=COM3

SET scr_dir=%~dp0
SET test_dir=%scr_dir%\networkbu\Test\T10x
SET config_dir=%scr_dir%\networkbu\Helper\t10x\config 


echo config_dir: %config_dir%

cd %config_dir%
python write_config.py %stage% %version% %serial_number% %serial_port%

echo test_dir: %test_dir%

cd %test_dir%
python Before_test.py

python Home.py

python After_test.py
echo scr_dir: %scr_dir%
cd %src_dir%