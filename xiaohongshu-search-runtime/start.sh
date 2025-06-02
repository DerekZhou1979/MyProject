#!/bin/bash

# 小红书搜索服务启动脚本
# 版本：2.0
# 功能：自动检查环境、安装依赖、启动服务

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python环境
check_python() {
    log_info "检查Python环境..."
    
    if command -v python3 &>/dev/null; then
        PYTHON=python3
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        log_success "找到Python3: $PYTHON_VERSION"
    elif command -v python &>/dev/null; then
        PYTHON=python
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        log_success "找到Python: $PYTHON_VERSION"
    else
        log_error "未找到Python环境，请安装Python 3.7+"
        exit 1
    fi
}

# 检查Chrome浏览器
check_chrome() {
    log_info "检查Chrome浏览器..."
    
    if command -v google-chrome &>/dev/null; then
        log_success "找到Chrome浏览器: $(which google-chrome)"
    elif [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
        log_success "找到Chrome浏览器: /Applications/Google Chrome.app"
    else
        log_warning "未找到Chrome浏览器，Selenium可能无法正常工作"
        log_warning "请安装Chrome浏览器: https://www.google.com/chrome/"
        read -r -p "是否继续? [y/N] " choice
        if [[ ! "$choice" =~ ^[Yy]$ ]]; then
            log_info "已取消启动"
            exit 1
        fi
    fi
}

# 检查并激活虚拟环境
setup_venv() {
    log_info "检查虚拟环境..."
    
    if [ -d "venv" ]; then
        log_info "使用虚拟环境..."
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
            log_success "虚拟环境已激活"
        elif [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate
            log_success "虚拟环境已激活"
        else
            log_warning "虚拟环境存在但无法激活，使用系统Python"
        fi
    else
        log_warning "未找到虚拟环境，使用系统Python"
    fi
}

# 安装依赖
install_dependencies() {
    log_info "检查并安装依赖..."
    
    if [ ! -f "requirements.txt" ]; then
        log_error "未找到requirements.txt文件"
        exit 1
    fi
    
    $PYTHON -m pip install -r requirements.txt --quiet
    log_success "依赖安装完成"
}

# 检查WebDriver
check_webdriver() {
    log_info "检查WebDriver..."
    
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
" 2>/dev/null || log_warning "WebDriver自动配置失败，将使用预配置的驱动"
}

# 创建必要目录
create_directories() {
    log_info "创建必要的目录..."
    mkdir -p cache img
    log_success "目录创建完成"
}

# 检查并清理端口
check_port() {
    local port=8080
    log_info "检查端口 $port 是否被占用..."
    
    PORT_PID=$(lsof -ti:$port 2>/dev/null || true)
    if [ ! -z "$PORT_PID" ]; then
        log_warning "发现端口 $port 被进程 $PORT_PID 占用"
        log_info "正在停止占用进程..."
        kill -9 $PORT_PID 2>/dev/null || true
        sleep 2
        
        # 再次检查端口是否释放
        if lsof -ti:$port &>/dev/null; then
            log_warning "端口 $port 仍被占用，可能需要手动处理"
            log_info "查看占用进程: lsof -i:$port"
            log_info "强制停止: sudo kill -9 \$(lsof -ti:$port)"
            read -r -p "是否继续启动? [y/N] " choice
            if [[ ! "$choice" =~ ^[Yy]$ ]]; then
                log_info "已取消启动"
                exit 1
            fi
        else
            log_success "端口 $port 已释放"
        fi
    else
        log_success "端口 $port 可用"
    fi
}

# 清理缓存文件
clean_cache() {
    log_info "清理cache文件夹中的临时文件..."
    
    if [ -d "cache" ]; then
        # 统计要删除的文件数量
        TEMP_FILES_COUNT=$(find cache -type f ! -name "xiaohongshu_cookies.json" | wc -l | tr -d ' ')
        if [ "$TEMP_FILES_COUNT" -gt 0 ]; then
            log_info "发现 $TEMP_FILES_COUNT 个临时文件，正在清理..."
            # 删除除了xiaohongshu_cookies.json以外的所有文件
            find cache -type f ! -name "xiaohongshu_cookies.json" -delete
            log_success "临时文件清理完成"
        else
            log_info "cache文件夹中没有需要清理的临时文件"
        fi
    else
        log_info "cache文件夹不存在，跳过清理"
    fi
}

# 显示启动信息
show_startup_info() {
    echo ""
    echo "============================================================"
    echo "🔍 小红书搜索服务准备启动"
    echo "============================================================"
    echo "📋 注意事项："
    echo "  • 程序将在启动时自动打开浏览器进行登录"
    echo "  • 请在浏览器中完成小红书登录（支持扫码或密码登录）"
    echo "  • 登录成功后服务将自动启动"
    echo "  • 服务地址: http://localhost:8080"
    echo "============================================================"
    read -r -p "按回车键继续..."
}

# 启动服务
start_service() {
    log_info "启动小红书搜索服务..."
    
    # 检查主程序文件
    if [ -f "main.py" ]; then
        $PYTHON main.py
    elif [ -f "app.py" ]; then
        $PYTHON app.py
    else
        log_error "未找到主程序文件 (main.py 或 app.py)"
        exit 1
    fi
}

# 主函数
main() {
    echo "🚀 小红书搜索服务启动脚本 v2.0"
    echo ""
    
    # 执行检查和准备步骤
    check_python
    check_chrome
    setup_venv
    install_dependencies
    check_webdriver
    create_directories
    check_port
    clean_cache
    
    # 显示启动信息
    show_startup_info
    
    # 启动服务
    start_service
}

# 错误处理
trap 'log_error "脚本执行被中断"; exit 1' INT TERM

# 执行主函数
main "$@" 