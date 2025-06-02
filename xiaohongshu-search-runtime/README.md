# 小红书热门笔记查询系统

这是一个用于查询小红书热门笔记的Web应用，包含前端界面和Python后端API。

## 🆕 最新更新 (v2.1)

**搜索和截图逻辑大幅优化** - 解决"页面不见了"问题：

- ✅ **智能等待机制**：使用WebDriverWait替代简单sleep，提升页面加载稳定性
- ✅ **页面错误检测**：自动识别"你访问页面不见了"、反爬虫验证等异常状态
- ✅ **自动恢复策略**：检测到页面错误时自动回到首页重新访问
- ✅ **改进的反爬虫处理**：支持ESC键、关闭按钮等多种弹窗处理方式
- ✅ **人性化浏览行为**：模拟真实用户的随机滚动和等待时间
- ✅ **更强的元素选择器**：适配最新版小红书页面结构变化
- ✅ **智能截图时机**：成功搜索后再截图，避免截取错误页面
- ✅ **详细错误分析**：保存错误页面截图和源码，便于问题诊断
- ✅ **优先级策略**：优先使用explore链接，确保笔记ID准确性

**测试工具**：
```bash
# 测试改进后的搜索功能
python test_search_improved.py
```

## 功能特点

- 🔍 实时搜索小红书热门笔记
- 🔐 自动登录获取最新cookies，无需手动管理登录状态
- 📊 展示笔记详情、点赞数、评论数等信息
- 📈 支持按热门程度排序
- 📱 响应式设计，适配移动端和桌面端
- 💾 数据缓存机制，减少重复请求
- 🛠️ 完善的错误处理和日志记录

## 技术栈

- **前端**：HTML5、CSS3、JavaScript
- **后端**：Python、Flask
- **爬虫**：Selenium、BeautifulSoup、Requests
- **数据存储**：JSON文件缓存

## 环境要求

- Python 3.7+
- Chrome浏览器
- ChromeDriver（程序会自动下载配置）

## 快速启动

### 方法一：使用启动脚本（推荐）

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### 方法二：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务（会自动打开浏览器进行登录）
python main.py

# 或者直接启动Flask应用
python app.py
```

## 使用流程

1. **运行启动脚本**：执行 `./start.sh` 或 `start.bat`
2. **自动登录**：程序会自动打开Chrome浏览器
3. **完成登录**：在浏览器中登录小红书账号（支持扫码登录或手机号+密码登录）
4. **服务启动**：登录成功后，浏览器会自动关闭，服务启动
5. **开始使用**：访问 http://localhost:8080 使用搜索功能

## 项目结构

```
xiaohongshu-search-runtime/
├── main.py                 # 主启动程序
├── app.py                  # Flask后端服务
├── crawler.py              # 爬虫模块
├── cookie_manager.py       # Cookie管理工具
├── cookie_tester.py        # Cookie测试工具
├── setup_webdriver.py      # WebDriver设置工具
├── start.sh                # Linux/Mac启动脚本
├── start.bat               # Windows启动脚本
├── index.html              # 前端主页面
├── css/                    # CSS样式文件
│   └── style.css
├── js/                     # JavaScript文件
│   ├── api.js
│   └── script.js
├── img/                    # 图片资源目录
├── cache/                  # 数据缓存目录
├── drivers/                # WebDriver目录
├── venv/                   # Python虚拟环境
├── requirements.txt        # Python依赖列表
├── webdriver_path.txt      # WebDriver路径配置
└── README.md               # 项目说明文档
```

## 工具使用说明

### Cookie管理工具

```bash
# 登录并保存Cookie
python cookie_manager.py login

# 验证Cookie有效性
python cookie_manager.py verify

# 删除Cookie文件
python cookie_manager.py delete

# 查看Cookie信息
python cookie_manager.py info
```

### Cookie测试工具

```bash
# 测试Cookie（显示浏览器）
python cookie_tester.py

# 测试Cookie（无头模式）
python cookie_tester.py --headless
```

## API接口说明

### 1. 搜索笔记

- **URL**: `/api/search`
- **方法**: GET
- **参数**:
  - `keyword`: 搜索关键词（必填）
  - `max_results`: 最大结果数量（可选，默认10）
  - `use_cache`: 是否使用缓存（可选，默认true）

**返回示例**:
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

1. **ChromeDriver错误**：
   ```bash
   python setup_webdriver.py
   ```

2. **登录失败**：
   - 确保网络连接正常
   - 尝试关闭代理软件
   - 清理缓存后重新启动
   - 使用Cookie管理工具重新登录：
     ```bash
     python cookie_manager.py login
     ```

3. **端口占用**：
   ```bash
   # 查看8080端口占用
   lsof -i:8080
   # 强制停止占用进程
   sudo kill -9 $(lsof -ti:8080)
   ```

4. **搜索无结果**：
   - 检查登录状态是否有效：
     ```bash
     python cookie_tester.py
     ```
   - 访问 `/login` 重新登录
   - 重启程序

5. **Cookie失效**：
   ```bash
   # 验证Cookie状态
   python cookie_tester.py
   
   # 重新获取Cookie
   python cookie_manager.py login
   ```

### 日志查看

程序运行时会输出详细的日志信息，包括：
- 初始化状态
- 登录过程
- 搜索请求
- 错误信息

## 开发说明

### 文件说明

- `main.py`: 主启动程序，负责初始化和启动服务
- `app.py`: Flask Web应用，提供API接口
- `crawler.py`: 爬虫核心模块，处理数据抓取
- `cookie_manager.py`: Cookie管理工具，支持登录、验证、删除等操作
- `cookie_tester.py`: Cookie测试工具，验证登录状态
- `setup_webdriver.py`: WebDriver自动配置工具

### 代码特点

- 🔧 模块化设计，职责分离
- 🛡️ 完善的错误处理机制
- 📝 详细的日志记录
- 🎨 用户友好的界面提示
- 🔄 自动重试和恢复机制

## 注意事项

1. **合规使用**：本项目仅供学习研究使用，请遵守小红书使用条款
2. **登录安全**：建议使用测试账号，避免使用主要账号
3. **请求频率**：合理控制搜索频率，避免触发反爬虫机制
4. **数据保护**：cookies文件包含登录信息，请妥善保管
5. **版本兼容**：确保Chrome浏览器版本与ChromeDriver版本兼容

## 更新日志

### v2.0
- 重构代码结构，提高可维护性
- 新增Cookie管理工具
- 新增Cookie测试工具
- 改进错误处理和日志记录
- 优化启动脚本
- 更新文档说明

### v1.0
- 基础功能实现
- 支持搜索和详情查看
- 自动登录功能

## 许可证

MIT License 