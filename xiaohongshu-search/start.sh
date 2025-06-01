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

# 创建必要的目录
mkdir -p cache img

# 检查cookie文件
COOKIE_FILE="cache/xiaohongshu_cookies.json"
if [ ! -f "$COOKIE_FILE" ]; then
    echo "未找到小红书cookie文件，需要先获取cookie"
    echo "请选择获取cookie的方式:"
    echo "1. 打开浏览器登录小红书 (可能需要手机验证)"
    echo "2. 手动输入cookie键值对"
    echo "3. 粘贴完整的cookie JSON数据"
    echo "4. 粘贴从浏览器复制的cookie字符串"
    echo "5. 跳过 (搜索功能可能无法使用)"
    read -r -p "请选择 [1-5]: " choice
    
    case $choice in
        1)
            echo "启动登录流程..."
            $PYTHON get_cookies.py
            if [ $? -ne 0 ]; then
                echo "登录失败，请手动运行 $PYTHON get_cookies.py 重试"
                exit 1
            fi
            ;;
        2)
            echo "启动cookie设置工具..."
            $PYTHON set_cookie.py
            if [ $? -ne 0 ]; then
                echo "设置cookie失败，请手动运行 $PYTHON set_cookie.py 重试"
                exit 1
            fi
            ;;
        3)
            echo "启动cookie JSON设置工具..."
            $PYTHON set_cookie_direct.py
            if [ $? -ne 0 ]; then
                echo "设置cookie失败，请手动运行 $PYTHON set_cookie_direct.py 重试"
                exit 1
            fi
            ;;
        4)
            echo "启动cookie字符串设置工具..."
            $PYTHON set_cookie_string.py
            if [ $? -ne 0 ]; then
                echo "设置cookie失败，请手动运行 $PYTHON set_cookie_string.py 重试"
                exit 1
            fi
            ;;
        5)
            echo "跳过登录，但搜索功能可能无法正常使用"
            ;;
        *)
            echo "无效选择，跳过登录"
            ;;
    esac
else
    echo "已找到cookie文件: $COOKIE_FILE"
fi

# 启动服务
echo "启动小红书笔记查询服务..."
$PYTHON app.py 