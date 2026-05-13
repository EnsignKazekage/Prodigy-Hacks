@echo off
:: Prodigy Companion - Windows one-command installer (cmd-friendly)
:: Usage from cmd.exe:
::   curl -sSL https://raw.githubusercontent.com/EnsignKazekage/Prodigy-Hacks/main/scripts/install.bat -o install.bat && install.bat

setlocal enabledelayedexpansion

set "REPO=https://github.com/EnsignKazekage/Prodigy-Hacks"
set "INSTALL_DIR=%USERPROFILE%\ProdigyCompanion"
set "BAT_DIR=%LOCALAPPDATA%\Programs\ProdigyCompanion"
set "BAT_PATH=%BAT_DIR%\prodigy.bat"

cls
echo.
echo   Prodigy Companion - Installer
echo   -----------------------------
echo.

:: --- Python check ----------------------------------------------------------
echo   [1/4] Checking Python 3.10+...
python --version >nul 2>&1
if errorlevel 1 (
    echo   Python not found, installing via winget...
    winget install Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts"
)
echo   OK Python ready

:: --- Git check -------------------------------------------------------------
echo   [2/4] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo   Git not found, installing via winget...
    winget install Git.Git -e --silent --accept-package-agreements --accept-source-agreements
    set "PATH=%PATH%;%ProgramFiles%\Git\cmd"
)
echo   OK Git ready

:: --- Clone or update -------------------------------------------------------
echo   [3/4] Setting up Prodigy Companion...
if exist "%INSTALL_DIR%" (
    pushd "%INSTALL_DIR%"
    git pull --quiet
    popd
) else (
    git clone %REPO% "%INSTALL_DIR%" --quiet
)

:: --- Dependencies ----------------------------------------------------------
echo   [4/4] Installing Python dependencies...
pushd "%INSTALL_DIR%"
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
popd

:: --- Create launcher -------------------------------------------------------
if not exist "%BAT_DIR%" mkdir "%BAT_DIR%"
(
echo @echo off
echo python "%INSTALL_DIR%\prodigy.py" %%*
) > "%BAT_PATH%"

:: --- Add to PATH if missing ------------------------------------------------
echo %PATH% | findstr /C:"ProdigyCompanion" >nul
if errorlevel 1 (
    setx PATH "%PATH%;%BAT_DIR%" >nul
)

echo.
echo   ==========================================
echo   Installation complete!
echo.
echo   Restart your terminal, then run:
echo.
echo     prodigy login --token YOUR_TOKEN
echo     prodigy use YOUR_CHILD_USER_ID
echo     prodigy week
echo     prodigy skills
echo     prodigy screen-time
echo.
echo   How to get your token:
echo     See %REPO%#getting-your-session-token
echo   ==========================================
echo.

endlocal
