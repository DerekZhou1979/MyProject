#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件模块
用于存储和管理脚本运行所需的各项配置
"""

import os
import json
import logging
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    # Qwen-Max API配置
    "qwen": {
        "api_key": "",
        "model": "qwen-max",
        "temperature": 0.7,
        "max_tokens": 2000,
        "prompt_template": "请生成一篇适合小红书平台的内容，主题是：{topic}。内容应该包括标题、正文和5个合适的标签。"
    },
    
    # 小红书配置
    "xiaohongshu": {
        "cookie": "",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "auto_add_tags": True,
        "default_tags": ["AI创作", "每日分享", "生活记录"]
    },
    
    # 内容配置
    "content": {
        "topics": ["生活小窍门", "美食推荐", "旅行攻略", "读书笔记", "职场技巧"],
        "current_topic_index": 0,
        "rotate_topics": True,
        "add_disclaimer": True,
        "disclaimer_text": "本内容由AI辅助创作，仅供参考。"
    },
    
    # 运行配置
    "runtime": {
        "log_level": "INFO",
        "save_content": True,
        "content_dir": "contents",
        "max_retries": 2,
        "retry_delay": 2
    }
}

class Config:
    """配置管理类"""
    
    def __init__(self, config_path=None):
        """初始化配置
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        self.config_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        self.config_path = config_path or self.config_dir / "config.json"
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logging.info(f"配置已从 {self.config_path} 加载")
                    return config
            except Exception as e:
                logging.error(f"加载配置文件失败: {e}")
                logging.info("将使用默认配置")
                return DEFAULT_CONFIG
        else:
            logging.info(f"配置文件不存在，创建默认配置: {self.config_path}")
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    
    def _save_config(self, config):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            logging.info(f"配置已保存到 {self.config_path}")
        except Exception as e:
            logging.error(f"保存配置文件失败: {e}")
    
    def save(self):
        """保存当前配置"""
        self._save_config(self.config)
    
    def get(self, section, key=None):
        """获取配置项
        
        Args:
            section: 配置区块名
            key: 配置项名，如果为None则返回整个区块
            
        Returns:
            配置值或配置区块
        """
        if section not in self.config:
            return None
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key)
    
    def set(self, section, key, value):
        """设置配置项
        
        Args:
            section: 配置区块名
            key: 配置项名
            value: 配置值
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        
    def update(self, section, data):
        """更新配置区块
        
        Args:
            section: 配置区块名
            data: 要更新的配置字典
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section].update(data)
    
    def ensure_content_dir(self):
        """确保内容保存目录存在"""
        content_dir = self.config_dir / self.get("runtime", "content_dir")
        os.makedirs(content_dir, exist_ok=True)
        return content_dir
