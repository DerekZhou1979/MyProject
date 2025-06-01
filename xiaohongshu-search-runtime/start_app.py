#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书搜索服务启动脚本
自动完成登录流程并启动服务
"""

import os
import sys
import logging

# 确保能找到app模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app import app, init_crawler_with_login, cleanup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    try:
        # 创建必要的目录
        os.makedirs('cache', exist_ok=True)
        os.makedirs('img', exist_ok=True)
        
        print("=" * 60)
        print("小红书搜索服务")
        print("=" * 60)
        print("注意：程序将打开浏览器进行小红书登录")
        print("请在浏览器中完成登录（支持扫码或密码登录）")
        print("登录成功后，浏览器将自动关闭，服务将启动")
        print("=" * 60)
        
        input("按回车键开始...")
        
        # 启动时强制执行登录流程
        logger.info("开始初始化服务...")
        success = init_crawler_with_login()
        
        if not success:
            logger.error("登录失败，无法启动服务")
            logger.error("请检查网络连接和Chrome浏览器安装情况")
            return 1
        
        print("=" * 60)
        print("登录成功！服务正在启动...")
        print("访问地址: http://localhost:8080")
        print("按 Ctrl+C 停止服务")
        print("=" * 60)
        
        # 启动Flask服务
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        logger.info("服务已停止")
        cleanup()
        return 0
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        cleanup()
        return 1

if __name__ == '__main__':
    sys.exit(main()) 