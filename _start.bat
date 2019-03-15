@echo off
@color 0A
@cls

SET script_dir=%~dp0

SET SecureCRT="C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe"
SET TFTPd64="C:\Program Files\Tftpd64\tftpd64.exe"
SET Seven_Zip="C:\Program Files\7-Zip\7z.exe"

SET URL_images="ftp://ftp.adobe.com/license.txt"
SET zip_images="fw_images.zip"

SET READY_SEC=120

SET BAUD_RATE=115200
SET COM_PORT=COM6

SET RG_IP=192.168.0.11
SET PC_IP=192.168.0.29


echo script_dir: %script_dir%
echo.
echo Getting firmware images from server....
bitsadmin /transfer "Downloading firmware images" %URL_images% "%script_dir%\%zip_images%"

echo.
echo Extracting downloaded firmware images....
%Seven_Zip% x "%script_dir%\%zip_images%" -o%script_dir% -aoa
rem del "%script_dir%\%zip_images%" /s /f /q

echo.
echo Need to kill some processes before flashing firmware images...
tasklist /fi "imagename eq SecureCRT.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "SecureCRT.exe"
tasklist /fi "imagename eq tftpd64.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "tftpd64.exe"

echo.
echo Starting TFTP server...
start "TFTPd64" %TFTPd64%

echo.
echo Flashing firmware images...
rem rem start "" %SecureCRT% /SCRIPT "Z:\_Share\TFTP\01\_tmp.py" /ARG %script_dir%
%SecureCRT% /ARG %script_dir% /ARG %RG_IP% /ARG %PC_IP% /SCRIPT "%script_dir%\flash_fw_silent.py" /SERIAL %COM_PORT% /BAUD %BAUD_RATE%

echo.
echo Killing processes after flashed firmware images...
tasklist /fi "imagename eq SecureCRT.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "SecureCRT.exe"
tasklist /fi "imagename eq tftpd64.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "tftpd64.exe"

echo.
echo Ready to run Automation test after %READY_SEC% seconds...
rem sleep %READY_SEC%

echo.
echo Done.
