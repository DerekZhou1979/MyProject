@echo off
echo 启动小红书笔记查询服务...

REM 检查Python环境
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到Python环境，请安装Python 3.7+
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist venv\Scripts\activate.bat (
    echo 使用虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 未找到虚拟环境，使用系统Python
)

REM 检查依赖
echo 检查依赖...
python -m pip install -r requirements.txt

REM 创建必要的目录
if not exist cache mkdir cache
if not exist img mkdir img

REM 启动服务
echo 启动小红书笔记查询服务...
python app.py

pause 