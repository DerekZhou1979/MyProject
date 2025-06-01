#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主程序模块
整合各个模块，实现从Qwen-Max获取内容到小红书发布的完整流程
"""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime

# 添加当前目录到模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入自定义模块
from config import Config
from qwen import QwenClient
from xiaohongshu import XiaohongshuPublisher

def setup_logging(log_level="INFO"):
    """设置日志记录
    
    Args:
        log_level: 日志级别
    """
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # 设置日志格式
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    # 设置日志级别
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    
    # 配置日志记录器
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    
    logging.info(f"日志记录已设置，级别: {log_level}, 文件: {log_file}")

def parse_arguments():
    """解析命令行参数
    
    Returns:
        解析后的参数
    """
    parser = argparse.ArgumentParser(description="Qwen-Max到小红书自动化脚本")
    
    parser.add_argument(
        "--config", 
        type=str, 
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--topic", 
        type=str, 
        help="指定内容主题，覆盖配置文件中的设置"
    )
    
    parser.add_argument(
        "--check-only", 
        action="store_true", 
        help="仅检查配置和登录状态，不执行发布"
    )
    
    parser.add_argument(
        "--generate-only", 
        action="store_true", 
        help="仅生成内容，不执行发布"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str, 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO", 
        help="日志级别"
    )
    
    return parser.parse_args()

def check_environment():
    """检查运行环境
    
    Returns:
        环境检查结果
    """
    try:
        # 检查Python版本
        python_version = sys.version.split()[0]
        logging.info(f"Python版本: {python_version}")
        
        # 检查必要的模块
        required_modules = ["requests", "playwright"]
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            logging.error(f"缺少必要的模块: {', '.join(missing_modules)}")
            logging.info("请使用以下命令安装缺少的模块:")
            logging.info(f"pip install {' '.join(missing_modules)}")
            return False
        
        # 检查Playwright浏览器
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                browser.close()
        except Exception as e:
            logging.error(f"Playwright浏览器检查失败: {e}")
            logging.info("请使用以下命令安装Playwright浏览器:")
            logging.info("playwright install chromium")
            return False
        
        return True
    except Exception as e:
        logging.error(f"环境检查失败: {e}")
        return False

def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 设置日志记录
    setup_logging(args.log_level)
    
    logging.info("=== Qwen-Max到小红书自动化脚本启动 ===")
    
    try:
        # 检查运行环境
        if not check_environment():
            logging.error("环境检查失败，脚本终止")
            return 1
        
        # 加载配置
        config = Config(args.config)
        
        # 如果命令行指定了日志级别，覆盖配置文件中的设置
        if args.log_level:
            config.set("runtime", "log_level", args.log_level)
            setup_logging(args.log_level)
        
        # 创建Qwen-Max客户端
        qwen_client = QwenClient(config)
        
        # 创建小红书发布客户端
        xiaohongshu_publisher = XiaohongshuPublisher(config)
        
        # 如果仅检查配置和登录状态
        if args.check_only:
            logging.info("仅检查配置和登录状态")
            
            # 检查Qwen-Max API密钥
            api_key = config.get("qwen", "api_key")
            if not api_key:
                logging.error("Qwen-Max API密钥未设置")
            else:
                logging.info("Qwen-Max API密钥已设置")
            
            # 检查小红书登录状态
            login_status = xiaohongshu_publisher.check_login_status()
            logging.info(f"小红书登录状态: {login_status['status']} - {login_status['message']}")
            
            return 0
        
        # 生成内容
        topic = args.topic
        logging.info(f"开始生成内容，主题: {topic if topic else '从配置中获取'}")
        content = qwen_client.generate_content(topic)
        logging.info(f"内容生成成功: {content['title']}")
        logging.info(f"内容生成-标签成功: {content['tags']}")    
        
        # 如果仅生成内容
        if args.generate_only:
            logging.info("仅生成内容，不执行发布")
            logging.info(f"生成的内容已保存")
            return 0
        
        # 发布内容到小红书
        logging.info("开始发布内容到小红书")
        result = xiaohongshu_publisher.publish_content(content)
        
        if result["status"] == "success":
            logging.info(f"内容发布成功: {result.get('result', {}).get('url', '未获取到URL')}")
        else:
            logging.error(f"内容发布失败: {result['message']}")
            return 1
        
        logging.info("=== 脚本执行完成 ===")
        return 0
        
    except Exception as e:
        logging.error(f"脚本执行失败: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
