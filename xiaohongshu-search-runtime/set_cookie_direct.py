#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书cookie直接设置工具
使用此脚本可以直接粘贴完整的cookie JSON数据
"""

import os
import json
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 确保cache目录存在
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # 默认cookie文件路径
    cookies_file = os.path.join(cache_dir, 'xiaohongshu_cookies.json')
    
    print("=" * 60)
    print("小红书Cookie直接设置工具")
    print("=" * 60)
    print("此工具可以直接设置完整的cookie JSON数据")
    print(f"Cookie文件路径: {cookies_file}")
    print("=" * 60)
    print("请粘贴完整的cookie JSON数据，格式示例:")
    print('[{"name":"cookie1","value":"value1","domain":".xiaohongshu.com","path":"/"},')
    print(' {"name":"cookie2","value":"value2","domain":".xiaohongshu.com","path":"/"}]')
    print("=" * 60)
    print("粘贴完成后按Ctrl+D (Unix/Mac) 或 Ctrl+Z (Windows) 结束输入:")
    
    # 读取用户输入的完整JSON
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    if not lines:
        print("没有输入任何数据，退出")
        return 1
    
    cookie_json = '\n'.join(lines)
    
    # 解析JSON数据
    try:
        cookies = json.loads(cookie_json)
        
        # 检查结构是否正确
        if not isinstance(cookies, list):
            print("错误: 输入的JSON数据必须是一个数组")
            return 1
        
        # 保存到文件
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        
        print("=" * 60)
        print(f"成功保存 {len(cookies)} 个cookie到文件: {cookies_file}")
        print("=" * 60)
        
        return 0
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {str(e)}")
        return 1
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 