#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
登录功能测试脚本
用于测试新的自动登录流程
"""

import logging
import os
from crawler import XiaoHongShuCrawler

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_login():
    """测试登录功能"""
    
    print("=" * 60)
    print("小红书登录功能测试")
    print("=" * 60)
    print("此测试将打开浏览器进行登录测试")
    print("请在浏览器中完成登录操作")
    print("=" * 60)
    
    input("按回车键开始测试...")
    
    try:
        # 确保cache目录存在
        os.makedirs('cache', exist_ok=True)
        
        # 创建爬虫实例（不加载cookies，用于登录）
        logger.info("创建爬虫实例...")
        crawler = XiaoHongShuCrawler(
            use_selenium=True,
            headless=False,  # 不使用无头模式
            cookies_file=None,
            load_cookies=False
        )
        
        # 执行登录
        logger.info("开始登录流程...")
        success = crawler.login()
        
        if success:
            print("=" * 60)
            print("登录测试成功！")
            print("Cookies已保存到文件")
            print("=" * 60)
            
            # 保存cookies
            cookies_file = os.path.join('cache', 'xiaohongshu_cookies.json')
            crawler.save_cookies(cookies_file)
            
            # 测试使用保存的cookies创建新的爬虫实例
            logger.info("测试使用保存的cookies...")
            crawler.close()
            
            # 创建新的爬虫实例使用cookies
            test_crawler = XiaoHongShuCrawler(
                use_selenium=True,
                headless=True,  # 使用无头模式
                cookies_file=cookies_file,
                load_cookies=True
            )
            
            logger.info("测试搜索功能...")
            # 简单测试搜索
            notes = test_crawler.search("口红", max_results=3, use_cache=False)
            
            if notes:
                print(f"搜索测试成功！找到 {len(notes)} 条笔记")
                for i, note in enumerate(notes, 1):
                    print(f"{i}. {note.get('title', '无标题')}")
            else:
                print("搜索测试失败，可能需要重新登录")
            
            test_crawler.close()
            
        else:
            print("=" * 60)
            print("登录测试失败！")
            print("请检查网络连接和浏览器")
            print("=" * 60)
            crawler.close()
            return False
        
        crawler.close()
        return True
        
    except Exception as e:
        logger.error(f"测试过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_login()
    if success:
        print("\n测试完成！可以使用 python app.py 启动正式服务")
    else:
        print("\n测试失败！请检查错误信息") 