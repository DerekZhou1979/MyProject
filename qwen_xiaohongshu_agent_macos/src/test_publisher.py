#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from xiaohongshu_publisher import XiaohongshuPublisher

def test_publish():
    # 获取测试图片路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(os.path.dirname(current_dir), 'test_data')
    
    # 确保测试数据目录存在
    os.makedirs(test_data_dir, exist_ok=True)
    
    # 测试数据
    test_image_path = os.path.join(test_data_dir, 'test_image.jpg')
    
    # 如果测试图片不存在，创建一个简单的测试图片
    if not os.path.exists(test_image_path):
        try:
            from PIL import Image
            # 创建一个100x100的红色测试图片
            img = Image.new('RGB', (100, 100), color='red')
            img.save(test_image_path)
            print(f"创建测试图片: {test_image_path}")
        except ImportError:
            print("请安装 Pillow 库来创建测试图片: pip install Pillow")
            return
    
    # 初始化发布器
    publisher = XiaohongshuPublisher()
    
    # 测试数据
    test_data = {
        "title": "测试笔记 - Python自动发布",
        "content": "这是一个自动发布测试笔记，使用Python和Playwright实现。\n\n"
                  "测试时间：2024年测试\n"
                  "#Python #自动化 #测试",
        "images": [test_image_path],
        "topics": ["Python", "自动化", "测试"]
    }
    
    # 执行发布测试
    print("开始测试发布笔记...")
    result = publisher.publish_note(**test_data)
    
    if result:
        print("测试成功：笔记发布成功！")
    else:
        print("测试失败：笔记发布失败，请检查日志获取详细信息。")

if __name__ == "__main__":
    test_publish() 