@REM untested
@echo off
setlocal enabledelayedexpansion

set PLUGIN_NAME=FieldConnect
for /f "tokens=2 delims==" %%A in ('findstr /b "version=" metadata.txt') do set VERSION=%%A
set VERSION=%VERSION: =%

if "%VERSION%"=="" (
    echo ❌ Could not read version from metadata.txt
    exit /b 1
)

set ZIPFILE=%PLUGIN_NAME%-v%VERSION%.zip

echo 📦 Creating release archive: %ZIPFILE%
git archive --format=zip --output="%ZIPFILE%" --prefix="%PLUGIN_NAME%/" HEAD
echo ✅ Archive created.

@REM set /p ANSWER=🏷️  Create a Git tag "v%VERSION%" and push it? [y/N]
@REM if /i "%ANSWER%"=="Y" (
@REM     git tag -a v%VERSION% -m "Release version %VERSION%"
@REM     git push origin v%VERSION%
@REM     echo ✅ Tag v%VERSION% created and pushed.
@REM ) else (
@REM     echo ℹ️  Skipped tagging.
@REM )
