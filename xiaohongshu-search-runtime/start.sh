#!/bin/bash

# 检查Python环境
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "错误: 未找到Python环境，请安装Python 3.7+"
    exit 1
fi

# 检查Chrome浏览器
if ! command -v google-chrome &>/dev/null && ! command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" &>/dev/null; then
    echo "警告: 未找到Chrome浏览器，Selenium可能无法正常工作"
    echo "请安装Chrome浏览器后再运行此脚本"
    echo "下载地址: https://www.google.com/chrome/"
    read -r -p "是否继续? [y/N] " choice
    if [[ ! "$choice" =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 1
    fi
fi

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "使用虚拟环境..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo "警告: 虚拟环境存在但无法激活，使用系统Python"
    fi
else
    echo "未找到虚拟环境，使用系统Python"
fi

# 检查依赖
echo "检查依赖..."
$PYTHON -m pip install -r requirements.txt

# 检查WebDriver
echo "检查WebDriver..."
$PYTHON -c "
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    print('正在自动下载和配置WebDriver...')
    service = Service(ChromeDriverManager().install())
    print('WebDriver配置成功')
except Exception as e:
    print(f'警告: WebDriver配置失败: {str(e)}')
    print('脚本将尝试使用系统已安装的WebDriver')
"

# 创建必要的目录
mkdir -p cache img

# 检查并清理8080端口
echo "检查8080端口是否被占用..."
PORT_PID=$(lsof -ti:8080 2>/dev/null)
if [ ! -z "$PORT_PID" ]; then
    echo "发现8080端口被进程 $PORT_PID 占用，正在停止该进程..."
    kill -9 $PORT_PID 2>/dev/null
    sleep 2
    # 再次检查端口是否释放
    if lsof -ti:8080 &>/dev/null; then
        echo "警告: 8080端口仍被占用，可能需要手动处理"
        echo "可以使用以下命令查看占用进程: lsof -i:8080"
        echo "可以使用以下命令强制停止: sudo kill -9 \$(lsof -ti:8080)"
        read -r -p "是否继续启动? [y/N] " choice
        if [[ ! "$choice" =~ ^[Yy]$ ]]; then
            echo "已取消启动"
            exit 1
        fi
    else
        echo "端口8080已释放"
    fi
else
    echo "端口8080可用"
fi

# 清理cache文件夹中的临时文件（保留xiaohongshu_cookies.json）
echo "清理cache文件夹中的临时文件..."
if [ -d "cache" ]; then
    # 统计要删除的文件数量
    TEMP_FILES_COUNT=$(find cache -type f ! -name "xiaohongshu_cookies.json" | wc -l | tr -d ' ')
    if [ "$TEMP_FILES_COUNT" -gt 0 ]; then
        echo "发现 $TEMP_FILES_COUNT 个临时文件，正在清理..."
        # 删除除了xiaohongshu_cookies.json以外的所有文件
        find cache -type f ! -name "xiaohongshu_cookies.json" -delete
        echo "临时文件清理完成"
    else
        echo "cache文件夹中没有需要清理的临时文件"
    fi
else
    echo "cache文件夹不存在，跳过清理"
fi

echo "============================================================"
echo "小红书搜索服务准备启动..."
echo "注意：程序将在启动时自动打开浏览器进行登录"
echo "请在浏览器中完成小红书登录（支持扫码或密码登录）"
echo "登录成功后服务将自动启动"
echo "============================================================"
read -r -p "按回车键继续..."

# 启动服务
echo "启动小红书笔记查询服务..."
$PYTHON app.py 