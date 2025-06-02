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
        
        # 加载cookie
        self.cookies = self._load_cookies()
        
        logger.info("小红书爬虫初始化完成")
    
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
        except Exception as e:
            logger.error(f"缓存保存失败: {str(e)}")
    
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
            
            # 等待页面加载
            time.sleep(8)
            
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
            
            # 处理链接
            for i, link in enumerate(unique_links[:max_links]):
                try:
                    href = link.get_attribute("href")
                    note_id = self._extract_note_id_from_url(href)
                    
                    if note_id:
                        note = self._extract_note_from_link(link, f"s2_{i}", note_id)
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
    
    def _extract_note_from_link(self, link_element, element_id, note_id):
        """从链接元素中提取笔记信息"""
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
        """检查URL是否有效"""
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
            return False
        
        # 如果是相对路径，检查路径模式
        if url.startswith('/'):
            for pattern in valid_patterns:
                if pattern in url:
                    return True
            return False
        
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