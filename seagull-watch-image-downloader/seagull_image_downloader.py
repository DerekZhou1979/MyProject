#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海鸥表官网图片下载器
自动从 https://www.seagullwatch.com/ 下载图片并保存到指定目录
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Gemini Vision API 相关导入
try:
    import google.generativeai as genai
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini Vision API 不可用，将使用基础匹配模式")

class SeagullImageDownloader:
    def __init__(self, config_file='image_download_config.json'):
        """初始化下载器"""
        self.config_file = config_file
        self.base_url = 'https://www.seagullwatch.com/'
        self.images_dir = Path('./images')
        self.session = requests.Session()
        
        # 模式控制标志
        self.force_matching_mode = False
        self.force_download_all = False
        self.use_gemini_vision = False
        
        # 设置请求头，模拟浏览器访问
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 创建images目录
        self.images_dir.mkdir(exist_ok=True)
        
        # 初始化 Gemini API
        self.init_gemini_api()
        
        self.load_config()
    
    def init_gemini_api(self):
        """初始化 Gemini API"""
        if not GEMINI_AVAILABLE:
            self.gemini_model = None
            return
        
        # 获取当前location信息
        print("🌍 检测当前地理位置和网络环境...")
        self._detect_location()
        
        # 只从环境变量获取 API 密钥
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ 未找到 GEMINI_API_KEY 环境变量")
            print("\n💡 解决方案:")
            print("   请在运行前设置环境变量:")
            print("   export GEMINI_API_KEY='your_api_key_here'")
            print("   ")
            print("   获取API密钥: https://makersuite.google.com/app/apikey")
            print("   详细配置请查看: GEMINI_SETUP.md")
            print(f"\n🛑 程序将退出，请设置API密钥后重新运行")
            sys.exit(1)

        try:
            print("🔐 配置Gemini API密钥...")
            genai.configure(api_key=api_key)
            # 使用最新的 Gemini 2.5 Flash Preview 模型
            self.gemini_model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
            
            # 测试API连接
            print("🧪 测试Gemini API连接...")
            test_response = self.gemini_model.generate_content("Hello")
            if test_response.text:
                self.use_gemini_vision = True
                print("✅ Gemini Vision API 已配置成功并通过连接测试")
            else:
                raise Exception("API测试无响应")
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Gemini API 配置失败: {error_msg}")
            
            # 分析具体错误类型并提供解决方案
            if "User location is not supported" in error_msg:
                print("\n🚫 地理位置限制错误详情:")
                print("   - 错误类型: Gemini API 地理位置不支持")
                print("   - 可能原因: 当前地区不在 Google Gemini API 支持范围内")
                print("\n💡 解决方案:")
                print("   1. 使用VPN连接到支持的地区 (如美国、英国等)")
                print("   2. 确保VPN全局代理模式，而非分流模式")
                print("   3. 检查IP地址是否为支持地区的IP")
                print("   4. 或者使用 --rename 模式进行基础智能重命名")
                
            elif "invalid" in error_msg.lower() or "key" in error_msg.lower():
                print("\n🔑 API密钥错误详情:")
                print("   - 错误类型: API密钥无效或已过期")
                print("\n💡 解决方案:")
                print("   1. 检查GEMINI_API_KEY是否正确")
                print("   2. 前往 https://makersuite.google.com/app/apikey 生成新密钥")
                print("   3. 确保API密钥具有Gemini Vision权限")
                
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                print("\n📊 配额限制错误详情:")
                print("   - 错误类型: API配额不足或请求频率过高")
                print("\n💡 解决方案:")
                print("   1. 等待配额重置 (通常为每日重置)")
                print("   2. 升级API计划获得更高配额")
                print("   3. 降低请求频率")
                
            else:
                print(f"\n🔧 网络连接错误详情:")
                print(f"   - 错误类型: {error_msg}")
                print("\n💡 解决方案:")
                print("   1. 检查网络连接")
                print("   2. 确认防火墙设置")
                print("   3. 尝试使用VPN")
            
            print(f"\n🛑 由于Gemini API不可用，程序将退出")
            print(f"💡 建议: 使用 './start_download.sh rename' 进行基础智能重命名")
            
            # 直接退出程序
            sys.exit(1)
    
    def _detect_location(self):
        """检测当前地理位置，使用多个备用API服务"""
        location_apis = [
            {
                'name': 'IPApi.co',
                'url': 'https://ipapi.co/json/',
                'timeout': 8
            },
            {
                'name': 'IP-API.com', 
                'url': 'http://ip-api.com/json/',
                'timeout': 6
            },
            {
                'name': 'IPInfo.io',
                'url': 'https://ipinfo.io/json',
                'timeout': 8
            },
            {
                'name': 'HTTPBin.org',
                'url': 'https://httpbin.org/ip',
                'timeout': 5
            }
        ]
        
        for api in location_apis:
            try:
                import requests
                print(f"🔍 尝试通过 {api['name']} 获取地理位置...")
                
                response = requests.get(api['url'], timeout=api['timeout'])
                if response.status_code == 200:
                    location_data = response.json()
                    
                    if api['name'] == 'IPApi.co':
                        print(f"📍 当前公网IP: {location_data.get('ip', '未知')}")
                        print(f"🗺️  地理位置: {location_data.get('country_name', '未知')} - {location_data.get('city', '未知')}")
                        print(f"🏢 ISP: {location_data.get('org', '未知')}")
                        return
                    elif api['name'] == 'IP-API.com':
                        print(f"📍 当前公网IP: {location_data.get('query', '未知')}")
                        print(f"🗺️  地理位置: {location_data.get('country', '未知')} - {location_data.get('city', '未知')}")
                        print(f"🏢 ISP: {location_data.get('isp', '未知')}")
                        return
                    elif api['name'] == 'IPInfo.io':
                        print(f"📍 当前公网IP: {location_data.get('ip', '未知')}")
                        print(f"🗺️  地理位置: {location_data.get('country', '未知')} - {location_data.get('city', '未知')}")
                        print(f"🏢 ISP: {location_data.get('org', '未知')}")
                        return
                    elif api['name'] == 'HTTPBin.org':
                        print(f"📍 当前公网IP: {location_data.get('origin', '未知')}")
                        print(f"🗺️  地理位置: 正在解析...")
                        return
                        
            except requests.exceptions.Timeout:
                print(f"⏰ {api['name']} 响应超时，尝试下一个服务...")
                continue
            except requests.exceptions.ConnectionError:
                print(f"🔌 {api['name']} 连接失败，尝试下一个服务...")
                continue
            except Exception as e:
                print(f"⚠️  {api['name']} 获取失败: {e}")
                continue
        
        # 所有API都失败的情况
        print("⚠️  所有地理位置服务都无法访问")
        print("💡 这可能不会影响Gemini API的正常使用")
        print("🌐 如果Gemini API报错地理位置限制，请考虑使用VPN")
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ 已加载配置文件: {self.config_file}")
        except FileNotFoundError:
            print(f"❌ 配置文件 {self.config_file} 不存在，请先创建配置文件")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ 配置文件 {self.config_file} 格式错误")
            sys.exit(1)
    
    def get_page_content(self, url):
        """获取网页内容，带重试机制"""
        max_retries = 3
        timeout_values = [45, 60, 90]  # 递增的超时时间
        
        for attempt in range(max_retries):
            try:
                timeout = timeout_values[attempt]
                print(f"🌐 正在访问: {url} (尝试 {attempt + 1}/{max_retries}, 超时设置: {timeout}秒)")
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                print(f"✅ 网页访问成功")
                return response.text
            except requests.RequestException as e:
                print(f"⚠️  第 {attempt + 1} 次尝试失败: {e}")
                if attempt < max_retries - 1:
                    wait_time = 3 * (attempt + 1)  # 递增等待时间
                    print(f"⏱️  等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 访问网页失败，已尝试 {max_retries} 次")
                    return None
    
    def find_images_on_page(self, html_content, base_url):
        """在网页中查找图片URL"""
        soup = BeautifulSoup(html_content, 'html.parser')
        image_urls = []
        
        # 查找所有img标签
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                # 转换为绝对URL
                full_url = urljoin(base_url, src)
                if self.is_valid_image_url(full_url):
                    image_urls.append(full_url)
        
        # 查找背景图片
        for element in soup.find_all(attrs={'style': re.compile(r'background.*?url')}):
            style = element.get('style', '')
            urls = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
            for url in urls:
                full_url = urljoin(base_url, url)
                if self.is_valid_image_url(full_url):
                    image_urls.append(full_url)
        
        return list(set(image_urls))  # 去重
    
    def is_valid_image_url(self, url):
        """检查是否为有效的图片URL"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # 检查文件扩展名
        for ext in image_extensions:
            if path.endswith(ext):
                return True
        
        # 检查是否包含常见的图片关键词
        image_keywords = ['img', 'image', 'photo', 'pic', 'thumb', 'banner']
        for keyword in image_keywords:
            if keyword in path:
                return True
        
        return False
    
    def download_image(self, url, filename):
        """下载单张图片"""
        try:
            print(f"📥 正在下载: {filename}")
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            file_path = self.images_dir / filename
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            file_size = file_path.stat().st_size
            print(f"✅ 下载完成: {filename} ({self.format_file_size(file_size)})")
            return True
            
        except Exception as e:
            print(f"❌ 下载失败: {filename} - {e}")
            return False
    
    def format_file_size(self, size_bytes):
        """格式化文件大小显示"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 1)
        return f"{s} {size_names[i]}"
    
    def search_and_download_images(self):
        """搜索并下载配置文件中指定的图片"""
        print("🚀 开始下载海鸥表官网图片...")
        print("=" * 60)
        
        total_downloaded = 0
        total_failed = 0
        
        # 获取所有图片URL
        all_image_urls = self.get_all_image_urls()
        
        if not all_image_urls:
            print("❌ 未找到任何图片")
            return
        
        print(f"🔍 总共找到 {len(all_image_urls)} 张不重复的图片")
        print("=" * 60)
        
        # 根据设置的模式标志选择下载方式
        if self.force_matching_mode:
            print("\n🎯 使用智能匹配模式")
            total_downloaded, total_failed = self.download_with_matching()
        elif self.force_download_all:
            print("\n📥 使用全量下载模式")
            total_downloaded, total_failed = self.download_all_images(all_image_urls)
        else:
            # 交互模式（保留原有逻辑作为备用）
            print("\n🤖 请选择下载模式:")
            print("1. 智能匹配模式 (根据配置文件匹配特定图片)")
            print("2. 全量下载模式 (下载所有找到的图片)")
            
            try:
                choice = input("请输入选择 (1 或 2，默认为 2): ").strip()
                if not choice:
                    choice = "2"
            except:
                choice = "2"
            
            if choice == "1":
                total_downloaded, total_failed = self.download_with_matching()
            else:
                total_downloaded, total_failed = self.download_all_images(all_image_urls)
        
        print("\n" + "=" * 60)
        print(f"📊 下载统计:")
        print(f"✅ 成功下载: {total_downloaded} 张")
        print(f"❌ 下载失败: {total_failed} 张")
        print("🎉 下载任务完成!")
        
        # 如果有成功下载的图片，执行智能重命名
        if total_downloaded > 0:
            self.smart_rename_images()
    
    def get_all_image_urls(self):
        """获取所有图片URL"""
        # 首先访问主页，获取所有可能的图片URL
        main_page_content = self.get_page_content(self.base_url)
        if not main_page_content:
            print("❌ 无法访问主页，退出程序")
            return []
        
        # 获取主页所有图片URL
        all_image_urls = self.find_images_on_page(main_page_content, self.base_url)
        print(f"🔍 在主页找到 {len(all_image_urls)} 张图片")
        
        # 已知有效的页面列表（已验证可访问）
        working_pages = [
            'news/', 'master/'
        ]
        
        # 访问已知有效的页面
        for page in working_pages:
            page_url = urljoin(self.base_url, page)
            page_content = self.get_page_content(page_url)
            if page_content:
                page_images = self.find_images_on_page(page_content, page_url)
                all_image_urls.extend(page_images)
                print(f"🔍 在 {page} 找到 {len(page_images)} 张图片")
            time.sleep(0.5)  # 减少等待时间，提高效率
        
        # 去重所有图片URL
        return list(set(all_image_urls))
    
    def download_with_matching(self):
        """使用配置文件匹配下载"""
        all_image_urls = self.get_all_image_urls()
        total_downloaded = 0
        total_failed = 0
        
        # 根据配置文件下载指定图片
        for category, images in self.config['image_categories'].items():
            print(f"\n📁 正在处理分类: {category}")
            print("-" * 40)
            
            for image_info in images:
                filename = image_info['filename']
                keywords = image_info['keywords']
                description = image_info['description']
                
                print(f"🎯 寻找匹配图片: {description}")
                
                # 根据关键词匹配最合适的图片
                best_match = self.find_best_matching_image(all_image_urls, keywords)
                
                if best_match:
                    if self.download_image(best_match, filename):
                        total_downloaded += 1
                    else:
                        total_failed += 1
                else:
                    print(f"⚠️  未找到匹配的图片: {filename}")
                    total_failed += 1
                
                time.sleep(0.5)  # 避免下载过快
        
        return total_downloaded, total_failed
    
    def download_all_images(self, image_urls):
        """下载所有找到的图片"""
        total_downloaded = 0
        total_failed = 0
        
        print(f"\n📥 开始下载所有图片 (共 {len(image_urls)} 张)")
        print("-" * 60)
        
        for i, url in enumerate(image_urls, 1):
            # 生成文件名
            filename = self.generate_filename(url, i)
            
            print(f"📥 [{i}/{len(image_urls)}] 正在下载: {filename}")
            
            if self.download_image(url, filename):
                total_downloaded += 1
            else:
                total_failed += 1
            
            time.sleep(0.3)  # 避免下载过快
        
        return total_downloaded, total_failed
    
    def generate_filename(self, url, index):
        """根据URL生成合适的文件名"""
        parsed_url = urlparse(url)
        original_filename = os.path.basename(parsed_url.path)
        
        if original_filename and '.' in original_filename:
            # 有原始文件名
            name, ext = os.path.splitext(original_filename)
            return f"seagull_{index:03d}_{name}{ext}"
        else:
            # 没有原始文件名，根据URL特征生成
            url_parts = [part for part in parsed_url.path.split('/') if part]
            if url_parts:
                name_part = '_'.join(url_parts[-2:])  # 取最后两个路径部分
                return f"seagull_{index:03d}_{name_part}.jpg"
            else:
                return f"seagull_{index:03d}.jpg"
    
    def find_best_matching_image(self, image_urls, keywords):
        """根据关键词找到最匹配的图片URL - 优化版本"""
        scored_images = []
        
        for url in image_urls:
            score = 0
            url_lower = url.lower()
            
            # 计算匹配分数 - 更宽松的匹配策略
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # URL中包含关键词
                if keyword_lower in url_lower:
                    score += 5
                    
                # 文件名匹配权重更高
                filename = os.path.basename(urlparse(url).path).lower()
                if keyword_lower in filename:
                    score += 15
                
                # 路径匹配
                path = urlparse(url).path.lower()
                if keyword_lower in path:
                    score += 8
            
            # 即使没有关键词匹配，也给一个基础分数，确保有图片被下载
            if score == 0:
                # 检查是否是高质量图片（大尺寸、高清等）
                if any(qual in url_lower for qual in ['large', 'big', 'high', 'hd', '1200', '1920', '800']):
                    score = 1
                elif any(size in url_lower for size in ['thumb', 'small', 'mini', '150', '200']):
                    score = 0.5
                else:
                    score = 1  # 给所有图片一个基础分数
            
            scored_images.append((url, score))
        
        # 按分数排序，返回最高分的URL
        if scored_images:
            scored_images.sort(key=lambda x: x[1], reverse=True)
            return scored_images[0][0]
        
        return None
    
    def manual_download_mode(self):
        """手动下载模式 - 显示所有找到的图片供用户选择"""
        print("🔍 手动下载模式 - 正在扫描网站...")
        
        # 获取所有图片URL
        main_page_content = self.get_page_content(self.base_url)
        if not main_page_content:
            return
        
        all_image_urls = self.find_images_on_page(main_page_content, self.base_url)
        
        print(f"\n🖼️  找到以下图片 (共 {len(all_image_urls)} 张):")
        print("=" * 80)
        
        for i, url in enumerate(all_image_urls[:50], 1):  # 只显示前50张
            filename = os.path.basename(urlparse(url).path)
            print(f"{i:2d}. {filename}")
            print(f"    URL: {url}")
            print()
        
        if len(all_image_urls) > 50:
            print(f"... 还有 {len(all_image_urls) - 50} 张图片未显示")
    
    def smart_rename_images(self):
        """智能重命名images目录下的图片文件"""
        print("\n" + "=" * 60)
        print("🤖 开始智能重命名图片文件...")
        print("=" * 60)
        
        if not self.images_dir.exists():
            print("❌ images目录不存在")
            return
        
        # 获取所有图片文件
        image_files = list(self.images_dir.glob("seagull_*"))
        if not image_files:
            print("📂 未找到需要重命名的图片文件")
            return
        
        print(f"📁 发现 {len(image_files)} 个图片文件需要处理")
        
        # 存储重命名映射
        rename_mapping = {}
        used_names = set()
        
        # 为每个分类创建匹配计数器
        category_counters = {}
        for category in self.config['image_categories'].keys():
            category_counters[category] = 1
        
        # 遍历所有图片文件进行智能匹配
        for image_file in image_files:
            original_name = image_file.name
            file_size = image_file.stat().st_size
            
            print(f"\n🔍 分析文件: {original_name}")
            print(f"   文件大小: {self.format_file_size(file_size)}")
            
            # 找到最佳匹配的配置项
            best_match = self.find_best_config_match(original_name, file_size)
            
            if best_match:
                category, config_item, score = best_match
                
                # 生成新的文件名
                new_name = self.generate_smart_filename(
                    config_item, category, category_counters, used_names, original_name
                )
                
                if new_name != original_name:
                    rename_mapping[original_name] = new_name
                    used_names.add(new_name)
                    category_counters[category] += 1
                    
                    print(f"   ✅ 匹配成功: {config_item['description']}")
                    print(f"   📝 新文件名: {new_name}")
                    print(f"   🎯 匹配分数: {score}")
                else:
                    print(f"   ✅ 文件名已是最佳匹配")
            else:
                print(f"   ⚠️  未找到合适的匹配，保持原文件名")
        
        # 执行重命名
        if rename_mapping:
            print(f"\n📝 准备重命名 {len(rename_mapping)} 个文件...")
            
            for old_name, new_name in rename_mapping.items():
                old_path = self.images_dir / old_name
                new_path = self.images_dir / new_name
                
                try:
                    old_path.rename(new_path)
                    print(f"   ✅ {old_name} → {new_name}")
                except Exception as e:
                    print(f"   ❌ 重命名失败 {old_name}: {e}")
            
            print(f"\n🎉 智能重命名完成! 成功重命名 {len(rename_mapping)} 个文件")
        else:
            print("\n📂 所有文件名都已是最佳匹配，无需重命名")
    
    def find_best_config_match(self, filename, file_size):
        """为图片文件找到最佳的配置匹配项"""
        best_score = 0
        best_match = None
        filename_lower = filename.lower()
        
        for category, config_items in self.config['image_categories'].items():
            for config_item in config_items:
                score = 0
                
                # 基于关键词匹配
                for keyword in config_item['keywords']:
                    keyword_lower = keyword.lower()
                    if keyword_lower in filename_lower:
                        # 关键词匹配给分
                        if len(keyword_lower) > 3:  # 长关键词权重更高
                            score += 15
                        else:
                            score += 8
                
                # 基于文件大小特征匹配
                if file_size > 5 * 1024 * 1024:  # 大于5MB，可能是高质量产品图
                    if any(kw in config_item['keywords'] for kw in ['hero', 'main', 'master', 'large']):
                        score += 10
                elif file_size < 50 * 1024:  # 小于50KB，可能是图标
                    if any(kw in config_item['keywords'] for kw in ['icon', 'thumb', 'small']):
                        score += 10
                
                # 基于文件名模式匹配
                if 'team' in filename_lower and 'team' in ' '.join(config_item['keywords']).lower():
                    score += 20
                if 'footer' in filename_lower and any('icon' in kw for kw in config_item['keywords']):
                    score += 20
                if any(year in filename_lower for year in ['1963']) and '1963' in ' '.join(config_item['keywords']):
                    score += 25
                
                # 基于数字ID模式判断（长数字ID通常是产品图）
                long_numbers = re.findall(r'\d{10,}', filename)
                if long_numbers and any(kw in config_item['keywords'] for kw in ['product', 'main', 'detail']):
                    score += 8
                
                if score > best_score:
                    best_score = score
                    best_match = (category, config_item, score)
        
        return best_match if best_score > 5 else None  # 最低分数阈值
    
    def generate_smart_filename(self, config_item, category, counters, used_names, original_name):
        """生成智能的新文件名"""
        # 获取原文件扩展名
        _, ext = os.path.splitext(original_name)
        
        # 使用配置文件中的文件名作为基础
        base_name = config_item['filename']
        name_without_ext, _ = os.path.splitext(base_name)
        
        # 如果配置的文件名已经被使用，添加序号
        new_name = base_name
        counter = 1
        
        while new_name in used_names:
            name_parts = name_without_ext.split('_')
            if len(name_parts) > 2:
                # 在最后一个部分前插入序号
                name_parts.insert(-1, f"{counter:02d}")
            else:
                name_parts.append(f"{counter:02d}")
            
            new_name = '_'.join(name_parts) + ext
            counter += 1
        
        return new_name
    
    def analyze_image_features(self, image_path):
        """分析图片特征（文件大小、可能的内容类型等）"""
        try:
            file_size = image_path.stat().st_size
            filename = image_path.name.lower()
            
            features = {
                'size': file_size,
                'is_large': file_size > 2 * 1024 * 1024,  # 大于2MB
                'is_small': file_size < 100 * 1024,       # 小于100KB
                'is_icon': 'icon' in filename or file_size < 10 * 1024,
                'is_banner': 'banner' in filename or file_size > 1024 * 1024,
                'has_numbers': bool(re.search(r'\d{10,}', filename)),
                'has_team': 'team' in filename,
                'has_footer': 'footer' in filename,
            }
            
            return features
        except Exception as e:
            print(f"   ⚠️  分析图片特征失败: {e}")
            return {'size': 0}
    
    def analyze_image_with_gemini(self, image_path):
        """使用 Gemini Vision API 分析图片内容 - 保持原始分辨率"""
        if not self.use_gemini_vision or not self.gemini_model:
            return None
        
        try:
            # 打开图片但保持原始大小
            image = Image.open(image_path)
            
            print(f"   📐 原始图片尺寸: {image.width}x{image.height}")
            
            # 构建分析提示词
            prompt = """
请分析这张海鸥表相关的图片，并识别以下信息：

1. 图片类型：
   - hero/banner: 大幅宣传图、英雄图
   - product: 产品图、手表正面图
   - detail: 细节图、特写图
   - icon: 小图标、按钮图标
   - news: 新闻图片
   - team: 团队照片
   - background: 背景图

2. 手表系列特征：
   - 1963飞行员表系列: 计时表、飞行员风格
   - 陀飞轮/skeleton: 镂空表盘、可见机芯
   - 潜水表: 旋转表圈、防水设计
   - 女表: 精致小巧、珠宝感
   - 复古电视: 方形表盘、复古风格

3. 图片质量和用途：
   - 主图: 高质量产品主图
   - 缩略图: 小尺寸预览图
   - 背景图: 装饰性背景

请用JSON格式回复：
{
    "type": "图片类型",
    "series": "手表系列",
    "quality": "图片质量",
    "description": "简短描述",
    "confidence": "置信度(1-10)"
}"""
            
            print("   🤖 正在调用 Gemini Vision API 分析图片...")
            
            # 调用 Gemini Vision API - 使用原始图片
            response = self.gemini_model.generate_content([prompt, image])
            
            if response.text:
                print(f"   ✅ AI分析成功")
                print(f"   📝 AI分析结果: {response.text[:100]}...")
                return response.text
            else:
                print("   ❌ AI分析无响应")
                return None
                
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Gemini 分析失败: {error_msg}")
            
            # 检查是否为地理位置限制错误
            if "User location is not supported" in error_msg:
                print("   🚫 检测到地理位置限制错误")
                print("   💡 请使用VPN连接到支持的地区，或使用基础重命名模式")
                # 如果在批量处理中遇到地理位置错误，直接退出
                if hasattr(self, '_in_batch_processing'):
                    print("\n🛑 由于地理位置限制，批量处理将终止")
                    sys.exit(1)
            
            return None
    
    def smart_rename_with_gemini(self):
        """使用 Gemini Vision API 智能重命名图片文件 - 纯AI模式"""
        print("\n" + "=" * 60)
        print("🧠 使用 Gemini Vision AI 智能重命名图片文件...")
        print("=" * 60)
        
        if not self.use_gemini_vision or not self.gemini_model:
            print("❌ Gemini Vision API 未配置或不可用")
            print("💡 建议: 使用 './start_download.sh rename' 进行基础智能重命名")
            return
        
        # 设置批量处理标志
        self._in_batch_processing = True
        
        if not self.images_dir.exists():
            print("❌ images目录不存在")
            return
        
        # 获取所有图片文件
        image_files = []
        for ext in ['jpg', 'jpeg', 'png', 'webp']:
            image_files.extend(self.images_dir.glob(f"*.{ext}"))
            image_files.extend(self.images_dir.glob(f"*.{ext.upper()}"))
        
        if not image_files:
            print("📂 未找到需要重命名的图片文件")
            return
        
        print(f"📁 发现 {len(image_files)} 个图片文件需要AI分析")
        print("⚠️  注意: 只使用Gemini Vision API，不使用降级逻辑")
        
        # 存储成功分析的结果
        successful_analyses = []
        failed_analyses = []
        
        # 逐个分析图片
        for i, image_path in enumerate(image_files, 1):
            print(f"\n🔍 [{i}/{len(image_files)}] 分析: {image_path.name}")
            file_size = image_path.stat().st_size
            print(f"   文件大小: {self.format_file_size(file_size)}")
            
            # 使用 Gemini Vision 分析
            gemini_analysis = self.analyze_image_with_gemini(image_path)
            
            if gemini_analysis:
                try:
                    # 尝试解析JSON响应
                    import json
                    text = gemini_analysis.strip()
                    start = text.find('{')
                    end = text.rfind('}') + 1
                    if start >= 0 and end > start:
                        json_str = text[start:end]
                        analysis_data = json.loads(json_str)
                        
                        print(f"   🎯 AI识别类型: {analysis_data.get('type', '未知')}")
                        print(f"   📋 AI识别系列: {analysis_data.get('series', '未知')}")  
                        print(f"   🏆 置信度: {analysis_data.get('confidence', 0)}/10")
                        
                        # 根据AI分析生成新文件名
                        new_filename = self.generate_ai_filename(image_path, analysis_data)
                        if new_filename and new_filename != image_path.name:
                            successful_analyses.append({
                                'old_path': image_path,
                                'new_filename': new_filename,
                                'analysis': analysis_data
                            })
                            print(f"   ✅ AI推荐文件名: {new_filename}")
                        else:
                            print(f"   ⚠️  AI分析完成但无需重命名")
                            failed_analyses.append(image_path.name)
                    else:
                        print(f"   ❌ AI响应格式错误，无法解析JSON")
                        failed_analyses.append(image_path.name)
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ AI响应JSON解析失败: {e}")
                    failed_analyses.append(image_path.name)
            else:
                print(f"   ❌ Gemini Vision AI分析失败")
                failed_analyses.append(image_path.name)
        
        # 执行重命名操作
        if successful_analyses:
            print(f"\n📝 准备重命名 {len(successful_analyses)} 个AI分析成功的文件...")
            renamed_count = 0
            
            for item in successful_analyses:
                old_path = item['old_path']
                new_filename = item['new_filename']
                new_path = old_path.parent / new_filename
                
                try:
                    # 避免文件名冲突
                    if new_path.exists() and new_path != old_path:
                        base, ext = new_filename.rsplit('.', 1)
                        counter = 1
                        while new_path.exists():
                            new_filename = f"{base}_{counter:02d}.{ext}"
                            new_path = old_path.parent / new_filename
                            counter += 1
                    
                    old_path.rename(new_path)
                    print(f"   ✅ {old_path.name} → {new_filename}")
                    renamed_count += 1
                    
                except Exception as e:
                    print(f"   ❌ 重命名失败 {old_path.name}: {e}")
            
            print(f"\n🎉 Gemini Vision AI 智能重命名完成!")
            print(f"✅ 成功重命名: {renamed_count} 个文件") 
            print(f"❌ 分析失败: {len(failed_analyses)} 个文件")
            
            if failed_analyses:
                print(f"\n⚠️  AI分析失败的文件:")
                for filename in failed_analyses[:10]:  # 只显示前10个
                    print(f"   - {filename}")
                if len(failed_analyses) > 10:
                    print(f"   ... 还有 {len(failed_analyses) - 10} 个文件")
        else:
            print(f"\n❌ 所有文件的AI分析都失败了")
            print(f"💡 建议检查:")
            print(f"   1. Gemini API 密钥是否有效")
            print(f"   2. 网络连接是否正常") 
            print(f"   3. API 配额是否充足")
            print(f"   4. 地区是否支持Gemini API")
    
    def generate_ai_filename(self, image_path, analysis_data):
        """根据AI分析结果生成新文件名 - 格式: seagull_type_series_quality_description"""
        try:
            image_type = analysis_data.get('type', '').lower()
            series = analysis_data.get('series', '').lower()
            quality = analysis_data.get('quality', '').lower()
            description = analysis_data.get('description', '').lower()
            confidence_raw = analysis_data.get('confidence', 0)
            
            # 确保confidence是数字类型
            try:
                confidence = float(confidence_raw) if confidence_raw else 0
            except (ValueError, TypeError):
                # 如果confidence是字符串类型，尝试提取数字
                confidence = 0
                if isinstance(confidence_raw, str):
                    import re
                    match = re.search(r'(\d+)', confidence_raw)
                    if match:
                        confidence = float(match.group(1))
            
            # 只处理高置信度的分析结果
            if confidence < 6:
                print(f"   ⚠️  置信度过低({confidence}/10)，跳过重命名")
                return None
            
            # 获取文件扩展名
            ext = image_path.suffix.lower()
            
            # 清理和标准化各个字段
            type_clean = self._clean_field(image_type)
            series_clean = self._clean_field(series) 
            quality_clean = self._clean_field(quality)
            description_clean = self._extract_description_keyword(description)
            
            # 构建文件名组件
            filename_parts = ['seagull']
            
            # 添加type (必须)
            if type_clean:
                filename_parts.append(type_clean)
            else:
                filename_parts.append('unknown')
            
            # 添加series (如果有意义)
            if series_clean and series_clean not in ['null', 'none', '无', '未知', '无法确定', '其他']:
                filename_parts.append(series_clean)
            
            # 添加quality (如果有意义且简洁)
            if quality_clean and quality_clean in ['thumb', 'detail', 'main', 'hero', 'banner', 'icon']:
                filename_parts.append(quality_clean)
            
            # 添加description关键词 (如果有意义)
            if description_clean and description_clean not in ['unknown', 'general', 'image']:
                filename_parts.append(description_clean)
            
            # 生成最终文件名
            filename = '_'.join(filename_parts) + ext
            
            # 确保文件名不会太长
            if len(filename) > 80:
                # 如果太长，保留前3个部分
                filename = '_'.join(filename_parts[:3]) + ext
            
            return filename
                
        except Exception as e:
            print(f"   ❌ 生成文件名失败: {e}")
            return None
    
    def _clean_field(self, field):
        """清理字段，转换为适合文件名的全英文格式"""
        if not field:
            return ""
        
        # 转小写并移除特殊字符
        clean = str(field).lower().strip()
        
        # 移除常见无用词和特殊字符
        clean = clean.replace('/', '_').replace('-', '_').replace(' ', '_')
        clean = clean.replace('系列', '').replace('series', '')
        
        # 完整的中文到英文翻译映射
        translations = {
            # 产品系列相关
            '飞行员表': 'pilot',
            '飞行': 'flight',
            '陀飞轮': 'tourbillon',
            '潜水表': 'dive',
            '潜水': 'dive', 
            '海洋': 'ocean',
            '复古': 'retro',
            '电视': 'tv',
            '女表': 'women',
            '女士': 'women',
            '男表': 'men',
            '男士': 'men',
            '大师': 'master',
            '工匠': 'craftsman',
            '机械': 'mechanical',
            '自动': 'automatic',
            '石英': 'quartz',
            
            # 图片类型相关
            '团队': 'team',
            '新闻': 'news',
            '背景': 'background',
            '主图': 'main',
            '缩略图': 'thumb',
            '细节': 'detail',
            '产品': 'product',
            '英雄': 'hero',
            '横幅': 'banner',
            '图标': 'icon',
            
            # 质量和描述相关
            '高清': 'hd',
            '精美': 'fine',
            '优质': 'quality',
            '专业': 'professional',
            '商务': 'business',
            '运动': 'sport',
            '休闲': 'casual',
            '正装': 'formal',
            '时尚': 'fashion',
            '经典': 'classic',
            '现代': 'modern',
            '传统': 'traditional',
            
            # 材质相关
            '精钢': 'steel',
            '不锈钢': 'steel',
            '黄金': 'gold',
            '玫瑰金': 'rosegold',
            '白金': 'platinum',
            '钛合金': 'titanium',
            '陶瓷': 'ceramic',
            '皮革': 'leather',
            '橡胶': 'rubber',
            
            # 常见词汇清理
            '手表': 'watch',
            '腕表': 'watch',
            '时计': 'timepiece',
            '表': '',  # 单独的"表"字移除
            '款': '',  # "款"字移除
            '型': '',  # "型"字移除
            '级': '',  # "级"字移除
        }
        
        # 执行翻译
        for chinese, english in translations.items():
            clean = clean.replace(chinese, english)
        
        # 移除多余的下划线和空值
        clean = re.sub(r'_+', '_', clean).strip('_')
        
        # 移除任何剩余的中文字符
        clean = re.sub(r'[\u4e00-\u9fff]+', '', clean)
        
        # 最终清理
        clean = re.sub(r'_+', '_', clean).strip('_')
        
        return clean
    
    def _extract_description_keyword(self, description):
        """从描述中提取一个总结性的英文关键词"""
        if not description:
            return ""
        
        # 中文到英文的翻译映射
        chinese_translations = {
            '手表': 'watch',
            '腕表': 'watch', 
            '时计': 'timepiece',
            '机芯': 'movement',
            '表盘': 'dial',
            '表带': 'strap',
            '表链': 'bracelet',
            '表冠': 'crown',
            '指针': 'hands',
            '刻度': 'marker',
            '夜光': 'luminous',
            '防水': 'waterproof',
            '计时': 'chrono',
            '日历': 'calendar',
            '月相': 'moonphase',
            '动力': 'power',
            '储能': 'reserve',
            '精钢': 'steel',
            '黄金': 'gold',
            '玫瑰金': 'rosegold',
            '钛合金': 'titanium',
            '陶瓷': 'ceramic',
            '蓝宝石': 'sapphire',
            '皮革': 'leather',
            '橡胶': 'rubber',
            '尼龙': 'nylon',
            '男士': 'men',
            '女士': 'women',
            '运动': 'sport',
            '商务': 'business',
            '休闲': 'casual',
            '正装': 'formal',
            '复古': 'vintage',
            '现代': 'modern',
            '经典': 'classic',
            '时尚': 'fashion',
            '优雅': 'elegant',
            '精致': 'refined',
            '豪华': 'luxury',
            '限量': 'limited',
            '特别': 'special',
            '纪念': 'commemorative'
        }
        
        # 优先级关键词映射（按重要性排序）
        priority_keywords = {
            # 高优先级 - 产品特征
            'tourbillon': 'tourbillon',
            'skeleton': 'skeleton', 
            'chronograph': 'chrono',
            'diving': 'dive',
            'pilot': 'pilot',
            'aviation': 'aviation',
            'military': 'military',
            'dress': 'dress',
            'sport': 'sport',
            
            # 中优先级 - 材质和功能
            'gold': 'gold',
            'steel': 'steel',
            'titanium': 'titanium',
            'ceramic': 'ceramic',
            'automatic': 'auto',
            'mechanical': 'mech',
            'quartz': 'quartz',
            'solar': 'solar',
            
            # 低优先级 - 颜色和基本描述
            'black': 'black',
            'white': 'white', 
            'blue': 'blue',
            'brown': 'brown',
            'silver': 'silver',
            'rose': 'rose'
        }
        
        desc_lower = description.lower()
        
        # 首先翻译中文
        for chinese, english in chinese_translations.items():
            if chinese in desc_lower:
                desc_lower = desc_lower.replace(chinese, english)
        
        # 按优先级查找关键词
        for keyword, short in priority_keywords.items():
            if keyword in desc_lower:
                return short
        
        # 如果没找到优先关键词，查找第一个有意义的英文单词
        words = re.findall(r'\b[a-zA-Z]{4,}\b', desc_lower)
        if words:
            # 过滤掉常见无意义词汇
            filtered_words = [w for w in words if w not in [
                'this', 'that', 'with', 'from', 'have', 'been', 'they', 'were',
                'said', 'each', 'which', 'their', 'time', 'will', 'about', 'image',
                'picture', 'photo', 'showing', 'display', 'featuring', 'contains'
            ]]
            if filtered_words:
                return filtered_words[0].lower()
        
        # 最后尝试提取3字母单词
        words_3 = re.findall(r'\b[a-zA-Z]{3}\b', desc_lower)
        useful_3_words = [w for w in words_3 if w not in ['the', 'and', 'for', 'are', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'end', 'few', 'man', 'men', 'put', 'say', 'she', 'too', 'use']]
        if useful_3_words:
            return useful_3_words[0].lower()
        
        return ""
    
    def _clean_series_name(self, series):
        """清理系列名称，生成适合文件名的格式"""
        if not series:
            return ""
        
        # 移除常见的后缀
        clean = series.replace('系列', '').replace('series', '').strip()
        
        # 替换空格和特殊字符
        clean = clean.replace(' ', '_').replace('/', '_').replace('-', '_')
        
        # 移除多余的下划线
        clean = re.sub(r'_+', '_', clean).strip('_')
        
        # 翻译常见的中文系列名
        translations = {
            '飞行': 'flight',
            '陀飞轮': 'tourbillon', 
            '潜水': 'dive',
            '海洋': 'ocean',
            '复古': 'retro',
            '电视': 'tv',
            '女表': 'women',
            '大师': 'master',
            '工匠': 'craftsman'
        }
        
        for chinese, english in translations.items():
            clean = clean.replace(chinese, english)
        
        return clean.lower()


def main():
    """主函数"""
    print("🦅 海鸥表官网图片下载器")
    print("=" * 60)
    
    downloader = SeagullImageDownloader()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--manual':
            downloader.manual_download_mode()
        elif sys.argv[1] == '--match':
            # 强制使用匹配模式
            downloader.force_matching_mode = True
            downloader.search_and_download_images()
        elif sys.argv[1] == '--all':
            # 强制使用全量下载模式
            downloader.force_download_all = True
            downloader.search_and_download_images()
        elif sys.argv[1] == '--rename':
            # 只执行智能重命名
            downloader.smart_rename_images()
        elif sys.argv[1] == '--gemini':
            # 使用 Gemini Vision 智能重命名
            downloader.smart_rename_with_gemini()
        else:
            print("❌ 未知参数。可用参数:")
            print("   --manual : 手动模式，显示所有图片供选择")
            print("   --match  : 智能匹配模式")
            print("   --all    : 全量下载模式")
            print("   --rename : 智能重命名模式")
            print("   --gemini : Gemini Vision 智能重命名模式")
    else:
        # 默认使用全量下载模式
        downloader.force_download_all = True
        downloader.search_and_download_images()


if __name__ == '__main__':
    main() 