#!/bin/bash

echo "🎯 海鸥表展示应用 - Gitee Pages 一键部署"
echo "================================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Node.js环境
echo -e "${YELLOW}📋 检查环境...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js 未安装！请先安装 Node.js 18+${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm 未安装！${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js 版本: $(node --version)${NC}"
echo -e "${GREEN}✅ npm 版本: $(npm --version)${NC}"

# 安装依赖
echo -e "${YELLOW}📦 安装项目依赖...${NC}"
npm ci || {
    echo -e "${RED}❌ 依赖安装失败！${NC}"
    exit 1
}

# 构建项目
echo -e "${YELLOW}🏗️ 构建生产版本...${NC}"
npm run build || {
    echo -e "${RED}❌ 构建失败！${NC}"
    exit 1
}

# 检查构建结果
if [ -d "dist" ]; then
    echo -e "${GREEN}✅ 构建成功！${NC}"
    echo -e "${YELLOW}📁 构建文件：${NC}"
    ls -la dist/
    echo ""
    
    # 检查关键文件
    if [ -f "dist/index.html" ]; then
        echo -e "${GREEN}✅ index.html 存在${NC}"
    else
        echo -e "${RED}❌ index.html 缺失！${NC}"
    fi
    
    if [ -d "dist/assets" ]; then
        echo -e "${GREEN}✅ assets 目录存在${NC}"
    else
        echo -e "${YELLOW}⚠️ assets 目录不存在${NC}"
    fi
else
    echo -e "${RED}❌ 构建失败！dist 目录不存在${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 构建完成！${NC}"
echo -e "${YELLOW}📋 下一步部署指南：${NC}"
echo ""
echo "1. 🌐 登录 Gitee: https://gitee.com"
echo "2. 📁 创建仓库 'luxury-watch-emporium'"
echo "3. 📤 推送代码："
echo "   git add ."
echo "   git commit -m 'Deploy seagull watch emporium'"
echo "   git remote add origin https://gitee.com/derekzhou79/luxury-watch-emporium.git"
echo "   git push -u origin main"
echo ""
echo "4. ⚙️ 在Gitee仓库设置中："
echo "   - 找到 'Pages' 选项"
echo "   - 部署分支选择：main"
echo "   - 部署目录选择：dist"
echo "   - 点击启动服务"
echo ""
echo -e "${GREEN}🌐 部署后访问：https://derekzhou79.gitee.io/luxury-watch-emporium${NC}"
echo ""
echo -e "${YELLOW}💡 提示：每次代码更新后，重新运行此脚本并推送即可更新网站${NC}" 