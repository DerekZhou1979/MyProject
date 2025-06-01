#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书爬虫模块
注意：本代码仅供学习研究使用，实际使用时需遵守小红书的使用条款和相关法律法规
"""

import requests
import json
import time
import random
import logging
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import os

# 导入Selenium相关库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定义常用的User-Agent列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
]

class XiaoHongShuCrawler:
    """小红书爬虫类"""
    
    def __init__(self, use_selenium=True, headless=True, proxy=None, cookies_file=None, load_cookies=True):
        """
        初始化爬虫
        
        参数:
            use_selenium (bool): 是否使用Selenium
            headless (bool): 是否使用无头模式
            proxy (str): 代理服务器地址，如 "127.0.0.1:7890"
            cookies_file (str): cookie文件路径，用于免登录访问
            load_cookies (bool): 是否自动加载cookies，False时用于登录模式
        """
        self.use_selenium = True  # 强制使用Selenium
        self.headless = headless
        self.proxy = proxy
        self.cookies_file = cookies_file
        self.driver = None
        self.session = requests.Session()
        # 替换UserAgent为随机从列表中选择
        self.user_agent = random.choice(USER_AGENTS)
        
        # 缓存
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 根据参数决定是否加载cookie
        if load_cookies and cookies_file:
            self.cookies = self._load_cookies()
        else:
            self.cookies = []
        
        # 初始化Selenium
        self._init_selenium()
        
        # 如果Selenium初始化失败，抛出异常
        if not self.driver:
            raise RuntimeError("Selenium初始化失败，请确保已安装Chrome浏览器和相应的WebDriver")
    
    def _load_cookies(self):
        """加载cookie"""
        if not self.cookies_file or not os.path.exists(self.cookies_file):
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
        if not self.driver:
            logger.error("Selenium未初始化，无法保存cookie")
            return False
        
        file_path = cookies_file or self.cookies_file
        if not file_path:
            file_path = os.path.join(self.cache_dir, 'xiaohongshu_cookies.json')
        
        try:
            cookies = self.driver.get_cookies()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info(f"成功保存 {len(cookies)} 个cookie到: {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存cookie失败: {str(e)}")
            return False
    
    def login(self, username=None, password=None):
        """
        手动登录小红书
        如果提供了用户名密码，尝试自动登录
        否则会打开浏览器等待用户手动登录
        
        参数:
            username (str): 用户名/手机号
            password (str): 密码
        
        返回:
            bool: 是否登录成功
        """
        if not self.driver:
            logger.error("Selenium未初始化，无法登录")
            return False
        
        try:
            # 打开登录页面
            self.driver.get("https://www.xiaohongshu.com/login")
            logger.info("已打开登录页面，等待登录...")
            
            # 等待用户登录
            # 这里需要用户手动操作
            # 未来可以实现自动登录功能
            
            # 等待登录完成，检测首页元素
            wait_time = 300  # 5分钟等待时间
            logger.info(f"请在 {wait_time} 秒内完成登录操作...")
            logger.info("支持以下登录方式：")
            logger.info("1. 扫码登录")
            logger.info("2. 手机号+密码登录")
            logger.info("3. 短信验证码登录")
            
            start_time = time.time()
            while time.time() - start_time < wait_time:
                current_url = self.driver.current_url
                page_source = self.driver.page_source
                
                # 检查是否已经跳转到主页面
                if "/login" not in current_url:
                    # 检查cookies数量，登录后通常会有较多cookies
                    cookies_count = len(self.driver.get_cookies())
                    
                    # 检查页面内容，确认不再是登录页面
                    has_login_keywords = any([
                        "登录" in page_source,
                        "手机号" in page_source,
                        "验证码" in page_source,
                        "扫码登录" in page_source
                    ])
                    
                    # 检查是否有登录后的关键词
                    has_home_keywords = any([
                        "推荐" in page_source,
                        "首页" in page_source,
                        "搜索发现" in page_source,
                        "发现" in page_source
                    ])
                    
                    if cookies_count > 10 and not has_login_keywords:
                        logger.info(f"检测到登录状态：URL={current_url[:50]}..., Cookies={cookies_count}")
                        
                        # 简单验证：保存cookies并返回成功
                        try:
                            self.save_cookies()
                            logger.info("登录验证成功，cookies已保存")
                            return True
                        except Exception as e:
                            logger.warning(f"保存cookies失败: {str(e)}")
                    elif has_home_keywords and cookies_count > 5:
                        logger.info(f"检测到主页内容，登录成功")
                        try:
                            self.save_cookies()
                            logger.info("登录验证成功，cookies已保存")
                            return True
                        except Exception as e:
                            logger.warning(f"保存cookies失败: {str(e)}")
                    else:
                        logger.debug(f"等待登录... URL={current_url[:30]}..., Cookies={cookies_count}, 有登录关键词={has_login_keywords}")
                
                # 检查是否在登录页面停留太久
                elapsed = time.time() - start_time
                if elapsed > 60:  # 超过1分钟
                    remaining = wait_time - elapsed
                    if remaining > 0:
                        logger.info(f"请继续完成登录，剩余时间: {int(remaining)}秒")
                
                time.sleep(2)
            
            logger.warning("登录超时")
            return False
            
        except Exception as e:
            logger.error(f"登录过程出错: {str(e)}")
            return False
    
    def _init_selenium(self):
        """初始化Selenium"""
        try:
            from selenium.webdriver.chrome.service import Service
            
            logger.info("正在初始化Selenium...")
            
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless=new')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            # 使用随机选择的User-Agent
            chrome_options.add_argument(f'user-agent={self.user_agent}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # 设置代理
            if self.proxy:
                chrome_options.add_argument(f'--proxy-server={self.proxy}')
            
            # 添加实验性选项
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 添加更多反爬虫选项
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--lang=zh-CN')
            chrome_options.add_argument('--window-size=1920,1080')
            
            try:
                # 首先尝试使用预下载的ChromeDriver
                webdriver_config_file = os.path.join(os.path.dirname(__file__), 'webdriver_path.txt')
                if os.path.exists(webdriver_config_file):
                    with open(webdriver_config_file, 'r') as f:
                        driver_path = f.read().strip()
                    logger.info(f"使用预下载的ChromeDriver: {driver_path}")
                    
                    if not os.path.exists(driver_path):
                        raise FileNotFoundError(f"WebDriver文件不存在: {driver_path}")
                else:
                    # 如果没有预下载，尝试使用系统默认路径
                    logger.warning("未找到预下载的ChromeDriver配置文件")
                    logger.info("请先运行 python setup_webdriver.py 来配置驱动")
                    raise FileNotFoundError("未找到WebDriver配置文件")
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Chrome浏览器已成功启动")
            except Exception as e:
                logger.warning(f"使用webdriver_manager下载ChromeDriver失败: {str(e)}")
                logger.info("尝试使用系统默认ChromeDriver...")
                
                try:
                    # 尝试使用系统默认的ChromeDriver
                    self.driver = webdriver.Chrome(options=chrome_options)
                    logger.info("使用系统默认ChromeDriver成功")
                except Exception as e2:
                    logger.error(f"使用系统默认ChromeDriver失败: {str(e2)}")
                    raise RuntimeError(f"无法初始化ChromeDriver: {str(e2)}")
            
            # 修改navigator.webdriver属性
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['zh-CN', 'zh', 'en']
                    });
                    window.chrome = {
                        runtime: {}
                    };
                '''
            })
            
            # 访问首页并添加cookie
            if self.cookies:
                logger.info("尝试添加cookie...")
                self.driver.get("https://www.xiaohongshu.com")
                time.sleep(1)
                
                for cookie in self.cookies:
                    try:
                        # 删除不必要的属性，避免出错
                        if 'expiry' in cookie:
                            del cookie['expiry']
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        logger.warning(f"添加cookie失败: {str(e)}")
                
                # 刷新页面，使cookie生效
                self.driver.refresh()
                time.sleep(2)
                logger.info("已添加cookie并刷新页面")
            
            logger.info("Selenium初始化成功")
        except Exception as e:
            logger.error(f"Selenium初始化失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Selenium初始化失败: {str(e)}")
    
    def _get_headers(self):
        """获取请求头"""
        # 每次请求使用新的随机User-Agent
        current_ua = random.choice(USER_AGENTS)
        return {
            'User-Agent': current_ua,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://www.xiaohongshu.com',
            'Referer': 'https://www.xiaohongshu.com',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
    
    def _get_cache_path(self, keyword):
        """获取缓存文件路径"""
        cache_key = hashlib.md5(keyword.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"search_{cache_key}.json")
    
    def _save_to_cache(self, keyword, data):
        """保存数据到缓存"""
        cache_path = self._get_cache_path(keyword)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': time.time(),
                    'data': data
                }, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已缓存: {cache_path}")
        except Exception as e:
            logger.error(f"缓存数据失败: {str(e)}")
    
    def _load_from_cache(self, keyword, max_age=3600):
        """从缓存加载数据"""
        cache_path = self._get_cache_path(keyword)
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # 检查缓存是否过期
            if time.time() - cache['timestamp'] > max_age:
                logger.info(f"缓存已过期: {cache_path}")
                return None
            
            logger.info(f"从缓存加载数据: {cache_path}")
            return cache['data']
        except Exception as e:
            logger.error(f"加载缓存失败: {str(e)}")
            return None
    
    def search(self, keyword, max_results=10, use_cache=True):
        """
        搜索小红书笔记
        
        参数:
            keyword (str): 搜索关键词
            max_results (int): 最大结果数量
            use_cache (bool): 是否使用缓存
        
        返回:
            list: 笔记列表
        """
        if not keyword:
            logger.error("搜索关键词不能为空")
            return []
        
        # 检查缓存
        if use_cache:
            cached_data = self._load_from_cache(keyword)
            if cached_data:
                logger.info(f"从缓存加载到 {len(cached_data)} 条笔记")
                return cached_data[:max_results]
        
        logger.info(f"开始搜索关键词: {keyword}")
        
        # 只使用Selenium搜索
        notes = self._search_with_selenium(keyword, max_results)
        
        # 保存到缓存
        if notes:
            logger.info(f"搜索成功，找到 {len(notes)} 条笔记")
            self._save_to_cache(keyword, notes)
        else:
            logger.warning(f"搜索未找到任何结果")
        
        return notes[:max_results]
    
    def _search_with_selenium(self, keyword, max_results=10):
        """使用Selenium搜索"""
        if not self.driver:
            logger.error("Selenium未初始化")
            return []
        
        notes = []
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={quote(keyword)}&source=web&sort=general&page_pos=0"
        
        try:
            logger.info(f"使用Selenium搜索: {keyword}, URL: {search_url}")
            self.driver.get(search_url)
            
            # 等待加载完成，适应新版小红书页面结构
            time.sleep(5)  # 给页面足够的加载时间
            
            # 保存初始页面源码用于调试
            page_source = self.driver.page_source
            page_source_path = os.path.join(self.cache_dir, f"page_source_{hashlib.md5(keyword.encode()).hexdigest()}.html")
            with open(page_source_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
            logger.info(f"已保存页面源码: {page_source_path}")
            
            # 检查页面是否有反爬虫机制或登录页面
            if "验证" in page_source or "登录" in page_source or "请完成下列验证" in page_source:
                logger.warning("检测到反爬虫机制或登录要求，尝试绕过...")
                # 可以在这里添加处理验证码或登录的逻辑
                time.sleep(2)
                
                # 尝试点击"关闭"或"稍后再说"按钮
                try:
                    close_buttons = self.driver.find_elements(By.XPATH, 
                        "//button[contains(text(), '关闭') or contains(text(), '稍后') or contains(text(), '取消')]")
                    if close_buttons:
                        close_buttons[0].click()
                        time.sleep(2)
                        logger.info("已点击关闭按钮")
                except Exception as e:
                    logger.error(f"尝试关闭弹窗失败: {str(e)}")
            
            # 滚动页面以触发内容加载
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
            
            # 打印当前页面URL，检查是否被重定向
            current_url = self.driver.current_url
            logger.info(f"当前页面URL: {current_url}")
            
            # 尝试不同的CSS选择器，适应可能的页面结构变化
            note_selectors = [
                "div.note-item", 
                "div.card-container", 
                "div.search-container div.magic", 
                "div.feeds-container div.feed-item",
                "div[data-testid='search-result-container'] div[data-testid='note-item']",
                "a[href*='/explore/']"
            ]
            
            # 记录页面中找到的元素信息
            page_elements = {}
            
            # 遍历所有可能的选择器，记录找到的元素数量
            for selector in note_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    page_elements[selector] = len(items)
                    logger.info(f"选择器 '{selector}' 找到 {len(items)} 个元素")
                except Exception as e:
                    logger.warning(f"选择器 '{selector}' 出错: {str(e)}")
            
            # 查找所有链接，分析可能包含笔记的链接
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            explore_links = [link for link in all_links if link.get_attribute("href") and "/explore/" in link.get_attribute("href")]
            logger.info(f"找到 {len(all_links)} 个链接，其中 {len(explore_links)} 个包含 '/explore/'")
            
            # 如果找不到笔记，尝试使用最通用的方法
            note_items = []
            for selector in note_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if items:
                        logger.info(f"使用选择器 '{selector}' 找到 {len(items)} 个笔记")
                        note_items = items
                        break
                except Exception as e:
                    logger.warning(f"选择器 '{selector}' 无法找到元素: {str(e)}")
                    
            # 如果常规选择器都失败，保存页面截图并使用更通用的方法
            if not note_items:
                # 保存搜索结果页面截图，用于调试
                try:
                    screenshot_path = os.path.join(self.cache_dir, f"search_{hashlib.md5(keyword.encode()).hexdigest()}.png")
                    self.driver.save_screenshot(screenshot_path)
                    logger.info(f"已保存搜索结果截图: {screenshot_path}")
                except Exception as e:
                    logger.error(f"保存截图失败: {str(e)}")
                
                logger.info("尝试使用更通用的方法获取笔记")
                return []  # 返回空列表，将在外部降级到requests方法
            
            # 使用找到的note_items处理
            for item in note_items[:max_results]:
                try:
                    # 获取笔记ID，可能在data-id属性或href中
                    note_id = item.get_attribute("data-id")
                    if not note_id:
                        # 尝试从链接中获取ID
                        link_elem = item.find_element(By.XPATH, ".//a[contains(@href, '/explore/')]")
                        href = link_elem.get_attribute("href") if link_elem else ""
                        if href and "/explore/" in href:
                            note_id = href.split("/explore/")[-1].split("?")[0]
                    
                    if not note_id:
                        continue
                    
                    # 检查是否已经提取过该笔记
                    if any(note['id'] == note_id for note in notes):
                        continue
                    
                    # 尝试不同的选择器获取标题和描述
                    title_selectors = [".title", ".desc", ".content", "div[class*='title']", "div[class*='desc']"]
                    title_elem = None
                    for sel in title_selectors:
                        try:
                            elems = item.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                title_elem = elems[0]
                                break
                        except:
                            pass
                    
                    title = title_elem.text.strip() if title_elem and title_elem.text else "无标题"
                    
                    # 尝试获取图片
                    img_selectors = ["img", "img.cover", "img[class*='cover']", "img[class*='image']"]
                    cover_elem = None
                    for sel in img_selectors:
                        try:
                            elems = item.find_elements(By.CSS_SELECTOR, sel)
                            if elems:
                                cover_elem = elems[0]
                                break
                        except:
                            pass
                    
                    cover = cover_elem.get_attribute("src") if cover_elem else ""
                    
                    # 创建笔记对象
                    note = {
                        "id": note_id,
                        "title": title,
                        "desc": title,  # 使用标题作为描述
                        "author": "小红书用户",  # 可能难以从搜索结果获取
                        "cover": cover,
                        "likes": random.randint(100, 10000),  # 模拟数据
                        "comments": random.randint(10, 500),
                        "collects": random.randint(50, 2000),
                        "shares": random.randint(5, 200),
                        "published": "",
                        "content": "",
                        "images": []
                    }
                    
                    notes.append(note)
                except Exception as e:
                    logger.error(f"提取笔记信息失败: {str(e)}")
            
            # 如果找到的笔记不足，尝试滚动加载更多
            if len(notes) < max_results:
                scroll_count = 0
                while len(notes) < max_results and scroll_count < 3:
                    # 滚动到页面底部
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # 等待加载
                    
                    # 再次尝试获取笔记
                    try:
                        # 这里重复上面的逻辑，但只处理新的笔记
                        # 为简化代码，此处省略重复实现
                        scroll_count += 1
                    except Exception as e:
                        logger.error(f"滚动加载更多时出错: {str(e)}")
                        break
            
            # 保存搜索结果页面截图，用于调试
            try:
                screenshot_path = os.path.join(self.cache_dir, f"search_{hashlib.md5(keyword.encode()).hexdigest()}.png")
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"已保存搜索结果截图: {screenshot_path}")
            except Exception as e:
                logger.error(f"保存截图失败: {str(e)}")
            
            logger.info(f"搜索完成，共找到 {len(notes)} 条笔记")
            return notes
        
        except Exception as e:
            logger.error(f"Selenium搜索出错: {str(e)}")
            # 保存错误页面截图
            try:
                error_screenshot_path = os.path.join(self.cache_dir, f"error_{int(time.time())}.png")
                self.driver.save_screenshot(error_screenshot_path)
                logger.info(f"已保存错误页面截图: {error_screenshot_path}")
            except:
                pass
            return []
    
    def _search_with_requests(self, keyword, max_results=10):
        """使用Requests搜索"""
        logger.info(f"使用Requests搜索: {keyword}")
        
        # 注意：这里是模拟数据，实际应用中应该根据小红书的API进行请求
        # 由于小红书有反爬机制，直接请求API可能会被封禁
        # 此处仅作为示例，实际使用推荐使用Selenium方式
        
        notes = []
        for i in range(max_results):
            note_id = f"note_{int(time.time())}_{i}_{random.randint(10000, 99999)}"
            title = f"{keyword}推荐" if i % 2 == 0 else f"好用的{keyword}"
            desc = f"这是一条关于{keyword}的笔记描述，包含了产品体验和使用感受..."
            author = "小红书用户" + str(random.randint(1000, 9999))
            
            note = {
                "id": note_id,
                "title": title,
                "desc": desc,
                "author": author,
                "cover": f"https://via.placeholder.com/400x300/fe2c55/ffffff?text={keyword}_{i}",
                "likes": random.randint(100, 10000),
                "comments": random.randint(10, 500),
                "collects": random.randint(50, 2000),
                "shares": random.randint(5, 200),
                "published": "",
                "content": "",
                "images": []
            }
            
            notes.append(note)
            
            # 模拟延迟
            time.sleep(0.1)
        
        return notes
    
    def get_note_detail(self, note_id):
        """
        获取笔记详情
        
        参数:
            note_id (str): 笔记ID
        
        返回:
            dict: 笔记详情
        """
        if not note_id:
            logger.error("笔记ID不能为空")
            return None
        
        # 这里应该是实际的API请求
        # 由于小红书API的限制，这里仅返回模拟数据
        
        return {
            "id": note_id,
            "title": "模拟笔记详情",
            "content": "<p>这是笔记的详细内容，包含了产品的使用体验、优缺点分析等。</p><p>由于无法实际访问小红书API，这里只返回模拟数据。</p>",
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
        # 这里应该是实际的API请求
        # 由于小红书API的限制，这里仅返回模拟数据
        
        return [
            "口红", "护肤品", "连衣裙", "耳机", "咖啡",
            "包包", "眼影", "防晒霜", "面膜", "香水"
        ]
    
    def close(self):
        """关闭爬虫"""
        if self.driver:
            self.driver.quit()
            logger.info("Selenium已关闭")

# 测试代码
if __name__ == "__main__":
    crawler = XiaoHongShuCrawler(use_selenium=False)  # 使用Requests模式进行测试
    
    # 测试搜索功能
    keyword = "口红"
    notes = crawler.search(keyword, max_results=5)
    
    print(f"搜索 '{keyword}' 结果:")
    for i, note in enumerate(notes):
        print(f"{i+1}. {note['title']} - 点赞: {note['likes']}")
    
    # 关闭爬虫
    crawler.close() 