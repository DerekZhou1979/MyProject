#!/bin/bash
# macOS定时任务设置脚本
# 用于设置自动运行Qwen-Max到小红书自动化脚本的cron任务

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

# 打印欢迎信息
echo -e "${GREEN}===== Qwen-Max到小红书自动化脚本 - macOS定时任务设置 =====${NC}"
echo ""

# 检查Python环境
echo -e "${YELLOW}检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}未找到Python3，请安装Python3后再运行此脚本${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "Python版本: ${GREEN}$PYTHON_VERSION${NC}"

# 检查依赖
echo -e "${YELLOW}检查依赖包...${NC}"
if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}安装requests包...${NC}"
    pip3 install requests
fi

if ! python3 -c "import playwright" 2>/dev/null; then
    echo -e "${YELLOW}安装playwright包...${NC}"
    pip3 install playwright
    echo -e "${YELLOW}安装playwright浏览器...${NC}"
    python3 -m playwright install chromium
fi

# 创建运行脚本
echo -e "${YELLOW}创建运行脚本...${NC}"
RUN_SCRIPT="$SCRIPT_DIR/run_automation.sh"

cat > "$RUN_SCRIPT" << EOL
#!/bin/bash
# 自动运行Qwen-Max到小红书自动化脚本

# 获取脚本所在目录
SCRIPT_DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="\$(dirname "\$SCRIPT_DIR")"

# 设置日志文件
LOG_DIR="\$PARENT_DIR/logs"
mkdir -p "\$LOG_DIR"
LOG_FILE="\$LOG_DIR/cron_run_\$(date +%Y%m%d_%H%M%S).log"

# 记录开始时间
echo "===== 开始运行: \$(date) =====" >> "\$LOG_FILE"

# 切换到项目目录并运行脚本
cd "\$PARENT_DIR" && \\
python3 "\$PARENT_DIR/src/main.py" >> "\$LOG_FILE" 2>&1

# 记录结束时间和状态
if [ \$? -eq 0 ]; then
    echo "===== 运行成功: \$(date) =====" >> "\$LOG_FILE"
else
    echo "===== 运行失败: \$(date) =====" >> "\$LOG_FILE"
fi
EOL

# 设置执行权限
chmod +x "$RUN_SCRIPT"
echo -e "${GREEN}运行脚本已创建: $RUN_SCRIPT${NC}"

# 创建cron任务
echo -e "${YELLOW}设置cron任务...${NC}"
echo ""
echo -e "${YELLOW}请选择定时任务频率:${NC}"
echo "1) 每天运行一次"
echo "2) 每周运行一次"
echo "3) 自定义cron表达式"
echo ""
read -p "请输入选项 [1-3]: " OPTION

case $OPTION in
    1)
        echo -e "${YELLOW}请输入每天运行的时间 (格式: HH:MM，例如: 09:30):${NC}"
        read -p "时间: " DAILY_TIME
        HOUR=$(echo $DAILY_TIME | cut -d':' -f1)
        MINUTE=$(echo $DAILY_TIME | cut -d':' -f2)
        CRON_EXPR="$MINUTE $HOUR * * *"
        CRON_DESC="每天 $DAILY_TIME"
        ;;
    2)
        echo -e "${YELLOW}请选择每周运行的星期几:${NC}"
        echo "1) 星期一"
        echo "2) 星期二"
        echo "3) 星期三"
        echo "4) 星期四"
        echo "5) 星期五"
        echo "6) 星期六"
        echo "7) 星期日"
        read -p "星期几 [1-7]: " WEEKDAY
        
        echo -e "${YELLOW}请输入运行时间 (格式: HH:MM，例如: 09:30):${NC}"
        read -p "时间: " WEEKLY_TIME
        HOUR=$(echo $WEEKLY_TIME | cut -d':' -f1)
        MINUTE=$(echo $WEEKLY_TIME | cut -d':' -f2)
        
        CRON_EXPR="$MINUTE $HOUR * * $WEEKDAY"
        
        case $WEEKDAY in
            1) DAY_DESC="星期一";;
            2) DAY_DESC="星期二";;
            3) DAY_DESC="星期三";;
            4) DAY_DESC="星期四";;
            5) DAY_DESC="星期五";;
            6) DAY_DESC="星期六";;
            7) DAY_DESC="星期日";;
        esac
        
        CRON_DESC="每周$DAY_DESC $WEEKLY_TIME"
        ;;
    3)
        echo -e "${YELLOW}请输入自定义cron表达式 (格式: 分 时 日 月 星期):${NC}"
        echo "例如: 30 9 * * 1-5 (工作日上午9:30运行)"
        read -p "cron表达式: " CRON_EXPR
        CRON_DESC="自定义: $CRON_EXPR"
        ;;
    *)
        echo -e "${RED}无效选项，使用默认设置: 每天上午9:30${NC}"
        CRON_EXPR="30 9 * * *"
        CRON_DESC="每天 09:30"
        ;;
