#!/bin/bash

echo "🚀 开始部署海鸥表展示应用到Gitee Pages..."

# 检查环境
echo "📋 检查环境依赖..."
node --version
npm --version

# 安装依赖
echo "📦 安装项目依赖..."
npm ci

# 构建项目
echo "🏗️ 构建生产版本..."
npm run build

# 检查构建结果
if [ -d "dist" ]; then
    echo "✅ 构建成功！输出文件在 dist/ 目录"
    echo "📁 构建文件列表："
    ls -la dist/
else
    echo "❌ 构建失败！"
    exit 1
fi

echo "🎉 部署准备完成！"
echo "📌 下一步：将 dist/ 目录内容推送到 Gitee Pages"
echo "🌐 访问地址：https://derekzhou79.gitee.io/luxury-watch-emporium" 