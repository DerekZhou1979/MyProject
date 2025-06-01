# Qwen-Max到小红书自动化脚本使用说明

## 项目简介

这是一个基于通义千问Qwen-Max大模型的自动化脚本，用于自动生成内容并发布到小红书平台。结合macOS的定时任务功能，可以实现完全自动化的内容创作和发布流程。

## 功能特点

- 自动从通义千问Qwen-Max获取生成的内容
- 支持自定义内容主题和轮换主题
- 自动发布内容到小红书平台
- 自动添加标签和免责声明
- 完整的日志记录和错误处理
- 灵活的配置选项
- macOS本地定时任务自动化

## 安装步骤

1. 确保已安装Python 3.6或更高版本
2. 解压下载的项目文件到本地
3. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
4. 安装Playwright浏览器：
   ```
   python -m playwright install chromium
   ```
5. 也可以直接运行初始化脚本自动完成环境配置：
   ```
   python src/init.py
   ```

## 配置说明

首次运行脚本时会自动创建默认配置文件`config.json`，您需要编辑此文件并填入必要的信息：

### Qwen-Max配置

```json
"qwen": {
    "api_key": "您的通义千问API密钥",
    "model": "qwen-max",
    "temperature": 0.7,
    "max_tokens": 2000,
    "prompt_template": "请生成一篇适合小红书平台的内容，主题是：{topic}。内容应该包括标题、正文和5个合适的标签。"
}
```

- `api_key`: 您的通义千问API密钥，必须填写
- `model`: 使用的模型，建议使用qwen-max
- `temperature`: 生成内容的创造性，值越高创造性越强
- `max_tokens`: 生成内容的最大长度
- `prompt_template`: 提示词模板，{topic}会被替换为实际主题

### 小红书配置

```json
"xiaohongshu": {
    "cookie": "您的小红书Cookie",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "auto_add_tags": true,
    "default_tags": ["AI创作", "每日分享", "生活记录"]
}
```

- `cookie`: 您的小红书Cookie，必须填写
- `user_agent`: 浏览器User-Agent
- `auto_add_tags`: 是否自动添加标签
- `default_tags`: 默认标签列表

### 内容配置

```json
"content": {
    "topics": ["生活小窍门", "美食推荐", "旅行攻略", "读书笔记", "职场技巧"],
    "current_topic_index": 0,
    "rotate_topics": true,
    "add_disclaimer": true,
    "disclaimer_text": "本内容由AI辅助创作，仅供参考。"
}
```

- `topics`: 内容主题列表
- `current_topic_index`: 当前主题索引
- `rotate_topics`: 是否轮换主题
- `add_disclaimer`: 是否添加免责声明
- `disclaimer_text`: 免责声明文本

### 运行配置

```json
"runtime": {
    "log_level": "INFO",
    "save_content": true,
    "content_dir": "contents",
    "max_retries": 3,
    "retry_delay": 5
}
```

- `log_level`: 日志级别
- `save_content`: 是否保存生成的内容
- `content_dir`: 内容保存目录
- `max_retries`: 最大重试次数
- `retry_delay`: 重试延迟（秒）

## 使用方法

### 基本用法

```
python src/main.py
```

这将使用配置文件中的设置生成内容并发布到小红书。

### 高级用法

```
python src/main.py --topic "健康生活" --log-level DEBUG
```

命令行参数：

- `--config`: 指定配置文件路径
- `--topic`: 指定内容主题，覆盖配置文件中的设置
- `--check-only`: 仅检查配置和登录状态，不执行发布
- `--generate-only`: 仅生成内容，不执行发布
- `--log-level`: 日志级别

## macOS定时任务设置

### 设置步骤

1. 打开终端，进入项目目录下的`macos_scheduler`文件夹
2. 运行验证脚本检查环境：
   ```
   chmod +x validate_setup.sh
   ./validate_setup.sh
   ```
3. 运行设置脚本并按照提示操作：
   ```
   chmod +x setup_cron.sh
   ./setup_cron.sh
   ```

### 定时选项

设置过程中，您可以选择：
- 每天运行一次（指定时间）
- 每周运行一次（指定星期几和时间）
- 自定义cron表达式（适合高级用户）

### 管理定时任务

设置完成后，您可以使用以下脚本管理定时任务：

- **立即运行一次**:
  ```bash
  ./run_now.sh
  ```

- **检查任务状态和日志**:
  ```bash
  ./check_status.sh
  ```

- **移除定时任务**:
  ```bash
  ./remove_cron.sh
  ```

## 获取小红书Cookie

1. 使用Chrome浏览器登录小红书网页版
2. 按F12打开开发者工具
3. 切换到"网络"(Network)标签
4. 刷新页面
5. 点击任意一个请求
6. 在请求头(Headers)中找到"Cookie"字段
7. 复制完整的Cookie值并填入配置文件

## 获取通义千问API密钥

1. 访问通义千问开放平台：https://dashscope.aliyun.com/
2. 注册并登录您的账号
3. 在控制台中找到"API密钥管理"
4. 创建或查看您的API密钥
5. 复制API密钥并填入配置文件

## 常见问题

1. **API密钥无效**
   - 确保您的通义千问API密钥正确且有效
   - 检查API密钥是否有足够的额度

2. **小红书登录失败**
   - Cookie可能已过期，请重新获取
   - 确保Cookie包含完整的登录信息

3. **发布内容失败**
   - 检查网络连接
   - 查看日志文件了解详细错误信息
   - 小红书可能有发布频率限制，尝试减少发布频率

4. **Playwright浏览器问题**
   - 确保已正确安装Playwright：`playwright install chromium`
   - 如果在无头服务器上运行，可能需要安装额外依赖：`apt-get install -y libgbm-dev`

5. **定时任务未运行**
   - 确保Mac在设定时间处于开机状态
   - 检查cron服务是否正常运行
   - 使用`check_status.sh`脚本查看任务状态

## 注意事项

- 请遵守通义千问和小红书的使用条款
- 不要过于频繁地发布内容，以免被平台限制
- 定期更新Cookie以确保登录状态
- 生成的内容质量取决于Qwen-Max模型和提示词设计
- 确保Mac在设定的时间是开机状态，否则任务将不会执行

## 日志和调试

日志文件保存在`logs`目录下，格式为`run_YYYYMMDD_HHMMSS.log`。如果遇到问题，请查看日志文件了解详细信息。

## 项目结构

```
qwen_xiaohongshu_agent/
├── config.json           # 配置文件
├── requirements.txt      # 依赖包列表
├── contents/             # 生成的内容保存目录
├── logs/                 # 日志目录
├── src/                  # 源代码目录
│   ├── __init__.py       # 包初始化文件
│   ├── config.py         # 配置模块
│   ├── qwen.py           # Qwen-Max内容获取模块
│   ├── xiaohongshu.py    # 小红书发布模块
│   ├── main.py           # 主程序
│   └── init.py           # 初始化脚本
└── macos_scheduler/      # macOS定时任务脚本
    ├── setup_cron.sh     # 设置定时任务脚本
    ├── validate_setup.sh # 验证环境脚本
    ├── run_now.sh        # 立即运行脚本(自动生成)
    ├── check_status.sh   # 检查状态脚本(自动生成)
    └── remove_cron.sh    # 移除任务脚本(自动生成)
```
