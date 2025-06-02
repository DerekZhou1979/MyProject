#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试改进后的搜索功能
"""

import os
import sys
import time
import logging
from crawler import XiaoHongShuCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_search.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def test_search_with_improved_logic():
    """测试改进后的搜索逻辑"""
    
    cookies_file = os.path.join('cache', 'xiaohongshu_cookies.json')
    
    # 检查cookies文件是否存在
    if not os.path.exists(cookies_file):
        logger.error(f"Cookie文件不存在: {cookies_file}")
        logger.info("请先运行 python cookie_manager.py login 进行登录")
        return False
    
    logger.info("🔍 开始测试改进后的搜索功能...")
    
    try:
        # 初始化爬虫
        crawler = XiaoHongShuCrawler(
            use_selenium=True,
            headless=False,  # 显示浏览器以便观察
            cookies_file=cookies_file,
            load_cookies=True
        )
        
        # 测试关键词
        test_keywords = [
            "美食推荐",
            "护肤心得", 
            "旅行攻略"
        ]
        
        for i, keyword in enumerate(test_keywords, 1):
            logger.info(f"\n📝 测试 {i}: 搜索关键词 '{keyword}'")
            logger.info("=" * 50)
            
            try:
                # 执行搜索
                start_time = time.time()
                results = crawler.search(keyword, max_results=5, use_cache=False)
                search_time = time.time() - start_time
                
                logger.info(f"⏱️  搜索耗时: {search_time:.2f} 秒")
                logger.info(f"📊 搜索结果数量: {len(results)}")
                
                if results:
                    logger.info("✅ 搜索成功！")
                    
                    # 显示前3个结果
                    for j, note in enumerate(results[:3], 1):
                        logger.info(f"  {j}. 标题: {note.get('title', '无标题')[:50]}")
                        logger.info(f"     ID: {note.get('id', 'N/A')}")
                        logger.info(f"     封面: {'有' if note.get('cover') else '无'}")
                        logger.info(f"     URL: {note.get('url', 'N/A')[:80]}")
                        logger.info("")
                else:
                    logger.warning("❌ 搜索无结果")
                    
                    # 检查是否有错误截图
                    cache_dir = crawler.cache_dir
                    error_screenshots = [f for f in os.listdir(cache_dir) 
                                       if f.startswith('search_failed_') and f.endswith('.png')]
                    
                    if error_screenshots:
                        latest_screenshot = max(error_screenshots, 
                                              key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
                        logger.info(f"📷 已保存错误截图: {latest_screenshot}")
                    
                    # 检查页面源码
                    page_sources = [f for f in os.listdir(cache_dir) 
                                   if f.startswith('page_source_') and f.endswith('.html')]
                    
                    if page_sources:
                        latest_source = max(page_sources, 
                                          key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
                        logger.info(f"📄 已保存页面源码: {latest_source}")
                
                # 等待一下再进行下一次搜索
                if i < len(test_keywords):
                    logger.info("⏳ 等待 3 秒后进行下一次搜索...")
                    time.sleep(3)
                    
            except Exception as e:
                logger.error(f"❌ 搜索关键词 '{keyword}' 时出错: {str(e)}")
                logger.error("详细错误信息:", exc_info=True)
        
        logger.info("\n🎯 测试完成!")
        
        # 显示缓存文件状态
        cache_dir = crawler.cache_dir
        cache_files = os.listdir(cache_dir)
        
        logger.info(f"\n📁 缓存目录文件: {len(cache_files)} 个")
        
        # 分类统计
        screenshots = len([f for f in cache_files if f.endswith('.png')])
        html_files = len([f for f in cache_files if f.endswith('.html')])
        json_files = len([f for f in cache_files if f.endswith('.json')])
        
        logger.info(f"   📷 截图文件: {screenshots} 个")
        logger.info(f"   📄 HTML文件: {html_files} 个") 
        logger.info(f"   📋 JSON文件: {json_files} 个")
        
        # 关闭浏览器
        crawler.close()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {str(e)}")
        logger.error("详细错误信息:", exc_info=True)
        return False

def analyze_search_results():
    """分析搜索结果和截图"""
    logger.info("\n🔍 分析搜索结果...")
    
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    
    if not os.path.exists(cache_dir):
        logger.warning("缓存目录不存在")
        return
    
    files = os.listdir(cache_dir)
    
    # 分析截图文件
    success_screenshots = [f for f in files if f.startswith('search_success_')]
    failed_screenshots = [f for f in files if f.startswith('search_failed_')]
    error_screenshots = [f for f in files if f.startswith('search_error_')]
    
    logger.info(f"✅ 成功搜索截图: {len(success_screenshots)} 个")
    logger.info(f"❌ 失败搜索截图: {len(failed_screenshots)} 个")
    logger.info(f"🚨 错误搜索截图: {len(error_screenshots)} 个")
    
    # 显示最新的截图文件
    all_screenshots = success_screenshots + failed_screenshots + error_screenshots
    if all_screenshots:
        latest_screenshot = max(all_screenshots, 
                              key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
        logger.info(f"📷 最新截图: {latest_screenshot}")
        
        # 显示截图文件的修改时间
        screenshot_path = os.path.join(cache_dir, latest_screenshot)
        mtime = os.path.getmtime(screenshot_path)
        import datetime
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"   时间: {mtime_str}")
    
    # 分析页面源码文件
    html_files = [f for f in files if f.startswith('page_source_')]
    logger.info(f"📄 页面源码文件: {len(html_files)} 个")
    
    if html_files:
        latest_html = max(html_files, 
                         key=lambda x: os.path.getctime(os.path.join(cache_dir, x)))
        logger.info(f"📄 最新页面源码: {latest_html}")
        
        # 简单分析HTML内容
        html_path = os.path.join(cache_dir, latest_html)
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查关键词
            has_error_indicators = any(indicator in content for indicator in [
                "你访问页面不见了", "页面不见了", "请返回上一页",
                "验证", "登录", "请完成下列验证"
            ])
            
            has_content_indicators = any(indicator in content for indicator in [
                "/explore/", "笔记", "小红书", "note-item", "feed-item"
            ])
            
            logger.info(f"   包含错误指示器: {'是' if has_error_indicators else '否'}")
            logger.info(f"   包含内容指示器: {'是' if has_content_indicators else '否'}")
            
        except Exception as e:
            logger.warning(f"读取HTML文件失败: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 小红书搜索功能测试")
    logger.info("=" * 60)
    
    # 运行测试
    success = test_search_with_improved_logic()
    
    # 分析结果
    analyze_search_results()
    
    if success:
        logger.info("\n✅ 测试完成！")
    else:
        logger.info("\n❌ 测试失败！")
        sys.exit(1) 