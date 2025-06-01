¬#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书cookie验证工具
用于测试cookie是否有效
"""

import os
import json
import time
import logging
from crawler import XiaoHongShuCrawler

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 获取cookie文件路径
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    cookies_file = os.path.join(cache_dir, 'xiaohongshu_cookies.json')
    
    if not os.path.exists(cookies_file):
        print(f"错误: Cookie文件不存在: {cookies_file}")
        return 1
    
    print("=" * 60)
    print("小红书Cookie验证工具")
    print("=" * 60)
    print(f"Cookie文件: {cookies_file}")
    
    # 加载cookie
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        print(f"成功加载 {len(cookies)} 个cookie:")
        for cookie in cookies:
            print(f"  - {cookie.get('name', 'unknown')}: {cookie.get('value', '')[:10]}...")
    except Exception as e:
        print(f"加载cookie文件失败: {str(e)}")
        return 1
    
    # 创建爬虫实例
    print("\n正在使用cookie测试小红书访问...")
    crawler = XiaoHongShuCrawler(use_selenium=True, headless=False, cookies_file=cookies_file)
    
    # 访问小红书首页，检查是否已登录
    try:
        # 获取爬虫的浏览器实例
        driver = crawler.driver
        if not driver:
            print("初始化Selenium失败，无法测试")
            return 1
        
        # 访问小红书首页
        driver.get("https://www.xiaohongshu.com")
        print("已打开小红书首页，等待加载...")
        time.sleep(5)
        
        # 保存页面截图
        screenshot_path = os.path.join(cache_dir, "login_test.png")
        driver.save_screenshot(screenshot_path)
        print(f"已保存页面截图: {screenshot_path}")
        
        # 检查是否有登录按钮或个人头像信息
        page_source = driver.page_source
        
        # 保存页面源码供分析
        source_path = os.path.join(cache_dir, "login_test.html")
        with open(source_path, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"已保存页面源码: {source_path}")
        
        # 检查是否已登录
        if "登录" in page_source or "注册" in page_source:
            # 可能未登录
            print("\n【测试结果】: Cookie可能失效，页面中仍包含'登录'或'注册'按钮")
            print("建议: 重新获取cookie或者手动检查截图和页面源码")
        elif "我的" in page_source or "消息" in page_source:
            # 可能已登录
            print("\n【测试结果】: Cookie有效，页面中包含已登录用户才能看到的元素")
            print("建议: 查看截图进一步确认")
        else:
            # 不确定状态
            print("\n【测试结果】: 无法确定登录状态，请查看截图和页面源码进行分析")
        
        # 输出截图和源码路径
        print(f"\n页面截图: {screenshot_path}")
        print(f"页面源码: {source_path}")
        
        # 关闭浏览器
        driver.quit()
        print("\n测试完成，浏览器已关闭")
        
    except Exception as e:
        print(f"测试过程出错: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 