esac

# 创建临时crontab文件
TEMP_CRONTAB=$(mktemp)
crontab -l > "$TEMP_CRONTAB" 2>/dev/null || echo "" > "$TEMP_CRONTAB"

# 检查是否已存在相同任务
if grep -q "$RUN_SCRIPT" "$TEMP_CRONTAB"; then
    echo -e "${YELLOW}发现已存在的定时任务，将被替换${NC}"
    sed -i '' "\|$RUN_SCRIPT|d" "$TEMP_CRONTAB"
fi

# 添加新的cron任务
echo "# Qwen-Max到小红书自动化脚本 - $CRON_DESC" >> "$TEMP_CRONTAB"
echo "$CRON_EXPR $RUN_SCRIPT" >> "$TEMP_CRONTAB"

# 应用新的crontab
crontab "$TEMP_CRONTAB"
rm "$TEMP_CRONTAB"

echo -e "${GREEN}cron任务已设置: $CRON_DESC${NC}"
echo ""

# 创建手动运行脚本
MANUAL_SCRIPT="$SCRIPT_DIR/run_now.sh"

cat > "$MANUAL_SCRIPT" << EOL
#!/bin/bash
# 立即运行Qwen-Max到小红书自动化脚本

# 获取脚本所在目录
SCRIPT_DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"

# 运行自动化脚本
"\$SCRIPT_DIR/run_automation.sh"

echo "脚本已运行，请查看日志目录获取详细信息"
EOL

# 设置执行权限
chmod +x "$MANUAL_SCRIPT"
echo -e "${GREEN}手动运行脚本已创建: $MANUAL_SCRIPT${NC}"

# 创建查看cron状态的脚本
STATUS_SCRIPT="$SCRIPT_DIR/check_status.sh"

cat > "$STATUS_SCRIPT" << EOL
#!/bin/bash
# 检查Qwen-Max到小红书自动化脚本的cron状态

# 获取脚本所在目录
SCRIPT_DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
PARENT_DIR="\$(dirname "\$SCRIPT_DIR")"

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

echo -e "\${YELLOW}===== Qwen-Max到小红书自动化脚本 - 状态检查 =====${NC}"
echo ""

# 检查cron任务
echo -e "\${YELLOW}当前cron任务:${NC}"
crontab -l | grep -A 1 "Qwen-Max到小红书自动化脚本" || echo -e "\${RED}未找到相关cron任务${NC}"

echo ""

# 检查最近的日志
echo -e "\${YELLOW}最近的运行日志:${NC}"
LOG_DIR="\$PARENT_DIR/logs"
if [ -d "\$LOG_DIR" ]; then
    LATEST_LOG=\$(ls -t "\$LOG_DIR"/cron_run_*.log 2>/dev/null | head -n 1)
    if [ -n "\$LATEST_LOG" ]; then
        echo -e "\${GREEN}最新日志文件: \$LATEST_LOG${NC}"
        echo ""
        echo "日志内容 (最后10行):"
        tail -n 10 "\$LATEST_LOG"
    else
        echo -e "\${RED}未找到日志文件${NC}"
    fi
else
    echo -e "\${RED}日志目录不存在${NC}"
fi

