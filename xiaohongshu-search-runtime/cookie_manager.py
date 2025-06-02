#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书Cookie管理工具
功能：提供独立的Cookie获取、验证和管理功能
版本：2.0
"""

import os
import sys
import json
import logging
import traceback
import argparse
from datetime import datetime
from crawler import XiaoHongShuCrawler

# 配置日志系统
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CookieManager:
    """Cookie管理器类"""
    
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
        self.cookies_file = os.path.join(self.cache_dir, 'xiaohongshu_cookies.json')
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def login_and_save(self):
        """登录并保存Cookie"""
        print("=" * 60)
        print("🔑 小红书登录工具")
        print("=" * 60)
        print("📝 说明：")
        print("  • 此工具将打开浏览器进行登录")
        print("  • 支持扫码登录和密码登录")
        print("  • 登录成功后将自动保存Cookie")
        print("  • Cookie用于后续免登录访问")
        print("")
        print(f"📁 Cookie保存路径: {self.cookies_file}")
        print("=" * 60)
        
        if not self._confirm_action("是否开始登录"):
            return False
        
        try:
            # 创建浏览器实例进行登录
            logger.info("正在启动浏览器...")
            crawler = XiaoHongShuCrawler(
                use_selenium=True, 
                headless=False, 
                cookies_file=self.cookies_file,
                load_cookies=False  # 登录模式不加载旧Cookie
            )
            
            # 开始登录流程
            logger.info("开始登录流程...")
            success = crawler.login()
            
            if success:
                print("=" * 60)
                print("✅ 登录成功！")
                print(f"📁 Cookie已保存至: {self.cookies_file}")
                print("=" * 60)
                print("💡 提示：现在可以运行 python main.py 启动服务")
                self._display_cookie_info()
            else:
                print("=" * 60)
                print("❌ 登录失败或超时！")
                print("💡 可能的解决方案：")
                print("   - 检查网络连接")
                print("   - 重新尝试登录")
                print("   - 确保Chrome浏览器正常")
                print("=" * 60)
            
            # 关闭浏览器
            crawler.close()
            return success
            
        except Exception as e:
            logger.error(f"登录过程发生错误: {str(e)}")
            print("=" * 60)
            print("❌ 登录过程出错")
            print(f"错误信息: {str(e)}")
            print("")
            print("💡 解决建议：")
            print("   - 确保已安装Chrome浏览器")
            print("   - 检查是否有其他程序占用")
            print("   - 重启程序重试")
            print("=" * 60)
            traceback.print_exc()
            return False
    
    def verify_cookies(self):
        """验证现有Cookie是否有效"""
        if not os.path.exists(self.cookies_file):
            print(f"❌ Cookie文件不存在: {self.cookies_file}")
            return False
        
        print("=" * 60)
        print("🔍 Cookie验证工具")
        print("=" * 60)
        
        try:
            # 加载Cookie信息
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            print(f"📁 Cookie文件: {self.cookies_file}")
            print(f"📊 Cookie数量: {len(cookies)}")
            
            # 显示Cookie详情
            self._display_cookie_info()
            
            # 使用Cookie进行验证测试
            print("\n🔄 正在验证Cookie有效性...")
            crawler = XiaoHongShuCrawler(
                use_selenium=True,
                headless=False,  # 显示浏览器以便查看结果
                cookies_file=self.cookies_file,
                load_cookies=True
            )
            
            # 访问小红书首页验证
            driver = crawler.driver
            driver.get("https://www.xiaohongshu.com")
            
            # 等待页面加载
            import time
            time.sleep(3)
            
            # 保存验证截图
            screenshot_path = os.path.join(self.cache_dir, f"cookie_verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            driver.save_screenshot(screenshot_path)
            
            print(f"📸 验证截图已保存: {screenshot_path}")
            print("👀 请查看浏览器页面确认登录状态")
            
            input("按回车键关闭浏览器...")
            crawler.close()
            
            print("✅ Cookie验证完成")
            return True
            
        except Exception as e:
            print(f"❌ Cookie验证失败: {str(e)}")
            traceback.print_exc()
            return False
    
    def delete_cookies(self):
        """删除Cookie文件"""
        if not os.path.exists(self.cookies_file):
            print("ℹ️   Cookie文件不存在，无需删除")
            return True
        
        print("=" * 60)
        print("🗑️  删除Cookie")
        print("=" * 60)
        print(f"📁 目标文件: {self.cookies_file}")
        
        if not self._confirm_action("确认删除Cookie文件"):
            return False
        
        try:
            os.remove(self.cookies_file)
            print("✅ Cookie文件已删除")
            return True
        except Exception as e:
            print(f"❌ 删除Cookie文件失败: {str(e)}")
            return False
    
    def _display_cookie_info(self):
        """显示Cookie信息"""
        try:
            if not os.path.exists(self.cookies_file):
                print("ℹ️  暂无Cookie信息")
                return
            
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            # 获取文件时间信息
            file_stat = os.stat(self.cookies_file)
            create_time = datetime.fromtimestamp(file_stat.st_ctime)
            modify_time = datetime.fromtimestamp(file_stat.st_mtime)
            
            print("\n📊 Cookie详细信息：")
            print(f"   文件路径: {self.cookies_file}")
            print(f"   创建时间: {create_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   修改时间: {modify_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Cookie数量: {len(cookies)}")
            
            # 显示重要Cookie
            important_cookies = ['web_session', 'webId', 'gid', 'sec_poison_id']
            found_important = [cookie['name'] for cookie in cookies if cookie['name'] in important_cookies]
            
            if found_important:
                print(f"   重要Cookie: {', '.join(found_important)}")
            
        except Exception as e:
            logger.warning(f"显示Cookie信息失败: {str(e)}")
    
    def _confirm_action(self, message):
        """确认操作"""
        while True:
            choice = input(f"{message}？(y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("请输入 y 或 n")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="小红书Cookie管理工具")
    parser.add_argument('action', choices=['login', 'verify', 'delete', 'info'],
                       help='操作类型: login(登录), verify(验证), delete(删除), info(信息)')
    
    args = parser.parse_args()
    
    manager = CookieManager()
    
    try:
        if args.action == 'login':
            success = manager.login_and_save()
            return 0 if success else 1
        elif args.action == 'verify':
            success = manager.verify_cookies()
            return 0 if success else 1
        elif args.action == 'delete':
            success = manager.delete_cookies()
            return 0 if success else 1
        elif args.action == 'info':
            manager._display_cookie_info()
            return 0
    except KeyboardInterrupt:
        print("\n⏹️  操作已取消")
        return 0
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 