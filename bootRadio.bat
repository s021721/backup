@echo off

rem ÿ�춨ʱ�Զ�����ʱ����������������
if %time:~0,2%%time:~3,2% LSS 845 exit
if %time:~0,2%%time:~3,2% GTR 855 exit

ping -n 20 127.1 >nul
ping -n 20 127.1 >nul
ping -n 20 127.1 >nul
ping -n 20 127.1 >nul

echo ******************* start radio for auto boot..........
start D:\software\radio\radio.exe


