# 小红书热门笔记查询系统

这是一个用于查询小红书热门笔记的Web应用，包含前端界面和Python后端API。

## 功能特点

- 实时搜索小红书热门笔记
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
- Chrome浏览器（如使用Selenium模式）
- ChromeDriver（如使用Selenium模式）

### 安装依赖

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行应用

```bash
# 启动Flask服务器
python app.py
```

服务器默认运行在 http://localhost:8080

### 使用方法

1. 打开浏览器访问 http://localhost:8080
2. 在搜索框中输入关键词，如"口红"、"护肤品"等
3. 点击"搜索"按钮或按Enter键开始搜索
4. 查看搜索结果，点击笔记卡片可查看详情

## 项目结构

```
xiaohongshu-search/
├── app.py              # Flask后端服务
├── crawler.py          # 爬虫模块
├── index.html          # 前端主页面
├── css/                # CSS样式文件
│   └── style.css       # 主样式文件
├── js/                 # JavaScript文件
│   ├── api.js          # API调用模块
│   └── script.js       # 前端交互逻辑
├── img/                # 图片资源目录
├── cache/              # 数据缓存目录
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
      },
      // ...更多笔记
    ]
  }
  ```

### 2. 获取笔记详情

- **URL**: `/api/note/<note_id>`
- **方法**: GET
- **返回示例**:
  ```json
  {
    "note": {
      "id": "note_123456",
      "title": "口红推荐",
      "content": "<p>这是笔记的详细内容...</p>",
      "images": ["https://...", "https://..."],
      "author": "美妆达人",
      "published": "2023-01-15",
      "likes": 8765,
      "comments": 432,
      "collects": 1234,
      "shares": 56
    }
  }
  ```

### 3. 获取热门关键词

- **URL**: `/api/hot-keywords`
- **方法**: GET
- **返回示例**:
  ```json
  {
    "keywords": ["口红", "护肤品", "连衣裙", "耳机", "咖啡", "包包", "眼影", "防晒霜", "面膜", "香水"]
  }
  ```

## 注意事项

1. 本项目仅供学习研究使用，请遵守小红书的使用条款和相关法律法规
2. 默认使用Requests模式模拟数据，如需真实数据，请设置`use_selenium=True`并安装相关依赖
3. 频繁请求可能导致IP被封，建议合理控制请求频率
4. 数据缓存默认保存1小时，可在代码中调整

## 依赖列表

创建`requirements.txt`文件，包含以下依赖：

```
flask==2.0.1
flask-cors==3.0.10
requests==2.26.0
beautifulsoup4==4.10.0
selenium==4.1.0
fake-useragent==0.1.11
```

## 许可证

MIT License 