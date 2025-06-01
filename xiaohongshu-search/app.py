#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import logging
import os
import time
from crawler import XiaoHongShuCrawler
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)  # 允许跨域请求

# 配置文件路径
COOKIES_FILE = os.path.join('cache', 'xiaohongshu_cookies.json')

# 初始化爬虫
# 只使用Selenium模式
crawler = None  # 暂时设为None，延迟初始化

def init_crawler():
    """延迟初始化爬虫"""
    global crawler
    if crawler is None:
        try:
            logger.info("正在初始化爬虫...")
            crawler = XiaoHongShuCrawler(use_selenium=True, headless=True, cookies_file=COOKIES_FILE)
            logger.info("爬虫初始化成功，使用Selenium模式")
            return True
        except Exception as e:
            logger.error(f"爬虫初始化失败: {str(e)}")
            logger.error(traceback.format_exc())
            crawler = None
            return False
    return True

@app.route('/')
def index():
    """提供静态文件服务"""
    return send_from_directory('.', 'index.html')

@app.route('/login')
def login():
    """登录页面"""
    # 不使用无头模式，打开浏览器进行登录
    try:
        # 创建一个新的爬虫实例，专门用于登录
        login_crawler = XiaoHongShuCrawler(use_selenium=True, headless=False)
        success = login_crawler.login()
        if success:
            # 登录成功后，需要重新初始化主爬虫
            global crawler
            crawler = XiaoHongShuCrawler(use_selenium=True, headless=True, cookies_file=COOKIES_FILE)
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
        # 获取最大结果数量参数，默认为10
        max_results = int(request.args.get('max_results', 10))
        # 是否使用缓存，默认为True
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
        # 使用爬虫搜索
        notes = crawler.search(keyword, max_results=max_results, use_cache=use_cache)
        
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
    # 检查爬虫是否初始化成功
    if not crawler:
        return jsonify({"error": "爬虫未初始化，请先登录"}), 500
        
    if not note_id:
        return jsonify({"error": "缺少笔记ID参数"}), 400
    
    try:
        # 使用爬虫获取笔记详情
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
    # 检查爬虫是否初始化成功
    if not crawler:
        return jsonify({"error": "爬虫未初始化，请先登录"}), 500
        
    try:
        # 使用爬虫获取热门关键词
        keywords = crawler.get_hot_keywords()
        return jsonify({"keywords": keywords})
    except Exception as e:
        logger.error(f"获取热门关键词出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "获取热门关键词失败", "message": str(e)}), 500

@app.route('/css/<path:path>')
def serve_css(path):
    """提供CSS文件服务"""
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    """提供JavaScript文件服务"""
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def serve_img(path):
    """提供图片文件服务"""
    return send_from_directory('img', path)

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
    if crawler:
        crawler.close()

# 应用终止时清理资源
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        # 创建必要的目录
        os.makedirs('cache', exist_ok=True)
        os.makedirs('img', exist_ok=True)
        
        # 检查爬虫是否初始化成功
        if not crawler:
            logger.warning("爬虫未初始化，某些功能可能不可用")
            logger.warning("请先运行登录流程: http://localhost:8080/login")
        
        # 启动服务
        app.run(debug=False, host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        logger.info("服务已停止")
        cleanup()
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        logger.error(traceback.format_exc())
        cleanup() 