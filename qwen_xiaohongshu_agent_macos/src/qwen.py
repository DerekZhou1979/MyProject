#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Qwen-Max内容获取模块
负责与通义千问Qwen-Max API交互，获取生成的内容
"""

import os
import json
import time
import logging
import requests
from datetime import datetime

class QwenClient:
    """Qwen-Max API客户端"""
    
    def __init__(self, config):
        """初始化Qwen-Max客户端
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.api_key = config.get("qwen", "api_key")
        self.model = config.get("qwen", "model")
        self.temperature = config.get("qwen", "temperature")
        self.max_tokens = config.get("qwen", "max_tokens")
        self.prompt_template = config.get("qwen", "prompt_template")
        self.max_retries = config.get("runtime", "max_retries")
        self.retry_delay = config.get("runtime", "retry_delay")
        
        # 验证API密钥是否已设置
        if not self.api_key:
            logging.error("Qwen-Max API密钥未设置，请在配置文件中设置api_key")
            raise ValueError("Qwen-Max API密钥未设置")
    
    def generate_content(self, topic=None):
        """生成内容
        
        Args:
            topic: 内容主题，如果为None则从配置中获取
            
        Returns:
            生成的内容字典，包含标题、正文和标签
        """
        # 如果未指定主题，则从配置中获取
        if topic is None:
            topics = self.config.get("content", "topics")
            current_index = self.config.get("content", "current_topic_index")
            
            if not topics:
                logging.error("未配置内容主题")
                raise ValueError("未配置内容主题")
                
            topic = topics[current_index % len(topics)]
            
            # 如果启用了主题轮换，更新下一个主题索引
            if self.config.get("content", "rotate_topics"):
                next_index = (current_index + 1) % len(topics)
                self.config.set("content", "current_topic_index", next_index)
                self.config.save()
        
        # 构建提示词
        prompt = self.prompt_template.format(topic=topic)
        
        # 调用API生成内容
        for attempt in range(self.max_retries):
            try:
                logging.info(f"正在生成主题为 '{topic}' 的内容 (尝试 {attempt+1}/{self.max_retries})")
                response = self._call_qwen_api(prompt)
                
                # 解析生成的内容
                content = self._parse_generated_content(response, topic)
                
                # 保存内容到文件（如果配置了保存）
                if self.config.get("runtime", "save_content"):
                    self._save_content(content)
                
                return content
                
            except Exception as e:
                logging.error(f"生成内容失败: {e}")
                if attempt < self.max_retries - 1:
                    logging.info(f"将在 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logging.error("已达到最大重试次数，放弃生成内容")
                    raise
    
    def _call_qwen_api(self, prompt):
        """调用通义千问Qwen-Max API
        
        Args:
            prompt: 提示词
            
        Returns:
            API响应文本
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 正确的通义千问API请求格式
        data = {
            "model": self.model,
            "input": {
                "messages": [{"role": "user", "content": prompt}]
            },
            "parameters": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
        }
        
        # api_url = "https://dashscope.aliyuncs.com/v1/services/aigc/text-generation/generation"
        # api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        # 添加调试日志
        logging.info(f"API URL: {api_url}")
        logging.info(f"Request Headers: {headers}")
        logging.info(f"Request Data: {data}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            logging.error(f"API调用失败: {response.status_code} {response.text}")
            raise Exception(f"API调用失败: {response.status_code}")
        
        result = response.json()
        # 通义千问的响应格式
        return result["output"]["text"]

    

    def _parse_generated_content(self, text, topic):
        """解析生成的内容，提取标题、正文和标签
        
        Args:
            text: 生成的文本
            topic: 内容主题
            
        Returns:
            解析后的内容字典
        """
        lines = text.strip().split('\n')
        
        # 尝试提取标题（通常是第一行）
        title = lines[0].strip()
        if title.startswith('#'):
            title = title[1:].strip()
        
        # 提取标签（通常在文本末尾，以#开头）
        tags = []
        content_lines = []
        
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('#') and not line.startswith('##'):
                # 这可能是一个标签
                tags.append(line[1:].strip())
            else:
                content_lines.append(line)
        
        # 如果没有找到标签，尝试从文本中查找
        if not tags:
            content_text = '\n'.join(content_lines)
            # 查找常见的标签格式
            tag_markers = ["标签：", "标签:", "Tags：", "Tags:", "#"]
            for marker in tag_markers:
                if marker in content_text:
                    tag_part = content_text.split(marker)[-1].strip()
                    potential_tags = [t.strip() for t in tag_part.split() if t.strip()]
                    if potential_tags:
                        tags = potential_tags
                        break
        
        # 如果配置了自动添加标签，添加默认标签
        if self.config.get("xiaohongshu", "auto_add_tags") and not tags:
            tags = self.config.get("xiaohongshu", "default_tags")
        
        # 如果配置了添加免责声明，添加到正文末尾
        content = '\n'.join(content_lines)
        if self.config.get("content", "add_disclaimer"):
            disclaimer = self.config.get("content", "disclaimer_text")
            content = f"{content}\n\n{disclaimer}"
        
        return {
            "title": title,
            "content": content,
            "tags": tags,
            "topic": topic,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _save_content(self, content):
        """保存内容到文件
        
        Args:
            content: 内容字典
        """
        try:
            content_dir = self.config.ensure_content_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{content['topic'].replace(' ', '_')}.json"
            filepath = os.path.join(content_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=4)
                
            logging.info(f"内容已保存到 {filepath}")
            return filepath
        except Exception as e:
            logging.error(f"保存内容失败: {e}")
            return None
