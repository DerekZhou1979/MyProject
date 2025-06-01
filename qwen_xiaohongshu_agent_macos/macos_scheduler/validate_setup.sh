#!/bin/bash
# 用于验证macOS定时任务设置的测试脚本

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

echo -e "${YELLOW}===== 验证Qwen-Max到小红书自动化的macOS定时任务设置 =====${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SETUP_SCRIPT="$SCRIPT_DIR/setup_cron.sh"

# 检查setup_cron.sh是否存在
if [ ! -f "$SETUP_SCRIPT" ]; then
    echo -e "${RED}错误: 未找到setup_cron.sh脚本${NC}"
    exit 1
fi

# 检查脚本权限
if [ ! -x "$SETUP_SCRIPT" ]; then
    echo -e "${YELLOW}设置执行权限...${NC}"
    chmod +x "$SETUP_SCRIPT"
fi

# 验证cron服务是否运行
echo -e "${YELLOW}检查cron服务状态...${NC}"
if pgrep -x "cron" > /dev/null || pgrep -x "crond" > /dev/null; then
    echo -e "${GREEN}cron服务正在运行${NC}"
else
    echo -e "${YELLOW}注意: 未检测到cron服务运行${NC}"
    echo -e "${YELLOW}这可能是正常的，因为macOS使用launchd管理cron任务${NC}"
fi

# 验证用户是否有crontab权限
echo -e "${YELLOW}检查crontab权限...${NC}"
if crontab -l > /dev/null 2>&1; then
    echo -e "${GREEN}用户有crontab权限${NC}"
else
    echo -e "${RED}警告: 用户可能没有crontab权限${NC}"
    echo -e "${YELLOW}请确保您有足够的权限设置cron任务${NC}"
fi

# 验证Python环境
echo -e "${YELLOW}检查Python环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}$PYTHON_VERSION 已安装${NC}"
else
    echo -e "${RED}警告: 未找到Python3${NC}"
    echo -e "${YELLOW}请安装Python3以确保脚本正常运行${NC}"
fi

# 验证必要的Python包
echo -e "${YELLOW}检查必要的Python包...${NC}"
MISSING_PACKAGES=()

if ! python3 -c "import requests" 2>/dev/null; then
    MISSING_PACKAGES+=("requests")
fi

if ! python3 -c "import playwright" 2>/dev/null; then
    MISSING_PACKAGES+=("playwright")
fi

if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
    echo -e "${GREEN}所有必要的Python包已安装${NC}"
else
    echo -e "${YELLOW}缺少以下Python包: ${MISSING_PACKAGES[*]}${NC}"
    echo -e "${YELLOW}setup_cron.sh脚本将尝试安装这些包${NC}"
fi

# 验证目录结构
echo -e "${YELLOW}检查项目目录结构...${NC}"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PARENT_DIR/src"
MAIN_SCRIPT="$SRC_DIR/main.py"

if [ -d "$SRC_DIR" ] && [ -f "$MAIN_SCRIPT" ]; then
    echo -e "${GREEN}项目目录结构正确${NC}"
else
    echo -e "${RED}警告: 项目目录结构不完整${NC}"
    echo -e "${YELLOW}请确保src目录和main.py脚本存在${NC}"
fi

echo ""
echo -e "${GREEN}验证完成${NC}"
echo -e "${YELLOW}您可以运行setup_cron.sh脚本来设置定时任务${NC}"
echo ""
