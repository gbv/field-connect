@echo off
REM untested
REM Creates a distributable plugin ZIP and optionally adds a version tag

set PLUGIN_NAME=field_connect

for /f "tokens=2 delims==" %%A in ('findstr /R "^version=" metadata.txt') do set VERSION=%%A
set VERSION=%VERSION: =%

if "%VERSION%"=="" (
  echo ❌ Could not read version from metadata.txt
  exit /b 1
)

REM --- Output ZIP in plugin folder ---
set ZIPFILE=%CD%\%PLUGIN_NAME%-v%VERSION%.zip

REM Create temp directory
set TMPDIR=%TEMP%\%PLUGIN_NAME%_%RANDOM%
mkdir "%TMPDIR%"
echo 📁 Using temporary directory: %TMPDIR%

REM Export plugin to temp folder
git archive --format=tar --prefix="%PLUGIN_NAME%/" HEAD | tar -x -C "%TMPDIR%"

REM Strip # comments but keep docstrings, shebangs, and spacing
echo 🧹 Stripping comments from Python files...
powershell -NoProfile -Command ^
  "Get-ChildItem '%TMPDIR%\%PLUGIN_NAME%' -Recurse -Filter *.py | ForEach-Object { ^
    $lines = Get-Content $_.FullName; ^
    $out = foreach ($l in $lines) { ^
      if ($l -match '^\s*#') { continue } ^
      ($l -replace '\s+#.*$', '') ^
    }; ^
    Set-Content -Encoding UTF8 $_.FullName $out ^
  }"

REM Create final ZIP
echo 📦 Creating release archive: %ZIPFILE%
powershell -NoProfile -Command ^
  "Compress-Archive -Path '%TMPDIR%\%PLUGIN_NAME%' -DestinationPath '%ZIPFILE%' -Force"

REM Cleanup
rmdir /S /Q "%TMPDIR%"

echo ✅ Archive created: %ZIPFILE%

REM --- Optional tagging ---
REM echo.
REM set /p ANSWER=🏷️  Create a Git tag 'v%VERSION%' and push it? [y/N]
REM if /I "%ANSWER%"=="Y" (
REM   git tag -a "v%VERSION%" -m "Release version %VERSION%"
REM   git push origin "v%VERSION%"
REM   echo ✅ Tag 'v%VERSION%' created and pushed.
REM ) else (
REM   echo ℹ️  Skipped tagging.
REM )
