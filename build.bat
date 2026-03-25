@echo off
setlocal EnableDelayedExpansion

set APP_NAME=TerminalX
set APP_VERSION=34.0
set MAIN_SCRIPT=TerminalX.py
set SPEC_FILE=TerminalX.spec
set ICON_FILE=ico.ico
set VERSION_FILE=version_info.txt
set DIST_DIR=dist
set BUILD_DIR=build

set FLAG_DEBUG=0
set FLAG_NO_UPX=0
set FLAG_CLEAN=0

for %%A in (%*) do (
    if /I "%%A"=="--debug"   set FLAG_DEBUG=1
    if /I "%%A"=="--no-upx"  set FLAG_NO_UPX=1
    if /I "%%A"=="--clean"   set FLAG_CLEAN=1
)

echo.
echo %APP_NAME% v%APP_VERSION% - EXE Builder
echo.

if "%FLAG_CLEAN%"=="1" (
    echo Cleaning build artifacts...
    if exist "%BUILD_DIR%" rmdir /S /Q "%BUILD_DIR%"
    if exist "%DIST_DIR%"  rmdir /S /Q "%DIST_DIR%"
    echo Done.
    goto :EOF
)

if not exist "%MAIN_SCRIPT%" (
    echo ERROR: %MAIN_SCRIPT% not found.
    exit /b 1
)

if not exist "%ICON_FILE%"    set ICON_FILE=
if not exist "%VERSION_FILE%" set VERSION_FILE=

echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found on PATH.
    exit /b 1
)
for /f "tokens=2 delims= " %%V in ('python --version 2^>^&1') do echo       Python %%V found.

echo [2/5] Checking PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo       Installing PyInstaller...
    python -m pip install pyinstaller --quiet
    if errorlevel 1 ( echo ERROR: pip install failed. & exit /b 1 )
) else (
    for /f %%V in ('python -m PyInstaller --version 2^>^&1') do echo       PyInstaller %%V found.
)

echo [3/5] Checking Pillow...
python -c "from PIL import Image" >nul 2>&1
if errorlevel 1 (
    echo       Installing Pillow...
    python -m pip install Pillow --quiet
)

echo [4/5] Cleaning previous build...
if exist "%BUILD_DIR%" rmdir /S /Q "%BUILD_DIR%"
if exist "%DIST_DIR%"  rmdir /S /Q "%DIST_DIR%"

echo [5/5] Building EXE...

if exist "%SPEC_FILE%" (
    echo       Using: %SPEC_FILE%
    python -m PyInstaller "%SPEC_FILE%"
    goto :check
)

set CMD=python -m PyInstaller --onefile --console --name "%APP_NAME%" --optimize 1
if not "%ICON_FILE%"==""    set CMD=!CMD! --icon "%ICON_FILE%"
if not "%VERSION_FILE%"=="" set CMD=!CMD! --version-file "%VERSION_FILE%"
set CMD=!CMD! --hidden-import readline --hidden-import curses --hidden-import curses.ascii
set CMD=!CMD! --hidden-import tty --hidden-import termios --hidden-import fcntl
set CMD=!CMD! --hidden-import pwd --hidden-import grp --hidden-import stat
set CMD=!CMD! --hidden-import getpass --hidden-import platform --hidden-import configparser
set CMD=!CMD! --hidden-import csv --hidden-import difflib --hidden-import glob
set CMD=!CMD! --hidden-import math --hidden-import statistics --hidden-import string
set CMD=!CMD! --hidden-import struct --hidden-import uuid --hidden-import zipfile
set CMD=!CMD! --hidden-import tarfile --hidden-import threading --hidden-import socket
set CMD=!CMD! --hidden-import http.server --hidden-import urllib.request
set CMD=!CMD! --hidden-import urllib.error --hidden-import urllib.parse
set CMD=!CMD! --hidden-import importlib.util --hidden-import importlib.metadata
set CMD=!CMD! --hidden-import ctypes --hidden-import ctypes.util
set CMD=!CMD! --hidden-import tkinter --hidden-import tkinter.ttk
set CMD=!CMD! --hidden-import PIL --hidden-import PIL.Image --hidden-import PIL.ImageTk
if not "%ICON_FILE%"=="" set CMD=!CMD! --add-data "%ICON_FILE%;."
if "%FLAG_NO_UPX%"=="1"  set CMD=!CMD! --noupx
if "%FLAG_DEBUG%"=="1"   set CMD=!CMD! --debug all
set CMD=!CMD! "%MAIN_SCRIPT%"
!CMD!

:check
if errorlevel 1 (
    echo.
    echo ERROR: Build failed.
    exit /b 1
)

if not exist "%DIST_DIR%\%APP_NAME%.exe" (
    echo ERROR: EXE not found after build.
    exit /b 1
)

for %%F in ("%DIST_DIR%\%APP_NAME%.exe") do set EXE_SIZE=%%~zF
set /a EXE_MB=%EXE_SIZE% / 1048576

echo.
echo BUILD OK: %DIST_DIR%\%APP_NAME%.exe  (%EXE_MB% MB)
echo.

endlocal