echo ""
echo -e "\${YELLOW}下次运行时间预估:${NC}"
NEXT_RUN=\$(crontab -l | grep -A 1 "Qwen-Max到小红书自动化脚本" | tail -n 1 | awk '{print \$1,\$2,\$3,\$4,\$5}')
if [ -n "\$NEXT_RUN" ]; then
    # 尝试使用cronexpr计算下次运行时间
    if command -v python3 &> /dev/null && python3 -c "import croniter" 2>/dev/null; then
        NEXT_TIME=\$(python3 -c "from croniter import croniter; from datetime import datetime; print(croniter('\$NEXT_RUN', datetime.now()).get_next(datetime).strftime('%Y-%m-%d %H:%M:%S'))")
        echo -e "\${GREEN}下次运行时间: \$NEXT_TIME${NC}"
    else
        echo -e "\${YELLOW}cron表达式: \$NEXT_RUN${NC}"
        echo -e "\${YELLOW}(安装python croniter包可显示精确时间)${NC}"
    fi
else
    echo -e "\${RED}无法确定下次运行时间${NC}"
fi
EOL

# 设置执行权限
chmod +x "$STATUS_SCRIPT"
echo -e "${GREEN}状态检查脚本已创建: $STATUS_SCRIPT${NC}"

# 创建移除cron任务的脚本
REMOVE_SCRIPT="$SCRIPT_DIR/remove_cron.sh"

cat > "$REMOVE_SCRIPT" << EOL
#!/bin/bash
# 移除Qwen-Max到小红书自动化脚本的cron任务

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

echo -e "\${YELLOW}===== 移除Qwen-Max到小红书自动化脚本的cron任务 =====${NC}"
echo ""

# 创建临时crontab文件
TEMP_CRONTAB=\$(mktemp)
crontab -l > "\$TEMP_CRONTAB" 2>/dev/null || echo "" > "\$TEMP_CRONTAB"

# 检查是否存在相关任务
if grep -q "Qwen-Max到小红书自动化脚本" "\$TEMP_CRONTAB"; then
    # 显示将被移除的任务
    echo -e "\${YELLOW}以下任务将被移除:${NC}"
    grep -A 1 "Qwen-Max到小红书自动化脚本" "\$TEMP_CRONTAB"
    echo ""
    
    # 确认移除
    read -p "确认移除这些任务? (y/n): " CONFIRM
    if [[ \$CONFIRM =~ ^[Yy] ]]; then
        # 移除相关任务
        sed -i '' "/Qwen-Max到小红书自动化脚本/,+1d" "\$TEMP_CRONTAB"
        
        # 应用新的crontab
        crontab "\$TEMP_CRONTAB"
        echo -e "\${GREEN}cron任务已成功移除${NC}"
    else
        echo -e "\${YELLOW}操作已取消${NC}"
    fi
else
    echo -e "\${RED}未找到相关cron任务${NC}"
fi

# 清理临时文件
rm "\$TEMP_CRONTAB"
EOL

# 设置执行权限
chmod +x "$REMOVE_SCRIPT"
echo -e "${GREEN}移除脚本已创建: $REMOVE_SCRIPT${NC}"

echo ""
echo -e "${GREEN}===== 设置完成 =====${NC}"
echo ""
echo -e "您可以使用以下脚本管理自动化任务:"
echo -e "- ${YELLOW}$MANUAL_SCRIPT${NC}: 立即运行一次自动化脚本"
echo -e "- ${YELLOW}$STATUS_SCRIPT${NC}: 检查cron任务状态和最近的运行日志"
echo -e "- ${YELLOW}$REMOVE_SCRIPT${NC}: 移除cron任务"
echo ""
echo -e "当前cron设置: ${GREEN}$CRON_DESC${NC}"
echo -e "脚本将按照设定的时间自动运行，无需手动干预"
echo ""
echo -e "${YELLOW}注意: 请确保您的Mac在设定的时间是开机状态，否则任务将不会执行${NC}"
echo -e "${YELLOW}如果您的Mac经常休眠，可以考虑使用launchd代替cron${NC}"
