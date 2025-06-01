#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
import signal
import logging
from typing import List, Optional
from playwright.sync_api import sync_playwright, Page, Browser

# 设置全局变量用于优雅退出
should_exit = False

def signal_handler(signum, frame):
    """信号处理函数"""
    global should_exit
    print("\n检测到退出信号，正在安全退出...")
    should_exit = True

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

class XiaohongshuPublisher:
    def __init__(self, cookies_path: str = "cookies.json"):
        self.cookies_path = os.path.abspath(cookies_path)
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        """设置日志配置"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def load_cookies(self) -> List[dict]:
        """加载cookies"""
        try:
            with open(self.cookies_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                self.logger.info(f"成功加载 cookies，共 {len(cookies)} 个")
                return cookies
        except FileNotFoundError:
            self.logger.warning(f"Cookie文件不存在: {self.cookies_path}")
            return []
        except json.JSONDecodeError:
            self.logger.error(f"Cookie文件格式错误: {self.cookies_path}")
            return []

    def save_cookies(self, cookies: List[dict]):
        """保存cookies"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.cookies_path), exist_ok=True)
            
            with open(self.cookies_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            self.logger.info(f"成功保存 {len(cookies)} 个 cookies 到: {self.cookies_path}")
        except Exception as e:
            self.logger.error(f"保存 cookies 失败: {str(e)}")

    def check_login_status(self, page: Page) -> bool:
        """检查是否已登录"""
        try:
            # 等待页面加载完成
            page.wait_for_load_state('networkidle')
            
            # 检查URL，如果已经在发布页面或者其他用户页面，说明已登录
            if '/publish' in page.url or '/user/' in page.url:
                return True
            
            # 检查多个可能的登录状态指标
            login_indicators = [
                '登录',
                '注册',
                '手机号登录',
                '密码登录',
                '验证码登录'
            ]
            
            # 检查页面内容
            content = page.content().lower()
            
            # 如果页面上有明显的登录相关文字，说明未登录
            login_text_present = any(indicator in content for indicator in login_indicators)
            if login_text_present:
                return False
            
            # 尝试检查特定元素
            try:
                # 如果能找到这些元素，说明还没登录
                login_elements = page.query_selector_all('text=登录, text=注册, text="手机号登录"')
                if login_elements:
                    return False
            except Exception:
                pass
            
            # 尝试检查用户相关元素
            try:
                # 如果能找到这些元素，说明已登录
                user_elements = page.query_selector_all('text="个人中心", text="消息", text="发布"')
                if user_elements:
                    return True
            except Exception:
                pass
            
            return True
            
        except Exception as e:
            self.logger.error(f"检查登录状态时出错: {str(e)}")
            return False

    def wait_for_login(self, page: Page) -> bool:
        """等待用户登录"""
        global should_exit
        
        print("\n请在浏览器中登录小红书账号...")
        print("提示：登录成功后会自动继续")
        print("等待登录中...")
        print("按 Ctrl+C 可以安全退出程序")
        
        # 最多等待5分钟
        max_wait_time = 300  # 秒
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time and not should_exit:
            try:
                # 检查登录状态
                if self.check_login_status(page):
                    print("\n检测到登录成功！")
                    # 确保页面完全加载
                    page.wait_for_load_state('networkidle')
                    # 如果不在发布页面，则跳转到发布页面
                    if not page.url.endswith('/publish'):
                        print("正在跳转到发布页面...")
                        page.goto('https://www.xiaohongshu.com/publish')
                        page.wait_for_load_state('networkidle')
                    return True
                
                # 每2秒检查一次
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"等待登录时出错: {str(e)}")
                time.sleep(2)
        
        if should_exit:
            print("\n用户取消登录")
        else:
            print("登录等待超时，请重新运行程序")
        return False

    def safe_close_browser(self, browser: Browser):
        """安全关闭浏览器"""
        try:
            if not should_exit:
                input("\n按回车键关闭浏览器...")
            browser.close()
        except Exception as e:
            self.logger.warning(f"关闭浏览器时发生错误: {str(e)}")

    def publish_note(self, 
                    title: str, 
                    content: str, 
                    images: List[str] = None, 
                    topics: List[str] = None):
        """
        发布小红书笔记
        :param title: 笔记标题
        :param content: 笔记内容
        :param images: 图片路径列表
        :param topics: 话题标签列表
        """
        global should_exit
        
        with sync_playwright() as p:
            browser = None
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                
                # 加载cookies
                cookies = self.load_cookies()
                if cookies:
                    try:
                        context.add_cookies(cookies)
                        self.logger.info("已加载保存的登录状态")
                    except Exception as e:
                        self.logger.error(f"加载 cookies 失败: {str(e)}")

                page = context.new_page()
                
                # 访问小红书发布页面
                self.logger.info("正在访问小红书发布页面...")
                page.goto('https://www.xiaohongshu.com/publish')
                page.wait_for_load_state('networkidle')

                # 检查是否需要登录
                if not self.check_login_status(page):
                    self.logger.info("需要登录小红书账号，等待用户登录...")
                    if not self.wait_for_login(page):
                        return False
                    
                    if should_exit:
                        return False
                    
                    # 保存登录后的cookies
                    self.logger.info("正在保存登录状态...")
                    self.save_cookies(context.cookies())
                    page.wait_for_load_state('networkidle')

                if should_exit:
                    return False

                self.logger.info("正在填写笔记内容...")
                
                # 输入标题
                title_selector = 'textarea[placeholder="填写标题会让更多人看到你的笔记"]'
                page.wait_for_selector(title_selector)
                page.fill(title_selector, title)
                self.logger.info(f"已填写标题: {title}")
                
                # 输入正文
                content_selector = 'div[contenteditable="true"]'
                page.wait_for_selector(content_selector)
                page.fill(content_selector, content)
                self.logger.info("已填写正文内容")

                # 上传图片
                if images and not should_exit:
                    self.logger.info("开始上传图片...")
                    for image_path in images:
                        if os.path.exists(image_path):
                            upload_button = page.get_by_text('图片')
                            page.wait_for_selector('input[type="file"]')
                            upload_button.click()
                            page.set_input_files('input[type="file"]', image_path)
                            self.logger.info(f"已上传图片: {image_path}")
                            time.sleep(2)  # 等待图片上传
                        else:
                            self.logger.warning(f"图片不存在: {image_path}")

                # 添加话题
                if topics and not should_exit:
                    self.logger.info("开始添加话题...")
                    for topic in topics:
                        topic_button = page.get_by_text('添加话题')
                        page.wait_for_selector('input[placeholder="搜索话题"]')
                        topic_button.click()
                        page.fill('input[placeholder="搜索话题"]', topic)
                        page.keyboard.press('Enter')
                        self.logger.info(f"已添加话题: {topic}")
                        time.sleep(1)

                if should_exit:
                    return False

                # 点击发布按钮
                self.logger.info("准备发布笔记...")
                publish_button = page.get_by_text('发布')
                page.wait_for_selector('text=发布')
                publish_button.click()
                page.wait_for_load_state('networkidle')

                # 保存最新的cookies
                self.save_cookies(context.cookies())
                
                self.logger.info("笔记发布成功")
                return True

            except Exception as e:
                self.logger.error(f"发布笔记失败: {str(e)}")
                return False
            
            finally:
                if browser:
                    self.safe_close_browser(browser)

def main():
    publisher = XiaohongshuPublisher()
    
    # 测试数据
    title = "测试笔记 - Python自动发布"
    content = "这是一个自动发布测试笔记，使用Python和Playwright实现。\n\n" \
             "测试时间：2024年测试\n" \
             "#Python #自动化 #测试"
    
    # 获取测试图片路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(os.path.dirname(current_dir), 'test_data')
    test_image_path = os.path.join(test_data_dir, 'test_image.jpg')
    
    publisher.publish_note(
        title=title,
        content=content,
        images=[test_image_path],
        topics=["Python", "自动化", "测试"]
    )

if __name__ == "__main__":
    main() 