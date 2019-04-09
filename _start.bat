rem @echo off
@color 0A
@cls

SET script_dir=%~dp0
SET binaries_dir=%script_dir%\binaries\
SET utils_dir=%script_dir%\utils\

SET SecureCRT="C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe"
SET TFTPd64="C:\Program Files\Tftpd64\tftpd64.exe"
SET Seven_Zip="C:\Program Files\7-Zip\7z.exe"

SET URL_images=%1
SET zip_images="fw_images.zip"
SET user="admin:password"

SET READY_SEC=120

SET BAUD_RATE=115200
SET RG_COM_PORT=COM5
SET CM_COM_PORT=COM6

SET RG_IP=192.168.0.11
SET PC_IP=192.168.0.29

if not exist %SecureCRT% (
    echo %SecureCRT% not exist. Exit!!!
    exit /B -1
)

if not exist %TFTPd64% (
    echo %TFTPd64% not exist. Exit!!!
    exit /B -1
)

if not exist %Seven_Zip% (
    echo %Seven_Zip% not exist. Exit!!!
    exit /B -1
)

IF [%URL_images%] EQU [] (
    echo.
    echo URL_images not be input. Using the default URL.
    SET URL_images="http://arti.humaxdigital.com:8081/artifactory/Vina_automation/Network/hga20r_fw_images.zip"
)

echo.
echo script_dir: %script_dir%
echo binaries_dir: %binaries_dir%
echo utils_dir: %utils_dir%

if exist "%script_dir%\%zip_images%" (
    echo Removing the existed firmwares before downloading.
    del /s /f /q "%script_dir%\%zip_images%"
)

echo.
echo Getting firmware images from server: %URL_images%
curl --retry 3 -u %user% %URL_images% -o "%script_dir%\%zip_images%"
if errorlevel 1 (
    echo Download firmware images FAIL. Exit!!!
    exit /B -1
)

echo.
echo Checking the downloaded firmware images: %script_dir%\%zip_images%
if not exist "%script_dir%\%zip_images%" (
    echo The firmwares not exist. Exit!!!
    exit /B -1
)

echo.
echo Extracting the downloaded firmware images....
%Seven_Zip% x "%script_dir%\%zip_images%" -o%binaries_dir% -aoa
if errorlevel 1 (
    echo Something wrong when extract the downloaded firmware images. Exit!!!
    exit /B -1
)

echo.
echo Need to kill some processes before flashing firmware images...
tasklist /fi "imagename eq SecureCRT.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "SecureCRT.exe"
tasklist /fi "imagename eq tftpd64.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "tftpd64.exe"

echo.
echo Enabling CM console if disabled...
%SecureCRT% /SCRIPT "%utils_dir%\enable_cm_console.py" /SERIAL %RG_COM_PORT% /BAUD %BAUD_RATE%

call echo.
echo Starting TFTP server...
start "TFTPd64" %TFTPd64%
if errorlevel 1 (
    echo Could not start: %TFTPd64%. Exit!!!
    exit /B -1
)

echo.
echo Flashing firmware images...
%SecureCRT% /ARG %binaries_dir% /ARG %RG_IP% /ARG %PC_IP% /SCRIPT "%utils_dir%\flash_fw_silent.py" /SERIAL %CM_COM_PORT% /BAUD %BAUD_RATE%

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
