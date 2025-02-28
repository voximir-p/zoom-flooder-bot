@ECHO OFF
:choice
cls
set /P c=Did you want to install?[Y/n]: 
if /I "%c%" EQU "Y" goto :continue
if /I "%c%" EQU "n" goto :exit
goto :choice

:continue
cls
echo Installing Please wait...
pip install selenium
pip install keyboard
cls
echo Installed!
pause
exit

:exit
cls
echo Exiting...
pause
exit
