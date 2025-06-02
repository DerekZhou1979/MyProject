@echo off
chcp 65001 >nul
title 小红书搜索服务启动器

echo ============================================================
echo 🚀 小红书搜索服务启动脚本 v2.0
echo ============================================================
echo.

REM 检查Python环境
echo [INFO] 检查Python环境...
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON=python
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [SUCCESS] 找到Python: !PYTHON_VERSION!
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON=python3
        for /f "tokens=2" %%i in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%i
        echo [SUCCESS] 找到Python3: !PYTHON_VERSION!
    ) else (
        echo [ERROR] 未找到Python环境，请安装Python 3.7+
        echo 下载地址: https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

REM 检查Chrome浏览器
echo [INFO] 检查Chrome浏览器...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo [SUCCESS] 找到Chrome浏览器
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo [SUCCESS] 找到Chrome浏览器
) else (
    echo [WARNING] 未找到Chrome浏览器，Selenium可能无法正常工作
    echo 请安装Chrome浏览器: https://www.google.com/chrome/
    set /p choice="是否继续? [y/N]: "
    if /i not "%choice%"=="y" (
        echo [INFO] 已取消启动
        pause
        exit /b 1
    )
)

REM 检查虚拟环境
echo [INFO] 检查虚拟环境...
if exist venv\Scripts\activate.bat (
    echo [INFO] 使用虚拟环境...
    call venv\Scripts\activate.bat
    echo [SUCCESS] 虚拟环境已激活
) else (
    echo [WARNING] 未找到虚拟环境，使用系统Python
)

REM 检查依赖文件
if not exist requirements.txt (
    echo [ERROR] 未找到requirements.txt文件
    pause
    exit /b 1
)

REM 安装依赖
echo [INFO] 检查并安装依赖...
%PYTHON% -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] 依赖安装失败
    pause
    exit /b 1
)
echo [SUCCESS] 依赖安装完成

REM 创建必要的目录
echo [INFO] 创建必要的目录...
if not exist cache mkdir cache
if not exist img mkdir img
echo [SUCCESS] 目录创建完成

REM 显示启动信息
echo.
echo ============================================================
echo 🔍 小红书搜索服务准备启动
echo ============================================================
echo 📋 注意事项：
echo   • 程序将在启动时自动打开浏览器进行登录
echo   • 请在浏览器中完成小红书登录（支持扫码或密码登录）
echo   • 登录成功后服务将自动启动
echo   • 服务地址: http://localhost:8080
echo ============================================================
pause

REM 启动服务
echo [INFO] 启动小红书搜索服务...
if exist main.py (
    %PYTHON% main.py
) else if exist app.py (
    %PYTHON% app.py
) else (
    echo [ERROR] 未找到主程序文件 (main.py 或 app.py)
    pause
    exit /b 1
)

pause 