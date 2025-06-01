#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初始化模块
用于初始化项目环境和依赖
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def init_environment():
    """初始化运行环境
    
    安装必要的依赖包和设置环境
    
    Returns:
        初始化结果
    """
    try:
        logging.info("开始初始化环境...")
        
        # 获取当前脚本所在目录
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        project_dir = current_dir.parent
        
        # 创建必要的目录
        dirs = ["logs", "contents"]
        for dir_name in dirs:
            dir_path = project_dir / dir_name
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"创建目录: {dir_path}")
        
        # 安装依赖包
        logging.info("安装依赖包...")
        requirements = [
            "requests",
            "playwright"
        ]
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade"] + requirements)
        
        # 安装Playwright浏览器
        logging.info("安装Playwright浏览器...")
        try:
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        except Exception as e:
            logging.error(f"安装Playwright浏览器失败: {e}")
            logging.info("请手动运行: playwright install chromium")
        
        logging.info("环境初始化完成")
        return True
    except Exception as e:
        logging.error(f"环境初始化失败: {e}")
        return False

if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # 初始化环境
    if init_environment():
        print("环境初始化成功")
    else:
        print("环境初始化失败，请查看日志")
        sys.exit(1)
