# 🚀 海鸥表展示应用部署指南

## 📋 部署前准备

### 环境要求
- **Node.js**: >= 18.0.0
- **npm**: >= 8.0.0
- **Gitee账号**: 用于代码托管和Pages服务

### 项目依赖
```json
"dependencies": {
  "@google/genai": "^1.3.0",
  "react": "^19.1.0", 
  "react-dom": "^19.1.0",
  "react-router-dom": "^7.6.2"
}
```

## 🌐 方案一：Gitee Pages部署 (推荐)

### 1. 代码准备
```bash
# 克隆项目到本地
git clone <your-repo-url>
cd luxury-watch-emporium

# 安装依赖
npm install

# 本地测试
npm run dev
```

### 2. Gitee仓库设置
1. 登录 [Gitee](https://gitee.com)
2. 创建新仓库 `luxury-watch-emporium`
3. 将代码推送到Gitee：
   ```bash
   git remote add origin https://gitee.com/你的用户名/luxury-watch-emporium.git
   git push -u origin main
   ```

### 3. 构建和部署
```bash
# 使用自动化部署脚本
chmod +x deploy.sh
./deploy.sh

# 或手动构建
npm run build
```

### 4. 开启Gitee Pages
1. 进入仓库设置页面
2. 找到 "Pages" 选项
3. 选择部署分支为 `main`
4. 部署目录选择 `dist`
5. 点击启动服务

### 5. 访问应用
- **访问地址**: `https://你的用户名.gitee.io/luxury-watch-emporium`
- **更新部署**: 推送代码后，Gitee Pages会自动更新

## 🌐 方案二：Vercel部署 (国际化)

### 1. 连接GitHub/Gitee
1. 访问 [Vercel](https://vercel.com)
2. 导入Git仓库
3. 配置构建设置：
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 2. 环境变量配置
在Vercel项目设置中添加：
```
GEMINI_API_KEY=your_api_key_here
```

## 🌐 方案三：腾讯云开发部署

### 1. 安装CloudBase CLI
```bash
npm install -g @cloudbase/cli
```

### 2. 登录腾讯云
```bash
cloudbase login
```

### 3. 部署配置
创建 `cloudbaserc.json`:
```json
{
  "envId": "your-env-id",
  "framework": {
    "name": "vue",
    "plugins": {
      "client": {
        "use": "@cloudbase/framework-plugin-website",
        "inputs": {
          "buildCommand": "npm run build",
          "outputPath": "dist"
        }
      }
    }
  }
}
```

### 4. 部署
```bash
cloudbase framework:deploy
```

## 🛠️ 部署优化建议

### 1. 资源优化
- 图片压缩：使用webp格式
- 代码分割：利用Vite的自动分割
- CDN加速：配置静态资源CDN

### 2. SEO优化
```html
<!-- 在index.html中添加 -->
<meta name="description" content="海鸥表官方展示应用，中国制表行业领先品牌">
<meta name="keywords" content="海鸥表,中国制表,腕表,手表">
```

### 3. 性能监控
- 配置Google Analytics
- 使用Lighthouse检测性能
- 设置错误监控

## 🔧 常见问题解决

### 路由问题
如果使用React Router，需要在静态托管平台配置回退：
```
# _redirects 文件
/*    /index.html   200
```

### API密钥安全
- 开发环境：使用 `.env.local`
- 生产环境：使用平台环境变量

### 图片资源
确保所有图片路径使用相对路径：
```javascript
// 正确
<img src="./images/watch1.jpg" />

// 错误
<img src="/images/watch1.jpg" />
```

## 📊 部署后验证

### 功能测试清单
- [ ] 首页正常加载
- [ ] 产品列表显示
- [ ] 购物车功能
- [ ] 路由跳转
- [ ] 移动端适配
- [ ] 图片加载
- [ ] AI功能 (如配置)

### 性能指标
- **LCP** (最大内容绘制): < 2.5s
- **FID** (首次输入延迟): < 100ms  
- **CLS** (累积布局偏移): < 0.1

---

**部署成功后，您的海鸥表展示应用将在公网上为用户提供优质的浏览体验！** 🎉 