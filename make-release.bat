@echo off
@REM untested
setlocal enabledelayedexpansion

set PLUGIN_NAME=field_connect

rem --- Read version from metadata.txt ---
for /f "tokens=2 delims==" %%A in ('findstr /b "version=" metadata.txt') do (
    set VERSION=%%A
)
set VERSION=%VERSION: =%

if "%VERSION%"=="" (
    echo Could not read version from metadata.txt
    exit /b 1
)

rem --- Output zip in plugin folder ---
set "ZIPFILE=%~dp0%PLUGIN_NAME%-v%VERSION%.zip"

echo Creating stripped release: %ZIPFILE%

rem --- Create temp folder ---
for /f "usebackq" %%d in (`powershell -command "[System.IO.Path]::GetTempPath()"`) do set TMP=%%d
set TMPDIR=%TMP%%RANDOM%%RANDOM%
mkdir "%TMPDIR%"

rem --- Extract repo content into temp dir ---
powershell -command "git archive HEAD | tar -x -C '%TMPDIR%'"

echo Stripping comments...

rem --- Process all .py files ---
for /r "%TMPDIR%" %%f in (*.py) do (
    powershell -noprofile -command ^
        "(Get-Content '%%f') |
        ForEach-Object {
            if($_ -match '^\s*#!') { $_ }                   # keep shebang
            elseif($_ -match '^\s*#') { }                   # skip full-line comment
            else { $_ -replace '\s+#.*$','' }               # remove trailing comments
        } | Set-Content '%%f.tmp'"
    move /y "%%f.tmp" "%%f" >nul
)

rem --- Zip to final output ---
cd /d "%TMPDIR%"
powershell -command "Compress-Archive -Path '%PLUGIN_NAME%' -DestinationPath '%ZIPFILE%' -Force"
cd /d "%~dp0"

rem --- Optional tagging ---
rem echo.
rem set /p answer=🏷️  Create a Git tag 'v%VERSION%' and push it? [y/N]
rem if /I "%answer%"=="y" (
rem     git tag -a "v%VERSION%" -m "Release version %VERSION%"
rem     git push origin "v%VERSION%"
rem     echo Tag 'v%VERSION%' created and pushed.
rem ) else (
rem     echo Skipped tagging.
rem )

rem --- Cleanup ---
rmdir /s /q "%TMPDIR%"

echo Release created: %ZIPFILE%
endlocal
