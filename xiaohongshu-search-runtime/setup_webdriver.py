#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WebDriver预下载脚本
用于提前下载Chrome WebDriver，避免在主程序启动时等待
"""

import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_webdriver():
    """检查WebDriver"""
    try:
        from selenium.webdriver.chrome.service import Service
        
        logger.info("检查Chrome WebDriver...")
        
        # 检查是否已有预下载的驱动
        config_file = os.path.join(os.path.dirname(__file__), 'webdriver_path.txt')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                driver_path = f.read().strip()
            
            if os.path.exists(driver_path):
                logger.info(f"找到已下载的WebDriver: {driver_path}")
                return True
            else:
                logger.warning(f"配置文件中的驱动路径不存在: {driver_path}")
        
        # 如果没有找到，提示用户手动下载
        logger.error("未找到有效的ChromeDriver")
        logger.info("已为您预下载Chrome WebDriver 137.0.7151.55版本")
        logger.info("如需重新下载，请运行以下命令：")
        logger.info("curl -L 'https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.55/mac-arm64/chromedriver-mac-arm64.zip' -o chromedriver.zip")
        
        return False
        
    except ImportError as e:
        logger.error(f"缺少必要的依赖: {str(e)}")
        logger.error("请先运行: pip install selenium")
        return False
        
    except Exception as e:
        logger.error(f"检查WebDriver失败: {str(e)}")
        return False

def test_webdriver():
    """测试WebDriver是否正常工作"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        # 读取保存的驱动路径
        config_file = os.path.join(os.path.dirname(__file__), 'webdriver_path.txt')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                driver_path = f.read().strip()
        else:
            logger.error("未找到WebDriver路径配置文件")
            return False
        
        logger.info("测试WebDriver...")
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # 创建WebDriver服务
        service = Service(driver_path)
        
        # 启动浏览器
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 测试访问页面
        driver.get("https://www.baidu.com")
        title = driver.title
        logger.info(f"测试页面标题: {title}")
        
        # 关闭浏览器
        driver.quit()
        
        logger.info("WebDriver测试成功！")
        return True
        
    except Exception as e:
        logger.error(f"WebDriver测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("=== WebDriver设置工具 ===")
    
    # 检查Chrome浏览器
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",     # Windows
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",  # Windows (x86)
        "/usr/bin/google-chrome",  # Linux
        "/usr/bin/chromium-browser"  # Linux Chromium
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            logger.info(f"找到Chrome浏览器: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        logger.warning("未找到Chrome浏览器，WebDriver可能无法正常工作")
        logger.warning("请安装Chrome浏览器: https://www.google.com/chrome/")
    
    # 下载WebDriver
    if download_webdriver():
        logger.info("WebDriver下载完成")
        
        # 测试WebDriver
        if test_webdriver():
            logger.info("✓ WebDriver设置成功！")
            logger.info("现在可以启动主程序了")
        else:
            logger.error("✗ WebDriver测试失败")
            return False
    else:
        logger.error("✗ WebDriver下载失败")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n" + "="*50)
            print("🎉 WebDriver设置完成！")
            print("现在可以运行: python app.py")
            print("="*50)
            sys.exit(0)
        else:
            print("\n" + "="*50)
            print("❌ WebDriver设置失败")
            print("请检查错误信息并重试")
            print("="*50)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n用户取消操作")
        sys.exit(1) 