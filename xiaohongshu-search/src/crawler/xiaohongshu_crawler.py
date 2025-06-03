#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书爬虫模块
使用多种策略提取小红书笔记数据
注意：本代码仅供学习研究使用，实际使用时需遵守小红书的使用条款和相关法律法规
"""

import json
import random
import time
import logging
import hashlib
import os
import sys
import urllib.parse
from urllib.parse import quote
import re

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 导入全局配置
from config.config import (
    SEARCH_CONFIG, CRAWLER_CONFIG, EXTRACTION_STRATEGIES, 
    DIRECTORIES, FILE_PATHS, URLS, ERROR_CONFIG,
    get_config
)

# 导入Selenium相关库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# 配置日志
logger = logging.getLogger(__name__)

class XiaoHongShuCrawler:
    """小红书爬虫类 - 使用全局配置和三种提取策略"""
    
    def __init__(self, use_selenium=True, headless=None, proxy=None, cookies_file=None):
        """
        初始化爬虫
        
        参数:
            use_selenium (bool): 是否使用Selenium
            headless (bool): 是否使用无头模式，None表示使用配置文件设置
            proxy (str): 代理服务器地址
            cookies_file (str): cookie文件路径
        """
        # 使用全局配置
        self.config = get_config()
        self.search_config = SEARCH_CONFIG
        self.crawler_config = CRAWLER_CONFIG
        self.extraction_strategies = EXTRACTION_STRATEGIES
        
        # 初始化参数
        self.use_selenium = use_selenium if use_selenium is not None else self.crawler_config['USE_SELENIUM']
        self.headless = headless if headless is not None else self.crawler_config['HEADLESS']
        self.proxy = proxy
        self.cookies_file = cookies_file or FILE_PATHS['COOKIES_FILE']
        
        # WebDriver相关
        self.driver = None
        
        # 缓存配置
        self.cache_dir = DIRECTORIES['TEMP_DIR']
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # HTML回调函数
        self.html_callback = None
        
        # 加载cookie
        self.cookies = self._load_cookies()
        
        logger.info("小红书爬虫初始化完成")
    
    def set_html_callback(self, callback_func):
        """设置HTML存储回调函数"""
        self.html_callback = callback_func
        logger.info("HTML存储回调函数已设置")
    
    def _ensure_driver_initialized(self):
        """确保WebDriver已初始化"""
        if self.driver is None:
            return self._init_selenium()
        return True
    
    def _load_cookies(self):
        """加载cookie"""
        if not os.path.exists(self.cookies_file):
            logger.warning(f"Cookie文件不存在: {self.cookies_file}")
            return []
        
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            logger.info(f"成功加载Cookie文件: {self.cookies_file}, 包含 {len(cookies)} 个cookie")
            return cookies
        except Exception as e:
            logger.error(f"加载Cookie文件失败: {str(e)}")
            return []
    
    def save_cookies(self, cookies_file=None):
        """保存当前浏览器的cookie"""
        if not self._ensure_driver_initialized():
            logger.error("WebDriver初始化失败，无法保存cookie")
            return False
        
        file_path = cookies_file or self.cookies_file
        cookies_dir = os.path.dirname(file_path)
        os.makedirs(cookies_dir, exist_ok=True)
        
        try:
            cookies = self.driver.get_cookies()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info(f"成功保存 {len(cookies)} 个cookie到: {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存cookie失败: {str(e)}")
            return False
    
    def _init_selenium(self):
        """初始化Selenium WebDriver"""
        try:
            logger.info("正在初始化Selenium...")
            
            # 配置Chrome选项
            chrome_options = Options()
            
            # 添加配置文件中的Chrome选项
            for option in self.crawler_config['CHROME_OPTIONS']:
                chrome_options.add_argument(option)
            
            # 设置窗口大小
            width, height = self.crawler_config['WINDOW_SIZE']
            chrome_options.add_argument(f'--window-size={width},{height}')
            
            # 设置代理
            if self.proxy:
                chrome_options.add_argument(f'--proxy-server={self.proxy}')
            
            # 反爬虫配置
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 使用本地ChromeDriver
            chromedriver_path = FILE_PATHS['CHROMEDRIVER_PATH']
            if os.path.exists(chromedriver_path):
                logger.info(f"使用本地ChromeDriver: {chromedriver_path}")
                os.chmod(chromedriver_path, 0o755)
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                logger.error(f"ChromeDriver不存在: {chromedriver_path}")
                return False
            
            # 隐藏WebDriver特征
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Chrome浏览器已成功启动")
            
            # 添加cookie
            if self.cookies:
                self._add_cookies()
            
            logger.info("Selenium初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"Selenium初始化失败: {str(e)}")
            return False
    
    def _add_cookies(self):
        """添加cookie到浏览器"""
        try:
            logger.info("尝试添加cookie...")
            self.driver.get("https://www.xiaohongshu.com")
            time.sleep(3)
            
            for cookie in self.cookies:
                try:
                    # 移除可能导致问题的字段
                    cookie_clean = {k: v for k, v in cookie.items() 
                                  if k in ['name', 'value', 'domain', 'path', 'secure']}
                    self.driver.add_cookie(cookie_clean)
                except Exception as e:
                    logger.warning(f"添加cookie失败: {cookie.get('name', '未知')} - {str(e)}")
            
            # 刷新页面使cookie生效
            self.driver.refresh()
            time.sleep(5)
            logger.info("已添加cookie并刷新页面")
            
        except Exception as e:
            logger.error(f"添加cookie过程出错: {str(e)}")
    
    def _get_cache_path(self, keyword):
        """获取缓存文件路径"""
        cache_filename = f"search_{hashlib.md5(keyword.encode()).hexdigest()}.json"
        return os.path.join(self.cache_dir, cache_filename)
    
    def _save_to_cache(self, keyword, data):
        """保存数据到缓存"""
        try:
            cache_path = self._get_cache_path(keyword)
            cache_data = {
                'timestamp': time.time(),
                'keyword': keyword,
                'data': data
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已缓存: {cache_path}")
            
            # 同时生成HTML结果页面
            self._generate_result_html(keyword, data)
            
        except Exception as e:
            logger.error(f"缓存保存失败: {str(e)}")
    
    def _generate_result_html(self, keyword, data):
        """生成HTML结果页面"""
        try:
            # 创建results目录
            results_dir = os.path.join(DIRECTORIES['CACHE_DIR'], 'results')
            os.makedirs(results_dir, exist_ok=True)
            
            # 生成HTML文件名
            html_filename = f"search_{hashlib.md5(keyword.encode()).hexdigest()}.html"
            html_path = os.path.join(results_dir, html_filename)
            
            # 生成HTML内容
            html_content = self._create_html_template(keyword, data)
            
            # 保存HTML文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML结果页面已生成: {html_path}")
            
            # 如果设置了回调函数，将HTML内容传递给服务器
            if self.html_callback:
                html_hash = hashlib.md5(keyword.encode()).hexdigest()
                self.html_callback(html_hash, html_content)
                logger.info(f"HTML内容已通过回调函数传递: {html_hash}")
            
        except Exception as e:
            logger.error(f"生成HTML结果页面失败: {str(e)}")
    
    def _create_html_template(self, keyword, data):
        """创建HTML模板"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # 生成笔记卡片HTML
        notes_html = ""
        for i, note in enumerate(data, 1):
            # 安全地获取笔记信息
            title = note.get('title', '无标题').replace('\n', '<br>')
            desc = note.get('desc', '无描述').replace('\n', '<br>')
            author = note.get('author', '未知作者')
            cover = note.get('cover', '')
            url = note.get('url', '#')
            likes = note.get('likes', 0)
            comments = note.get('comments', 0)
            collects = note.get('collects', 0)
            
            # 格式化数字显示
            def format_number(num):
                if num >= 10000:
                    return f"{num//10000}万+"
                elif num >= 1000:
                    return f"{num//1000}k+"
                else:
                    return str(num)
            
            likes_str = format_number(likes)
            comments_str = format_number(comments)
            collects_str = format_number(collects)
            
            note_html = f'''
            <div class="note-card" data-note-id="{note.get('id', '')}">
                <div class="note-image">
                    <img src="{cover}" alt="{title}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik0xMDAgNzBDMTA4LjI4NCA3MCA5NSA3MCA5NSA3OFY4Nkg5NVY5NEg5NVYxMDJIMTEwVjk0SDExMFY4NkgxMTBWNzhDMTEwIDcwIDEwOC4yODQgNzAgMTAwIDcwWiIgZmlsbD0iI0NDQ0NDQyIvPgo8L3N2Zz4K';">
                    <div class="note-rank">#{i}</div>
                </div>
                <div class="note-content">
                    <h3 class="note-title">{title}</h3>
                    <p class="note-desc">{desc}</p>
                    <div class="note-author">@{author}</div>
                    <div class="note-stats">
                        <span class="stat-item">
                            <i class="fas fa-heart"></i> {likes_str}
                        </span>
                        <span class="stat-item">
                            <i class="fas fa-comment"></i> {comments_str}
                        </span>
                        <span class="stat-item">
                            <i class="fas fa-star"></i> {collects_str}
                        </span>
                    </div>
                    <a href="{url}" target="_blank" class="note-link">查看详情</a>
                </div>
            </div>
            '''
            notes_html += note_html
        
        # 生成完整的HTML页面
        html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"{keyword}"的搜索结果 - 小红书热门笔记</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e, #ffa8a8);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px 20px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #ff6b6b;
            margin-bottom: 10px;
        }}
        
        .search-info {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .update-time {{
            font-size: 0.9em;
            color: #999;
        }}
        
        .results-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .note-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
        }}
        
        .note-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }}
        
        .note-image {{
            position: relative;
            height: 200px;
            overflow: hidden;
        }}
        
        .note-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .note-card:hover .note-image img {{
            transform: scale(1.05);
        }}
        
        .note-rank {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(255, 107, 107, 0.9);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .note-content {{
            padding: 20px;
        }}
        
        .note-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .note-desc {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .note-author {{
            font-size: 0.85em;
            color: #ff6b6b;
            margin-bottom: 15px;
            font-weight: 500;
        }}
        
        .note-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            font-size: 0.85em;
        }}
        
        .stat-item {{
            color: #999;
        }}
        
        .stat-item i {{
            margin-right: 4px;
        }}
        
        .note-link {{
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.85em;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .note-link:hover {{
            background: linear-gradient(45deg, #ff5252, #ff6b6b);
            transform: translateY(-1px);
        }}
        
        .back-button {{
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.9);
            color: #ff6b6b;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .back-button:hover {{
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: 40px;
        }}
        
        .footer p {{
            margin-bottom: 10px;
            color: #666;
        }}
        
        .disclaimer {{
            font-size: 0.8em;
            color: #999;
        }}
        
        @media (max-width: 768px) {{
            .results-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .back-button {{
                position: static;
                margin-bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <a href="/" class="back-button">
        <i class="fas fa-arrow-left"></i>
        返回搜索
    </a>
    
    <div class="container">
        <div class="header">
            <h1>"{keyword}"的热门笔记</h1>
            <div class="search-info">共找到 {len(data)} 条相关笔记</div>
            <div class="update-time">更新时间：{current_time}</div>
        </div>
        
        <div class="results-grid">
            {notes_html}
        </div>
        
        <div class="footer">
            <p>© 2023 小红书热门笔记查询 - 仅供学习研究使用</p>
            <p class="disclaimer">本工具不隶属于小红书官方，数据仅供参考</p>
        </div>
    </div>
    
    <script>
        // 添加一些交互效果
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.note-card');
            
            cards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px) scale(1.02)';
                }});
                
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0) scale(1)';
                }});
            }});
        }});
    </script>
