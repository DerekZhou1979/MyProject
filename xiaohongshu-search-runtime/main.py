#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书搜索服务主启动程序
功能：自动完成登录流程并启动Web服务
作者：系统生成
版本：2.0
"""

import os
import sys
import logging
import signal

# 确保能找到app模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app, init_crawler_with_login, cleanup

# 配置日志系统
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    """处理系统信号，优雅关闭服务"""
    logger.info(f"接收到信号 {signum}，正在关闭服务...")
    cleanup()
    sys.exit(0)

def create_necessary_dirs():
    """创建必要的目录结构"""
    directories = ['cache', 'img']
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"确保目录存在: {directory}")
        except Exception as e:
            logger.error(f"创建目录 {directory} 失败: {e}")
            return False
    return True

def display_welcome_message():
    """显示欢迎信息"""
    print("=" * 60)
    print("🔍 小红书搜索服务")
    print("=" * 60)
    print("📋 功能说明：")
    print("  • 自动登录小红书账号")
    print("  • 提供搜索API服务")
    print("  • 支持热门笔记查询")
    print("")
    print("📝 使用说明：")
    print("  1. 程序将自动打开浏览器")
    print("  2. 请在浏览器中完成小红书登录")
    print("  3. 支持扫码登录或手机号+密码登录")
    print("  4. 登录成功后浏览器将自动关闭")
    print("  5. 服务启动后访问 http://localhost:8080")
    print("=" * 60)

def main():
    """主启动函数"""
    try:
        # 注册信号处理器
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # 显示欢迎信息
        display_welcome_message()
        
        # 创建必要目录
        if not create_necessary_dirs():
            logger.error("初始化目录结构失败")
            return 1
        
        # 等待用户确认
        input("按回车键开始启动服务...")
        
        # 初始化爬虫服务
        logger.info("正在初始化小红书搜索服务...")
        success = init_crawler_with_login()
        
        if not success:
            logger.error("❌ 登录失败，服务启动中止")
            logger.error("💡 请检查以下项目：")
            logger.error("   - 网络连接是否正常")
            logger.error("   - Chrome浏览器是否已安装")
            logger.error("   - 小红书登录是否成功")
            return 1
        
        # 显示启动成功信息
        print("=" * 60)
        print("✅ 登录成功！服务正在启动...")
        print("🌐 访问地址: http://localhost:8080")
        print("⚠️  按 Ctrl+C 停止服务")
        print("=" * 60)
        
        # 启动Flask Web服务
        app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("⏹️  用户手动停止服务")
        cleanup()
        return 0
    except Exception as e:
        logger.error(f"❌ 服务启动失败: {str(e)}")
        logger.debug("详细错误信息：", exc_info=True)
        cleanup()
        return 1

if __name__ == '__main__':
    sys.exit(main()) 