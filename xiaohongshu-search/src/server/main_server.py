#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import logging
import time
from src.crawler.xiaohongshu_crawler import XiaoHongShuCrawler
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../static')
CORS(app)  # 允许跨域请求

# 配置文件路径
COOKIES_FILE = os.path.join('cache', 'cookies', 'xiaohongshu_cookies.json')

# 全局爬虫实例
crawler = None

def init_crawler():
    """延迟初始化爬虫 - 只在需要时才初始化"""
    global crawler
    if crawler is None:
        try:
            logger.info("正在初始化小红书爬虫...")
            crawler = XiaoHongShuCrawler(use_selenium=True, headless=True, cookies_file=COOKIES_FILE)
            logger.info("小红书爬虫初始化成功")
            return True
        except Exception as e:
            logger.error(f"小红书爬虫初始化失败: {str(e)}")
            logger.error(traceback.format_exc())
            crawler = None
            return False
    return True

@app.route('/')
def index():
    """主页"""
    return send_from_directory('../../static', 'index.html')

@app.route('/login')
def login():
    """登录页面 - 打开浏览器进行手动登录"""
    try:
        # 创建一个新的爬虫实例，专门用于登录（非无头模式）
        login_crawler = XiaoHongShuCrawler(use_selenium=True, headless=False)
        success = login_crawler.login()
        login_crawler.close()  # 关闭登录用的浏览器
        
        if success:
            # 登录成功后，重置主爬虫实例
            global crawler
            crawler = None
            return redirect(url_for('index'))
        else:
            return jsonify({"error": "登录失败，请重试"}), 500
    except Exception as e:
        logger.error(f"登录过程出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"登录过程出错: {str(e)}"}), 500

@app.route('/api/search')
def search():
    """搜索API"""
    # 延迟初始化爬虫
    if not init_crawler():
        return jsonify({"error": "爬虫初始化失败，请检查网络连接和Chrome浏览器"}), 500
        
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({"error": "缺少关键词参数"}), 400
    
    try:
        # 获取参数 - 默认使用配置文件设置
        max_results = int(request.args.get('max_results', 21))  # 改为21篇笔记
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
        # 执行搜索
        search_results = crawler.search(keyword, max_results=max_results, use_cache=use_cache)
        
        # 确保返回的数据格式正确
        # 如果search_results是一个字典并且包含data字段，提取data字段
        if isinstance(search_results, dict) and 'data' in search_results:
            notes = search_results['data']
        else:
            # 否则直接使用搜索结果作为notes
            notes = search_results if isinstance(search_results, list) else []
        
        return jsonify({
            "keyword": keyword,
            "timestamp": int(time.time()),
            "count": len(notes),
            "notes": notes
        })
    except Exception as e:
        logger.error(f"搜索出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "搜索失败", "message": str(e)}), 500

@app.route('/api/note/<note_id>')
def get_note(note_id):
    """获取笔记详情API"""
    # 检查爬虫是否初始化
    if not init_crawler():
        return jsonify({"error": "爬虫初始化失败"}), 500
        
    if not note_id:
        return jsonify({"error": "缺少笔记ID参数"}), 400
    
    try:
        note = crawler.get_note_detail(note_id)
        
        if note:
            return jsonify({"note": note})
        else:
            return jsonify({"error": "未找到该笔记"}), 404
    except Exception as e:
        logger.error(f"获取笔记详情出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "获取笔记详情失败", "message": str(e)}), 500

@app.route('/api/hot-keywords')
def hot_keywords():
    """获取热门关键词API"""
    # 检查爬虫是否初始化
    if not init_crawler():
        return jsonify({"error": "爬虫初始化失败"}), 500
        
    try:
        keywords = crawler.get_hot_keywords()
        return jsonify({"keywords": keywords})
    except Exception as e:
        logger.error(f"获取热门关键词出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "获取热门关键词失败", "message": str(e)}), 500

@app.route('/css/<path:path>')
def serve_css(path):
    """提供CSS文件服务"""
    return send_from_directory('../../static/css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    """提供JavaScript文件服务"""
    return send_from_directory('../../static/js', path)

@app.route('/img/<path:path>')
def serve_img(path):
    """提供图片文件服务"""
    return send_from_directory('../../static/images', path)

@app.errorhandler(404)
def not_found(e):
    """处理404错误"""
    return jsonify({"error": "资源不存在"}), 404

@app.errorhandler(500)
def server_error(e):
    """处理500错误"""
    return jsonify({"error": "服务器内部错误"}), 500

def cleanup():
    """清理资源"""
    global crawler
    if crawler:
        crawler.close()
        crawler = None

# 应用终止时清理资源
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        # 创建必要的目录
        os.makedirs('cache/cookies', exist_ok=True)
        os.makedirs('cache/temp', exist_ok=True)
        os.makedirs('cache/logs', exist_ok=True)
        os.makedirs('static/images', exist_ok=True)
        
        logger.info("小红书搜索服务启动中...")
        logger.info("访问地址: http://localhost:8080")
        logger.info("如需登录，请访问: http://localhost:8080/login")
        
        # 启动服务（不预初始化爬虫）
        app.run(debug=False, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        logger.info("服务已停止")
        cleanup()
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        logger.error(traceback.format_exc())
        cleanup() 