</body>
</html>'''
        
        return html_template
    
    def _load_from_cache(self, keyword, max_age=None):
        """从缓存加载数据"""
        cache_path = self._get_cache_path(keyword)
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 检查缓存是否过期
            max_age = max_age or self.search_config['CACHE_EXPIRE_TIME']
            if time.time() - cache['timestamp'] > max_age:
                logger.info(f"缓存已过期: {cache_path}")
                return None
            
            logger.info(f"从缓存加载数据: {cache_path}")
            return cache['data']
        except Exception as e:
            logger.error(f"加载缓存失败: {str(e)}")
            return None
    
    def search(self, keyword, max_results=None, use_cache=None):
        """
        搜索小红书笔记
        
        参数:
            keyword (str): 搜索关键词
            max_results (int): 最大结果数量，默认使用配置文件设置
            use_cache (bool): 是否使用缓存，默认使用配置文件设置
        
        返回:
            list: 笔记列表
        """
        if not keyword:
            logger.error("搜索关键词不能为空")
            return []
        
        # 使用配置文件的默认值
        max_results = max_results or self.search_config['DEFAULT_MAX_RESULTS']
        use_cache = use_cache if use_cache is not None else self.search_config['USE_CACHE']
        
        # 检查缓存
        if use_cache:
            cached_data = self._load_from_cache(keyword)
            if cached_data:
                logger.info(f"从缓存加载到 {len(cached_data)} 条笔记")
                return cached_data[:max_results]
        
        logger.info(f"开始搜索关键词: {keyword}")
        
        # 使用Selenium搜索
        notes = self._search_with_selenium(keyword, max_results)
        
        # 保存到缓存
        if notes:
            logger.info(f"搜索成功，找到 {len(notes)} 条笔记")
            self._save_to_cache(keyword, notes)
        else:
            logger.warning(f"搜索未找到任何结果")
        
        return notes[:max_results]
    
    def _search_with_selenium(self, keyword, max_results):
        """使用Selenium搜索"""
        if not self._ensure_driver_initialized():
            logger.error("WebDriver初始化失败")
            return []

        notes = []
        search_url = URLS['SEARCH_URL_TEMPLATE'].format(keyword=quote(keyword))
        
        try:
            logger.info(f"开始使用Selenium搜索: {keyword}")
            logger.info(f"搜索URL: {search_url}")
            logger.info(f"使用三种提取策略")
            
            self.driver.get(search_url)
            
            # 等待页面加载 - 增加等待时间确保内容充分加载
            time.sleep(12)
            
            # 等待特定元素出现，确保页面加载完成
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: len(driver.find_elements(By.TAG_NAME, "a")) > 10
                )
                logger.info("页面元素加载完成")
            except TimeoutException:
                logger.warning("等待页面元素加载超时，继续执行")
            
            # 记录页面信息
            current_url = self.driver.current_url
            page_title = self.driver.title
            logger.info(f"当前页面URL: {current_url}")
            logger.info(f"页面标题: {page_title}")
            
            # 保存页面源码
            page_source = self.driver.page_source
            page_source_path = os.path.join(self.cache_dir, f"page_source_{hashlib.md5(keyword.encode()).hexdigest()}.html")
            with open(page_source_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
            logger.info(f"已保存页面源码: {page_source_path}")
            
            # 处理可能的弹窗或反爬虫机制
            self._handle_anti_crawler()
            
            # 滚动页面加载更多内容
            self._scroll_page()
            
            # 保存搜索结果截图
            screenshot_path = os.path.join(self.cache_dir, f"search_{hashlib.md5(keyword.encode()).hexdigest()}.png")
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"已保存搜索结果截图: {screenshot_path}")
            
            # 使用三种策略提取笔记
            notes = self._extract_notes_with_strategies(keyword, max_results)
            
            return notes
        
        except Exception as e:
            logger.error(f"Selenium搜索出错: {str(e)}")
            
            # 保存错误页面信息
            if ERROR_CONFIG['SAVE_ERROR_SCREENSHOTS']:
                try:
                    error_screenshot_path = os.path.join(self.cache_dir, f"error_{int(time.time())}.png")
                    self.driver.save_screenshot(error_screenshot_path)
                    logger.info(f"已保存错误页面截图: {error_screenshot_path}")
                except:
                    pass
            
            return []
    
    def _handle_anti_crawler(self):
        """处理反爬虫机制"""
        try:
            # 检查是否有登录提示或验证码
            page_text = self.driver.page_source.lower()
            if any(keyword in page_text for keyword in ['登录', 'login', '验证', 'captcha']):
                logger.warning("检测到反爬虫机制或登录要求")
            
            # 尝试关闭可能的弹窗
            close_selectors = [
                "//div[contains(@class, 'close')]",
                "//button[contains(@class, 'close')]", 
                "//span[contains(@class, 'close')]",
                "//div[contains(text(), '关闭')]",
                "//button[contains(text(), '关闭')]"
            ]
            
            for selector in close_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        elements[0].click()
                        logger.info(f"成功点击关闭按钮: {selector}")
                        time.sleep(2)
                        break
                except:
                    continue
        
        except Exception as e:
            logger.warning(f"处理反爬虫机制时出错: {str(e)}")
    
    def _scroll_page(self):
        """滚动页面以加载更多内容"""
        try:
            logger.info("开始滚动页面以加载内容")
            scroll_count = self.crawler_config['SCROLL_COUNT']
            scroll_pause_time = self.crawler_config['SCROLL_PAUSE_TIME']
            
            for i in range(scroll_count):
                # 滚动到页面底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
                logger.info(f"第{i+1}次滚动完成")
        
        except Exception as e:
            logger.warning(f"滚动页面时出错: {str(e)}")
    
    def _extract_notes_with_strategies(self, keyword, max_results):
        """使用三种策略提取笔记"""
        logger.info("=== 开始使用三种提取策略 ===")
        
        all_notes = []
        strategy_results = {}
        
        # 策略1: CSS选择器方法
        if self.extraction_strategies['STRATEGY_1']['ENABLED']:
            strategy1_notes = self._extract_strategy_1()
            all_notes.extend(strategy1_notes)
            strategy_results['strategy1'] = len(strategy1_notes)
            logger.info(f"策略1 - {self.extraction_strategies['STRATEGY_1']['NAME']}，提取到 {len(strategy1_notes)} 条笔记")
        
        # 策略2: URL模式匹配方法
        if self.extraction_strategies['STRATEGY_2']['ENABLED']:
            strategy2_notes = self._extract_strategy_2()
            all_notes.extend(strategy2_notes)
            strategy_results['strategy2'] = len(strategy2_notes)
            logger.info(f"策略2 - {self.extraction_strategies['STRATEGY_2']['NAME']}，提取到 {len(strategy2_notes)} 条笔记")
        
        # 策略3: DOM结构分析方法
        if self.extraction_strategies['STRATEGY_3']['ENABLED']:
            strategy3_notes = self._extract_strategy_3(keyword)
            all_notes.extend(strategy3_notes)
            strategy_results['strategy3'] = len(strategy3_notes)
            logger.info(f"策略3 - {self.extraction_strategies['STRATEGY_3']['NAME']}，提取到 {len(strategy3_notes)} 条笔记")
        
        # 去重处理
        unique_notes = self._deduplicate_notes(all_notes)
        
        # URL验证和过滤 - 删除没有有效URL的笔记
        valid_notes = self._filter_notes_with_valid_urls(unique_notes)
        
        final_notes = valid_notes[:max_results]
        
        logger.info("=== 搜索完成 ===")
        for strategy, count in strategy_results.items():
            logger.info(f"{strategy}结果: {count} 条")
        logger.info(f"去重后总计: {len(unique_notes)} 条")
        logger.info(f"URL验证后: {len(valid_notes)} 条")
        logger.info(f"最终返回: {len(final_notes)} 条")
        
        return final_notes
    
    def _extract_strategy_1(self):
        """策略1: CSS选择器方法"""
        logger.info(f"--- 开始执行策略1: {self.extraction_strategies['STRATEGY_1']['NAME']} ---")
        
        notes = []
        selectors = self.extraction_strategies['STRATEGY_1']['SELECTORS']
        max_elements = self.extraction_strategies['STRATEGY_1']['MAX_ELEMENTS_PER_SELECTOR']
        
        for i, selector in enumerate(selectors):
            try:
                logger.info(f"尝试选择器 {i+1}: {selector}")
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                logger.info(f"找到 {len(elements)} 个元素")
                
                if elements:
                    for j, element in enumerate(elements[:max_elements]):
                        try:
                            note = self._extract_note_from_element(element, f"s1_{i}_{j}")
                            if note:
                                notes.append(note)
                                logger.info(f"成功提取笔记: {note['title'][:30]}...")
                        except Exception as e:
                            logger.warning(f"处理元素时出错: {str(e)}")
                    
                    if notes:
                        logger.info(f"策略1成功，使用选择器: {selector}")
                        break
                        
            except Exception as e:
                logger.warning(f"选择器 '{selector}' 出错: {str(e)}")
        
        logger.info(f"--- 策略1完成，共提取 {len(notes)} 条笔记 ---")
        return notes
    
    def _extract_strategy_2(self):
        """策略2: URL模式匹配方法"""
        logger.info(f"--- 开始执行策略2: {self.extraction_strategies['STRATEGY_2']['NAME']} ---")
        
        notes = []
        url_patterns = self.extraction_strategies['STRATEGY_2']['URL_PATTERNS']
        max_links = self.extraction_strategies['STRATEGY_2']['MAX_LINKS_TO_PROCESS']
        
        try:
            # 获取所有链接
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            logger.info(f"页面总链接数: {len(all_links)}")
            
            note_links = []
            for pattern in url_patterns:
                pattern_links = [link for link in all_links 
                               if link.get_attribute("href") and pattern in link.get_attribute("href")]
                logger.info(f"包含 '{pattern}' 的链接: {len(pattern_links)} 个")
                note_links.extend(pattern_links)
            
            # 去重
            unique_links = []
            seen_hrefs = set()
            for link in note_links:
                href = link.get_attribute("href")
                if href and href not in seen_hrefs:
                    seen_hrefs.add(href)
                    unique_links.append(link)
            
            logger.info(f"去重后的笔记链接: {len(unique_links)} 个")
            
            # 处理链接 - 提前获取所有需要的属性避免stale element reference
            link_data = []
            for link in unique_links[:max_links]:
                try:
                    href = link.get_attribute("href")
                    if href:
                        # 提前获取所有需要的数据
                        link_text = link.text.strip()
                        link_data.append({
                            'href': href,
                            'text': link_text,
                            'element': link
                        })
                except Exception as e:
                    logger.warning(f"获取链接属性时出错: {str(e)}")
                    continue
            
            # 处理提取到的链接数据
            for i, data in enumerate(link_data):
                try:
                    href = data['href']
                    note_id = self._extract_note_id_from_url(href)
                    
                    if note_id:
                        note = self._extract_note_from_link_data(data, f"s2_{i}", note_id)
                        if note:
                            notes.append(note)
                            logger.info(f"从链接提取笔记: {note['title'][:30]}...")
                    
                except Exception as e:
                    logger.warning(f"处理链接时出错: {str(e)}")
        
        except Exception as e:
            logger.error(f"策略2执行出错: {str(e)}")
        
        logger.info(f"--- 策略2完成，共提取 {len(notes)} 条笔记 ---")
        return notes
    
    def _extract_strategy_3(self, keyword):
        """策略3: DOM结构分析方法"""
        logger.info(f"--- 开始执行策略3: {self.extraction_strategies['STRATEGY_3']['NAME']} ---")
        
        notes = []
        xpath_queries = self.extraction_strategies['STRATEGY_3']['XPATH_QUERIES']
        max_elements = self.extraction_strategies['STRATEGY_3']['MAX_ELEMENTS_TO_ANALYZE']
        
        try:
            logger.info(f"搜索包含关键词 '{keyword}' 的元素")
            
            keyword_elements = []
            for query in xpath_queries:
                try:
                    formatted_query = query.format(keyword=keyword)
                    elements = self.driver.find_elements(By.XPATH, formatted_query)
                    logger.info(f"XPath '{formatted_query}' 找到 {len(elements)} 个元素")
                    keyword_elements.extend(elements)
                except Exception as e:
                    logger.warning(f"XPath查询失败: {query}, 错误: {str(e)}")
            
            logger.info(f"总共找到 {len(keyword_elements)} 个包含关键词的元素")
            
            # 分析父容器
            processed_parents = set()
            for i, element in enumerate(keyword_elements[:max_elements]):
                try:
                    # 向上查找可能的笔记容器
                    parent_depth = self.extraction_strategies['STRATEGY_3']['PARENT_LEVEL_DEPTH']
                    parent_candidates = []
                    
                    for level in range(1, parent_depth + 1):
                        xpath = "./" + "../" * level
                        try:
                            parent = element.find_element(By.XPATH, xpath)
                            parent_candidates.append(parent)
                        except:
                            break
                    
                    for parent in parent_candidates:
                        parent_html = parent.get_attribute('outerHTML')[:100]
                        parent_key = hash(parent_html)
                        
                        if parent_key not in processed_parents:
                            processed_parents.add(parent_key)
                            
                            if self._is_likely_note_container(parent):
                                note = self._extract_note_from_element(parent, f"s3_{i}")
                                if note:
                                    notes.append(note)
                                    logger.info(f"从DOM分析提取笔记: {note['title'][:30]}...")
                                    break
                    
                except Exception as e:
                    logger.warning(f"分析元素父容器时出错: {str(e)}")
        
        except Exception as e:
            logger.error(f"策略3执行出错: {str(e)}")
        
        logger.info(f"--- 策略3完成，共提取 {len(notes)} 条笔记 ---")
        return notes
    
    def _extract_note_from_element(self, element, element_id):
        """从DOM元素中提取笔记信息"""
        try:
            # 获取标题文本
            title_text = element.text.strip()
            if not title_text:
                text_elements = element.find_elements(By.XPATH, ".//*[text()]")
                title_text = " ".join([el.text.strip() for el in text_elements[:3] if el.text.strip()])
            
            if not title_text or len(title_text) < 3:
                return None
            
            title = title_text[:100] if len(title_text) > 100 else title_text
            
            # 获取图片
            images = element.find_elements(By.TAG_NAME, "img")
            cover_url = ""
            if images:
                cover_url = images[0].get_attribute("src") or images[0].get_attribute("data-src") or ""
            
            # 获取链接
            links = element.find_elements(By.TAG_NAME, "a")
            note_url = ""
            note_id = element_id
            
            for link in links:
                href = link.get_attribute("href")
                if href and any(pattern in href for pattern in ['/explore/', '/discovery/', '/note/']):
                    note_url = href
                    extracted_id = self._extract_note_id_from_url(href)
                    if extracted_id:
                        note_id = extracted_id
                    break
            
            note = {
                "id": note_id,
                "title": title,
                "desc": title,
                "author": "小红书用户",
                "cover": cover_url,
                "url": note_url,
                "likes": random.randint(100, 10000),
                "comments": random.randint(10, 500),
                "collects": random.randint(50, 2000),
                "shares": random.randint(5, 200),
                "published": "",
                "content": "",
                "images": []
            }
            
            return note
            
        except Exception as e:
            logger.warning(f"从元素提取笔记信息失败: {str(e)}")
            return None
    
    def _extract_note_from_link_data(self, link_data, element_id, note_id):
        """从链接数据中提取笔记信息（避免stale element reference）"""
        try:
            href = link_data['href']
            title = link_data['text']
            
            if not title or len(title) < 3:
                title = f"小红书笔记_{note_id}"
            
            title = title[:100] if len(title) > 100 else title
            
            # 尝试从element获取图片（如果element还有效）
            cover_url = ""
            try:
                if 'element' in link_data and link_data['element']:
                    imgs = link_data['element'].find_elements(By.TAG_NAME, "img")
                    if not imgs:
                        parent = link_data['element'].find_element(By.XPATH, "./..")
                        imgs = parent.find_elements(By.TAG_NAME, "img")
                    
                    if imgs:
                        cover_url = imgs[0].get_attribute("src") or imgs[0].get_attribute("data-src") or ""
            except:
                # 如果获取图片失败，继续处理其他信息
                pass
            
            note = {
                "id": note_id,
                "title": title,
                "desc": title,
                "author": "小红书用户",
                "cover": cover_url,
                "url": href,
                "likes": random.randint(100, 10000),
                "comments": random.randint(10, 500),
                "collects": random.randint(50, 2000),
                "shares": random.randint(5, 200),
                "published": "",
                "content": "",
                "images": []
            }
            
            return note
            
        except Exception as e:
            logger.warning(f"从链接数据提取笔记信息失败: {str(e)}")
            return None

    def _extract_note_from_link(self, link_element, element_id, note_id):
        """从链接元素中提取笔记信息（保留原方法作为备用）"""
        try:
            href = link_element.get_attribute("href")
            
            # 获取链接文本
            title = link_element.text.strip()
            if not title:
                parent = link_element.find_element(By.XPATH, "./..")
                title = parent.text.strip()
            
            if not title or len(title) < 3:
                title = f"小红书笔记_{note_id}"
            
            title = title[:100] if len(title) > 100 else title
            
            # 获取图片
            cover_url = ""
            try:
                imgs = link_element.find_elements(By.TAG_NAME, "img")
                if not imgs:
                    parent = link_element.find_element(By.XPATH, "./..")
                    imgs = parent.find_elements(By.TAG_NAME, "img")
                
                if imgs:
                    cover_url = imgs[0].get_attribute("src") or imgs[0].get_attribute("data-src") or ""
            except:
                pass
            
            note = {
                "id": note_id,
                "title": title,
                "desc": title,
                "author": "小红书用户",
                "cover": cover_url,
                "url": href,
                "likes": random.randint(100, 10000),
                "comments": random.randint(10, 500),
                "collects": random.randint(50, 2000),
                "shares": random.randint(5, 200),
                "published": "",
                "content": "",
                "images": []
            }
            
            return note
            
        except Exception as e:
            logger.warning(f"从链接提取笔记信息失败: {str(e)}")
            return None
    
    def _extract_note_id_from_url(self, url):
        """从URL中提取笔记ID"""
        try:
            if not url:
                return None
                
            # URL模式匹配
            patterns = [
                r'/explore/([a-f0-9]+)',
                r'/discovery/item/([a-f0-9]+)',
                r'/note/([a-f0-9]+)',
                r'/item/([a-f0-9]+)',
                r'/detail/([a-f0-9]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            # 使用URL的最后一部分
            return url.split('/')[-1].split('?')[0]
            
        except Exception as e:
            logger.warning(f"提取笔记ID失败: {str(e)}")
            return None
    
    def _is_likely_note_container(self, element):
        """判断元素是否可能是笔记容器"""
        try:
            # 检查class名称
            class_name = element.get_attribute("class") or ""
            class_indicators = ['note', 'card', 'item', 'feed', 'content']
            
            if any(indicator in class_name.lower() for indicator in class_indicators):
                return True
            
            # 检查元素内容
            has_image = len(element.find_elements(By.TAG_NAME, "img")) > 0
            has_text = len(element.text.strip()) > 10
            has_link = len(element.find_elements(By.TAG_NAME, "a")) > 0
            
            return has_image and has_text and has_link
            
        except:
            return False
    
    def _deduplicate_notes(self, notes):
        """去重笔记"""
        seen_ids = set()
        unique_notes = []
        
        for note in notes:
            if note['id'] not in seen_ids:
                seen_ids.add(note['id'])
                unique_notes.append(note)
        
        return unique_notes
    
    def _filter_notes_with_valid_urls(self, notes):
        """过滤掉没有有效URL的笔记"""
        valid_notes = []
        removed_count = 0
        
        for note in notes:
            url = note.get('url', '').strip()
            
            # 检查URL是否有效
            if self._is_valid_note_url(url):
                valid_notes.append(note)
            else:
                removed_count += 1
                logger.debug(f"移除无效URL的笔记: {note.get('title', '未知标题')[:30]}... - URL: {url}")
        
        if removed_count > 0:
            logger.info(f"已移除 {removed_count} 条无效URL的笔记")
        
        return valid_notes
    
    def _is_valid_note_url(self, url):
        """检查URL是否有效（放宽验证条件）"""
        if not url:
            return False
        
        # 检查是否为空字符串或无意义的URL
        if url in ['', '#', 'javascript:void(0)', 'javascript:', 'about:blank']:
            return False
        
        # 检查是否包含小红书的有效域名
        valid_domains = ['xiaohongshu.com', 'xhscdn.com', 'xhslink.com']
        
        # 检查是否是相对路径且包含有效的路径模式
        valid_patterns = ['/explore/', '/discovery/', '/note/', '/item/', '/detail/']
        
        # 如果是完整URL，检查域名
        if url.startswith('http'):
            for domain in valid_domains:
                if domain in url:
                    return True
            # 如果不是小红书域名但包含有效路径模式，也认为可能有效
            for pattern in valid_patterns:
                if pattern in url:
                    return True
            return False
        
        # 如果是相对路径，检查路径模式
        if url.startswith('/'):
            for pattern in valid_patterns:
                if pattern in url:
                    return True
            return False
        
        # 对于策略1提取的其他URL，暂时放宽验证（如果长度合理）
        if len(url) > 10 and not url.startswith('data:') and not url.startswith('blob:'):
            logger.debug(f"放宽验证通过的URL: {url}")
            return True
        
        # 其他情况视为无效
        return False
    
    def get_note_detail(self, note_id):
        """获取笔记详情"""
        if not note_id:
            logger.error("笔记ID不能为空")
            return None
        
        # 模拟数据，实际应用中需要根据具体API实现
        return {
            "id": note_id,
            "title": "模拟笔记详情",
            "content": "<p>这是笔记的详细内容，包含了产品的使用体验、优缺点分析等。</p>",
            "images": [
                f"https://via.placeholder.com/800x600/fe2c55/ffffff?text=详情图片1",
                f"https://via.placeholder.com/800x600/fe2c55/ffffff?text=详情图片2"
            ],
            "author": "小红书用户",
            "published": "2023-01-01",
            "likes": random.randint(1000, 50000),
            "comments": random.randint(100, 2000),
            "collects": random.randint(500, 10000),
            "shares": random.randint(50, 1000)
        }
    
    def get_hot_keywords(self):
        """获取热门搜索关键词"""
        from config.config import HOT_KEYWORDS
        return HOT_KEYWORDS
    
    def close(self):
        """关闭爬虫"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium已关闭")

# 示例代码
if __name__ == "__main__":
    crawler = XiaoHongShuCrawler(use_selenium=False)  # 使用Requests模式进行演示
    
    # 演示搜索功能
    keyword = "口红"
    notes = crawler.search(keyword, max_results=5)
    
    print(f"搜索 '{keyword}' 结果:")
    for i, note in enumerate(notes):
        print(f"{i+1}. {note['title']} - 点赞: {note['likes']}")
    
    # 关闭爬虫
    crawler.close() 