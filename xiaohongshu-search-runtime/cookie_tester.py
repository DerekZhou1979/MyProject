#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书Cookie验证测试工具
功能：测试已保存的Cookie是否有效
版本：2.0
"""

import os
import json
import time
import logging
import sys
from datetime import datetime
from crawler import XiaoHongShuCrawler

# 配置日志系统
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CookieTester:
    """Cookie测试器类"""
    
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
        self.cookies_file = os.path.join(self.cache_dir, 'xiaohongshu_cookies.json')
    
    def test_cookies(self, headless=False):
        """测试Cookie有效性"""
        if not os.path.exists(self.cookies_file):
            print(f"❌ Cookie文件不存在: {self.cookies_file}")
            print("💡 请先运行: python cookie_manager.py login")
            return False
        
        print("=" * 60)
        print("🧪 小红书Cookie测试工具")
        print("=" * 60)
        print(f"📁 Cookie文件: {self.cookies_file}")
        
        # 加载并显示Cookie信息
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            print(f"📊 Cookie数量: {len(cookies)}")
            
            # 显示重要Cookie
            important_cookies = ['web_session', 'webId', 'gid', 'sec_poison_id']
            found_important = [cookie['name'] for cookie in cookies if cookie['name'] in important_cookies]
            
            if found_important:
                print(f"🔑 重要Cookie: {', '.join(found_important)}")
            
        except Exception as e:
            print(f"❌ 加载Cookie文件失败: {str(e)}")
            return False
        
        # 创建爬虫实例进行测试
        print("\n🔄 正在使用Cookie测试小红书访问...")
        
        try:
            crawler = XiaoHongShuCrawler(
                use_selenium=True, 
                headless=headless, 
                cookies_file=self.cookies_file,
                load_cookies=True
            )
            
            if not crawler.driver:
                print("❌ 初始化浏览器失败，无法测试")
                return False
            
            # 访问小红书首页
            print("🌐 正在访问小红书首页...")
            crawler.driver.get("https://www.xiaohongshu.com")
            time.sleep(5)  # 等待页面加载
            
            # 保存测试结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = os.path.join(self.cache_dir, f"cookie_test_{timestamp}.png")
            source_path = os.path.join(self.cache_dir, f"cookie_test_{timestamp}.html")
            
            # 保存页面截图
            crawler.driver.save_screenshot(screenshot_path)
            print(f"📸 页面截图已保存: {screenshot_path}")
            
            # 保存页面源码
            page_source = crawler.driver.page_source
            with open(source_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"📄 页面源码已保存: {source_path}")
            
            # 分析登录状态
            login_status = self._analyze_login_status(page_source)
            
            # 显示测试结果
            print("\n" + "=" * 60)
            print("📋 测试结果分析")
            print("=" * 60)
            
            if login_status == "logged_in":
                print("✅ Cookie有效 - 已成功登录")
                print("💡 页面包含已登录用户的专属内容")
            elif login_status == "not_logged_in":
                print("❌ Cookie失效 - 未登录状态")
                print("💡 建议重新获取Cookie")
            else:
                print("⚠️  登录状态不明确")
                print("💡 请查看截图和页面源码进行人工确认")
            
            print(f"\n📁 测试文件:")
            print(f"   截图: {screenshot_path}")
            print(f"   源码: {source_path}")
            
            if not headless:
                print("\n👀 请查看浏览器页面确认登录状态")
                input("按回车键关闭浏览器...")
            
            # 关闭浏览器
            crawler.close()
            
            return login_status == "logged_in"
            
        except Exception as e:
            print(f"❌ 测试过程出错: {str(e)}")
            logger.error("详细错误信息：", exc_info=True)
            return False
    
    def _analyze_login_status(self, page_source):
        """分析页面源码判断登录状态"""
        # 登录状态的关键词
        logged_in_keywords = [
            "我的", "消息", "收藏", "关注", "粉丝", 
            "个人中心", "设置", "退出登录"
        ]
        
        # 未登录状态的关键词
        not_logged_in_keywords = [
            "登录", "注册", "手机号", "验证码", 
            "扫码登录", "密码登录"
        ]
        
        # 统计关键词出现次数
        logged_in_count = sum(1 for keyword in logged_in_keywords if keyword in page_source)
        not_logged_in_count = sum(1 for keyword in not_logged_in_keywords if keyword in page_source)
        
        logger.debug(f"已登录关键词数量: {logged_in_count}")
        logger.debug(f"未登录关键词数量: {not_logged_in_count}")
        
        # 判断登录状态
        if logged_in_count > not_logged_in_count and logged_in_count >= 2:
            return "logged_in"
        elif not_logged_in_count > logged_in_count and not_logged_in_count >= 2:
            return "not_logged_in"
        else:
            return "unknown"

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书Cookie测试工具")
    parser.add_argument('--headless', action='store_true', 
                       help='使用无头模式运行（不显示浏览器窗口）')
    
    args = parser.parse_args()
    
    tester = CookieTester()
    
    try:
        success = tester.test_cookies(headless=args.headless)
        
        if success:
            print("\n🎉 Cookie测试通过！可以正常使用服务")
            return 0
        else:
            print("\n❌ Cookie测试失败！请重新获取Cookie")
            print("💡 运行命令: python cookie_manager.py login")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  测试已取消")
        return 0
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 