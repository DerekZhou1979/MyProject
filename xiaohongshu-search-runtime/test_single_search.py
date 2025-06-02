#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简化的单个搜索测试
"""

import os
import sys
import time
import logging
from crawler import XiaoHongShuCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_single_search(keyword="美食推荐"):
    """测试单个关键词搜索"""
    
    cookies_file = os.path.join('cache', 'xiaohongshu_cookies.json')
    
    # 检查cookies文件是否存在
    if not os.path.exists(cookies_file):
        logger.error(f"Cookie文件不存在: {cookies_file}")
        logger.info("请先运行 python cookie_manager.py login 进行登录")
        return False
    
    logger.info(f"🔍 测试搜索关键词: '{keyword}'")
    
    crawler = None
    try:
        # 初始化爬虫
        crawler = XiaoHongShuCrawler(
            use_selenium=True,
            headless=False,  # 显示浏览器以便观察
            cookies_file=cookies_file,
            load_cookies=True
        )
        
        # 执行搜索
        logger.info(f"开始搜索: {keyword}")
        start_time = time.time()
        results = crawler.search(keyword, max_results=3, use_cache=False)
        search_time = time.time() - start_time
        
        logger.info(f"⏱️  搜索耗时: {search_time:.2f} 秒")
        logger.info(f"📊 搜索结果数量: {len(results)}")
        
        if results:
            logger.info("✅ 搜索成功！")
            
            # 显示结果
            for i, note in enumerate(results, 1):
                logger.info(f"  {i}. 标题: {note.get('title', '无标题')}")
                logger.info(f"     ID: {note.get('id', 'N/A')}")
                logger.info(f"     URL: {note.get('url', 'N/A')}")
                logger.info("")
                
            return True
        else:
            logger.warning("❌ 搜索无结果")
            
            # 检查缓存目录
            cache_dir = crawler.cache_dir if crawler else 'cache'
            if os.path.exists(cache_dir):
                files = os.listdir(cache_dir)
                
                # 检查是否有错误截图
                error_screenshots = [f for f in files if 'failed' in f and f.endswith('.png')]
                if error_screenshots:
                    latest = max(error_screenshots, key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
                    logger.info(f"📷 错误截图: {latest}")
                
                # 检查页面源码
                html_files = [f for f in files if f.startswith('page_source_')]
                if html_files:
                    latest = max(html_files, key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
                    logger.info(f"📄 页面源码: {latest}")
            
            return False
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {str(e)}")
        logger.error("详细错误信息:", exc_info=True)
        return False
    
    finally:
        # 确保关闭浏览器
        if crawler:
            try:
                crawler.close()
            except:
                pass

if __name__ == "__main__":
    # 可以通过命令行参数指定搜索关键词
    keyword = sys.argv[1] if len(sys.argv) > 1 else "美食推荐"
    
    logger.info("🚀 小红书单个搜索测试")
    logger.info("=" * 50)
    
    success = test_single_search(keyword)
    
    if success:
        logger.info("\n✅ 测试成功！")
    else:
        logger.info("\n❌ 测试失败！")
        sys.exit(1) 