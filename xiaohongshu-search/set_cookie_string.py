#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
小红书cookie字符串设置工具
使用此脚本可以直接粘贴从浏览器复制的cookie字符串
"""

import os
import json
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_cookie_string(cookie_str):
    """解析cookie字符串，转换为列表格式"""
    cookies = []
    
    # 分割cookie字符串
    items = cookie_str.split(';')
    for item in items:
        item = item.strip()
        if not item or '=' not in item:
            continue
        
        name, value = item.split('=', 1)
        cookie = {
            'name': name.strip(),
            'value': value.strip(),
            'domain': '.xiaohongshu.com',
            'path': '/'
        }
        cookies.append(cookie)
    
    return cookies

def main():
    # 确保cache目录存在
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # 默认cookie文件路径
    cookies_file = os.path.join(cache_dir, 'xiaohongshu_cookies.json')
    
    print("=" * 60)
    print("小红书Cookie字符串设置工具")
    print("=" * 60)
    print("此工具可以直接粘贴从浏览器复制的cookie字符串")
    print("方法: 在浏览器中登录小红书，打开开发者工具(F12)，")
    print("选择'应用'或'Application'标签，找到'Cookies'，")
    print("在右侧选择小红书域名，然后复制所有cookie字符串")
    print(f"Cookie文件路径: {cookies_file}")
    print("=" * 60)
    
    # 获取用户输入的cookie字符串
    print("请粘贴完整的cookie字符串:")
    cookie_string = input().strip()
    
    if not cookie_string:
        print("没有输入任何cookie，退出")
        return 1
    
    # 解析cookie字符串
    cookies = parse_cookie_string(cookie_string)
    
    if not cookies:
        print("无法解析cookie字符串，请确保格式正确")
        return 1
    
    # 保存到文件
    try:
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print("=" * 60)
        print(f"成功保存 {len(cookies)} 个cookie到文件: {cookies_file}")
        for cookie in cookies:
            print(f"  - {cookie['name']}")
        print("=" * 60)
    except Exception as e:
        print(f"保存cookie文件失败: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 