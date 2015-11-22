@echo off
set OLDDIR=%CD%
cd %~p0
call cfg\config.bat
call %%python%% .\dialog.py %*
cd %OLDDIR%
