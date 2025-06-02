# 小红书搜索工具

一个简单易用的小红书笔记搜索工具，支持关键词搜索和笔记详情获取。

## 🌟 功能特点

- 🔍 关键词搜索小红书笔记
- 📱 现代化的Web界面
- 🚀 自动WebDriver管理
- 💾 搜索结果缓存
- 🔐 Cookie登录支持
- 📁 清晰的文件结构组织

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- Chrome浏览器
- macOS/Linux/Windows

### 2. 安装依赖

```bash
# 克隆项目
git clone <项目地址>
cd xiaohongshu-search

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r config/requirements.txt
```

### 3. 启动服务

```bash
# 方式1：使用启动脚本（推荐）
chmod +x scripts/run_server.sh
./scripts/run_server.sh

# 方式2：直接运行主启动文件
python app.py

# 方式3：运行服务器模块
python src/server/main_server.py
```

### 4. 访问应用

打开浏览器访问：http://localhost:8080

## 📁 项目结构

```
xiaohongshu-search/
├── app.py                          # 主启动文件
├── src/                            # 源代码目录
│   ├── server/                     # 服务器模块
│   │   └── main_server.py          # Flask主服务器
│   ├── crawler/                    # 爬虫模块
│   │   └── xiaohongshu_crawler.py  # 小红书爬虫核心
│   └── utils/                      # 工具模块
│       ├── login_helper.py         # 登录辅助工具
│       └── cookie_manager.py       # Cookie管理工具
├── static/                         # 静态文件目录
│   ├── index.html                  # 主页面
│   ├── css/                        # 样式文件
│   │   └── style.css               # 主样式文件
│   ├── js/                         # JavaScript文件
│   │   ├── api.js                  # API调用模块
│   │   └── script.js               # 前端交互逻辑
│   └── images/                     # 图片资源目录
├── config/                         # 配置文件目录
│   └── requirements.txt            # 依赖文件
├── scripts/                        # 脚本目录
│   └── run_server.sh              # 启动脚本
├── docs/                          # 文档目录
│   └── README.md                  # 项目文档
├── cache/                         # 缓存目录
│   ├── cookies/                   # Cookie存储
│   ├── temp/                      # 临时文件
│   └── logs/                      # 日志文件
├── drivers/                       # WebDriver目录
└── venv/                         # 虚拟环境目录
```

## 📖 使用说明

### 首次使用

1. 运行启动脚本：`./scripts/run_server.sh`
2. 选择登录方式（推荐选择1）
3. 在打开的浏览器中登录小红书
4. 登录成功后，服务自动启动

### 搜索笔记

1. 在搜索框输入关键词
2. 点击搜索按钮
3. 查看搜索结果

### API接口

- `GET /api/search?keyword=关键词` - 搜索笔记
- `GET /api/note/<note_id>` - 获取笔记详情
- `GET /api/hot-keywords` - 获取热门关键词

## ⚙️ 配置说明

### Cookie配置

Cookie文件保存在 `cache/cookies/xiaohongshu_cookies.json`，用于免登录访问。

### 缓存配置

- 搜索结果缓存：`cache/temp/`
- 日志文件：`cache/logs/`
- 缓存时间：1小时

### 静态文件

- HTML文件：`static/index.html`
- CSS样式：`static/css/style.css`
- JavaScript：`static/js/`
- 图片资源：`static/images/`

## 🔧 故障排除

### Chrome浏览器问题

确保已安装Chrome浏览器，WebDriver会自动下载和配置。

### 端口占用

如果8080端口被占用，启动脚本会自动处理。

### 搜索无结果

1. 检查网络连接
2. 尝试重新登录：访问 http://localhost:8080/login
3. 清理缓存文件：`rm -rf cache/temp/*`

### 文件路径问题

如果遇到导入错误，确保从项目根目录运行：
```bash
cd xiaohongshu-search
python app.py
```

## 🛠️ 开发说明

### 添加新功能

1. 服务器功能：在 `src/server/` 目录下添加
2. 爬虫功能：在 `src/crawler/` 目录下添加
3. 工具函数：在 `src/utils/` 目录下添加

### 静态资源

1. CSS文件：放在 `static/css/` 目录
2. JavaScript文件：放在 `static/js/` 目录
3. 图片文件：放在 `static/images/` 目录

### 配置文件

1. 依赖管理：`config/requirements.txt`
2. 启动脚本：`scripts/run_server.sh`

## ⚠️ 注意事项

- 本工具仅供学习研究使用
- 请遵守小红书的使用条款
- 避免频繁请求，以免被限制访问
- 建议使用代理以提高稳定性

## 🔧 技术栈

- **后端**: Python Flask
- **前端**: HTML + CSS + JavaScript
- **爬虫**: Selenium + BeautifulSoup
- **WebDriver**: Chrome + webdriver-manager

## 📝 更新日志

### v2.1.0 (当前版本)
- 重构项目文件结构
- 按文件类型分类组织
- 优化启动方式
- 改进缓存管理
- 增强错误处理

### v2.0.0
- 重构代码结构
- 优化文件命名
- 简化启动流程
- 改进错误处理
- 添加自动WebDriver管理

## �� 许可证

MIT License 