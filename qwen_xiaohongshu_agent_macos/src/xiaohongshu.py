#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小红书自动发布模块
负责将生成的内容发布到小红书平台
"""

import os
import time
import json
import logging
import requests
from datetime import datetime
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

class XiaohongshuPublisher:
    """小红书发布客户端"""
    
    def __init__(self, config):
        """初始化小红书发布客户端
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.cookie = config.get("xiaohongshu", "cookie")
        self.user_agent = config.get("xiaohongshu", "user_agent")
        self.max_retries = config.get("runtime", "max_retries")
        self.retry_delay = config.get("runtime", "retry_delay")
        
        # 验证Cookie是否已设置
        if not self.cookie:
            logging.error("小红书Cookie未设置，请在配置文件中设置cookie")
            raise ValueError("小红书Cookie未设置")
    
    def publish_content(self, content):
        """发布内容到小红书
        
        Args:
            content: 内容字典，包含标题、正文和标签
            
        Returns:
            发布结果字典，包含状态和消息
        """
        logging.info(f"准备发布内容: {content['title']}")
        
        for attempt in range(self.max_retries):
            try:
                logging.info(f"正在发布内容 (尝试 {attempt+1}/{self.max_retries})")
                
                # 使用Playwright模拟浏览器发布内容
                result = self._publish_with_playwright(content)
                
                logging.info(f"内容发布成功: {result}")
                return {
                    "status": "success",
                    "message": "内容发布成功",
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
            except Exception as e:
                logging.error(f"发布内容失败: {e}")
                if attempt < self.max_retries - 1:
                    logging.info(f"将在 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logging.error("已达到最大重试次数，放弃发布内容")
                    return {
                        "status": "error",
                        "message": f"发布内容失败: {str(e)}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
    
    def _publish_with_playwright(self, content):
        """使用Playwright模拟浏览器发布内容
        
        Args:
            content: 内容字典
            
        Returns:
            发布结果
        """
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=self.user_agent,
                viewport={"width": 1280, "height": 800}
            )
            logging.info(f"----浏览器已启动版本{browser}")
            logging.info(f"----浏览器已启动chromium")
            logging.info(f"----浏览器已启动context{context}")
            logging.info(f"----浏览器已启动chromium")
            
            # 设置Cookie
            self._set_cookies(context)
            
            # 打开小红书创建笔记页面
            page = context.new_page()
            page.goto("https://creator.xiaohongshu.com/publish/publish?from=menu", wait_until="networkidle")
            
            logging.info(f"----浏览器页面：{page.url}")
            logging.info(f"----浏览器页面：{page}")
            logging.info(f"----浏览器页面：{context}")
            logging.info(f"----浏览器页面：{browser}")
            logging.info(f"----浏览器页面：{self}")
            logging.info(f"----浏览器页面：{content}")
            logging.info(f"----浏览器页面：{self.cookie}")

            # 等待页面加载完成
            page.wait_for_selector("textarea, div[contenteditable=true]", timeout=30000)
            
            # 检查是否需要登录
            if "login" in page.url:
                logging.error("Cookie已过期，需要重新登录")
                browser.close()
                raise Exception("Cookie已过期，需要重新登录")
            
            # 填写标题
            title_selector = "textarea, div[contenteditable=true]"
            page.fill(title_selector, content["title"])
            
            # 填写正文内容
            content_selector = "div[contenteditable=true]"
            content_elements = page.query_selector_all(content_selector)
            if len(content_elements) >= 2:
                # 第二个contenteditable元素通常是正文
                content_elements[1].fill(content["content"])
            else:
                logging.warning("未找到正文输入框，尝试其他选择器")
                # 尝试其他可能的选择器
                alt_selectors = [
                    "div.publish-content",
                    "div.content-input",
                    "div.editor-content"
                ]
                for selector in alt_selectors:
                    element = page.query_selector(selector)
                    if element:
                        element.fill(content["content"])
                        break
            
            # 添加标签
            if content["tags"]:
                # 点击添加标签按钮
                tag_button_selectors = [
                    "button:has-text('添加标签')",
                    "div:has-text('添加标签')",
                    "span:has-text('添加标签')"
                ]
                for selector in tag_button_selectors:
                    tag_button = page.query_selector(selector)
                    if tag_button:
                        tag_button.click()
                        break
                
                # 等待标签输入框出现
                page.wait_for_selector("input[placeholder*='标签']", timeout=5000)
                
                # 添加每个标签
                for tag in content["tags"]:
                    tag_input = page.query_selector("input[placeholder*='标签']")
                    if tag_input:
                        tag_input.fill(tag)
                        tag_input.press("Enter")
                        time.sleep(0.5)
            
            # 点击发布按钮
            publish_button_selectors = [
                "button:has-text('发布')",
                "div.publish-button:has-text('发布')",
                "span.publish-button:has-text('发布')"
            ]
            for selector in publish_button_selectors:
                publish_button = page.query_selector(selector)
                if publish_button:
                    publish_button.click()
                    break
            
            # 等待发布完成
            try:
                # 等待成功提示或跳转
                page.wait_for_selector("div:has-text('发布成功')", timeout=10000)
                logging.info("检测到发布成功提示")
            except Exception:
                # 如果没有明确的成功提示，等待一段时间
                logging.info("未检测到发布成功提示，等待10秒")
                time.sleep(10)
            
            # 获取当前URL，可能包含已发布笔记的ID
            current_url = page.url
            
            # 关闭浏览器
            browser.close()
            
            return {
                "url": current_url,
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _set_cookies(self, context):
        """设置浏览器Cookie
        
        Args:
            context: 浏览器上下文
        """
        # 解析Cookie字符串
        cookies = []
        for cookie_str in self.cookie.split(';'):
            if '=' in cookie_str:
                name, value = cookie_str.strip().split('=', 1)
                cookies.append({
                    "name": name,
                    "value": value,
                    "domain": ".xiaohongshu.com",
                    "path": "/"
                })
        
        # 设置Cookie
        context.add_cookies(cookies)
    
    def check_login_status(self):
        """检查登录状态
        
        Returns:
            登录状态字典
        """
        try:
            headers = {
                "User-Agent": self.user_agent,
                "Cookie": self.cookie
            }
            
            response = requests.get(
                "https://www.xiaohongshu.com/user/profile",
                headers=headers
            )
            
            if response.status_code == 200 and "login" not in response.url:
                return {
                    "status": "success",
                    "message": "已登录",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                return {
                    "status": "error",
                    "message": "未登录或Cookie已过期",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"检查登录状态失败: {str(e)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
