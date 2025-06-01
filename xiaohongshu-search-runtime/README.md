# 小红书热门笔记查询系统

这是一个用于查询小红书热门笔记的Web应用，包含前端界面和Python后端API。

## 功能特点

- 实时搜索小红书热门笔记
- 自动登录获取最新cookies，无需手动管理登录状态
- 展示笔记详情、点赞数、评论数等信息
- 支持按热门程度排序
- 响应式设计，适配移动端和桌面端
- 数据缓存机制，减少重复请求

## 技术栈

- **前端**：HTML5、CSS3、JavaScript
- **后端**：Python、Flask
- **爬虫**：Selenium、BeautifulSoup、Requests

## 安装与使用

### 环境要求

- Python 3.7+
- Chrome浏览器
- ChromeDriver（程序会自动下载配置）

### 快速启动

1. **使用启动脚本（推荐）**：
   ```bash
   # Linux/Mac
   ./start.sh
   
   # Windows
   start.bat
   ```

2. **手动启动**：
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 启动服务（会自动打开浏览器进行登录）
   python start_app.py
   
   # 或者使用原始方式
   python app.py
   ```

### 使用流程

1. 运行启动脚本或启动程序
2. **程序会自动打开Chrome浏览器**
3. **在浏览器中登录小红书账号**（支持扫码登录或手机号+密码登录）
4. 登录成功后，浏览器会自动关闭，服务启动
5. 访问 http://localhost:8080 使用搜索功能

### 重要说明

- **每次启动都会重新登录**：确保获取最新的有效cookies
- **支持多种登录方式**：扫码登录、手机号+密码、短信验证码等
- **自动保存登录状态**：登录成功后会保存cookies供后续使用
- **无头模式运行**：登录完成后，爬虫在后台无界面运行

## 项目结构

```
xiaohongshu-search-runtime/
├── app.py              # Flask后端服务
├── start_app.py        # 简化启动脚本
├── crawler.py          # 爬虫模块
├── get_cookies.py      # 独立登录工具
├── start.sh            # Linux/Mac启动脚本
├── start.bat           # Windows启动脚本
├── index.html          # 前端主页面
├── css/                # CSS样式文件
├── js/                 # JavaScript文件
├── img/                # 图片资源目录
├── cache/              # 数据缓存目录
├── drivers/            # WebDriver目录
├── venv/               # Python虚拟环境
└── requirements.txt    # Python依赖列表
```

## API接口说明

### 1. 搜索笔记

- **URL**: `/api/search`
- **方法**: GET
- **参数**:
  - `keyword`: 搜索关键词（必填）
  - `max_results`: 最大结果数量（可选，默认10）
  - `use_cache`: 是否使用缓存（可选，默认true）
- **返回示例**:
  ```json
  {
    "keyword": "口红",
    "timestamp": 1637123456,
    "count": 10,
    "notes": [
      {
        "id": "note_123456",
        "title": "口红推荐",
        "desc": "最近入手了这款口红，真的太好用了！推荐给大家～",
        "author": "美妆达人",
        "avatar": "https://...",
        "cover": "https://...",
        "likes": 8765,
        "comments": 432,
        "collects": 1234,
        "shares": 56,
        "published": "2023-01-15",
        "content": "...",
        "images": ["https://...", "https://..."]
      }
    ]
  }
  ```

### 2. 获取笔记详情

- **URL**: `/api/note/<note_id>`
- **方法**: GET

### 3. 获取热门关键词

- **URL**: `/api/hot-keywords`
- **方法**: GET

### 4. 重新登录

- **URL**: `/login`
- **方法**: GET
- **说明**: 如果登录状态失效，可访问此地址重新登录

## 故障排除

### 常见问题

1. **ChromeDriver错误**：程序会自动下载配置，如有问题请手动运行：
   ```bash
   python setup_webdriver.py
   ```

2. **登录失败**：
   - 确保网络连接正常
   - 尝试关闭代理软件
   - 清理缓存后重新启动

3. **端口占用**：
   ```bash
   # 查看8080端口占用
   lsof -i:8080
   # 强制停止占用进程
   sudo kill -9 $(lsof -ti:8080)
   ```

4. **搜索无结果**：
   - 检查登录状态是否有效
   - 访问 `/login` 重新登录
   - 重启程序

## 注意事项

1. **合规使用**：本项目仅供学习研究使用，请遵守小红书使用条款
2. **登录安全**：建议使用测试账号，避免使用主要账号
3. **请求频率**：合理控制搜索频率，避免触发反爬虫机制
4. **数据保护**：cookies文件包含登录信息，请妥善保管

## 许可证

MIT License 