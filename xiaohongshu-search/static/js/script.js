document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const keywordLinks = document.querySelectorAll('.keyword');
    const loadingSection = document.getElementById('loading-section');
    const resultSection = document.getElementById('result-section');
    const emptyResult = document.getElementById('empty-result');
    const searchTermSpan = document.getElementById('search-term');
    const resultTimeDiv = document.getElementById('result-time');
    const resultContainer = document.getElementById('result-container');
    const modal = document.getElementById('note-modal');
    const modalBody = document.getElementById('modal-body');
    const closeModal = document.querySelector('.close-modal');
    
    // 默认logo图片加载失败时的占位图
    const logoImg = document.getElementById('logo-img');
    logoImg.onerror = function() {
        this.src = 'data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40"%3E%3Crect width="40" height="40" fill="%23fe2c55"%3E%3C/rect%3E%3Ctext x="50%25" y="50%25" font-size="20" text-anchor="middle" alignment-baseline="middle" font-family="Arial" fill="white"%3ER%3C/text%3E%3C/svg%3E';
    };
    
    // 进行搜索
    function performSearch(keyword) {
        // 如果搜索词为空，不执行搜索
        if (!keyword.trim()) {
            alert('请输入搜索关键词');
            return;
        }
        
        // 显示加载状态
        loadingSection.style.display = 'block';
        resultSection.style.display = 'none';
        emptyResult.style.display = 'none';
        
        // 更新搜索词显示
        searchTermSpan.textContent = keyword;
        
        // 使用API获取搜索结果
        getRedBookNotes(keyword)
            .then(data => {
                // 隐藏加载状态
                loadingSection.style.display = 'none';
                
                // 更新结果时间
                const now = new Date();
                resultTimeDiv.textContent = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
                
                // 检查是否有结果
                if (data && data.length > 0) {
                    // 显示结果区域
                    resultSection.style.display = 'block';
                    
                    // 清空之前的结果
                    resultContainer.innerHTML = '';
                    
                    // 生成结果卡片
                    data.forEach(note => {
                        const card = createNoteCard(note);
                        resultContainer.appendChild(card);
                    });
                } else {
                    // 显示空结果提示
                    emptyResult.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('搜索出错:', error);
                loadingSection.style.display = 'none';
                emptyResult.style.display = 'block';
            });
    }
    
    // 创建笔记卡片元素
    function createNoteCard(note) {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.dataset.noteId = note.id || '';
        
        // 创建图片占位符URL
        const imageUrl = note.cover || `https://via.placeholder.com/400x300/fe2c55/ffffff?text=${encodeURIComponent(note.title || '小红书笔记')}`;
        
        // 卡片HTML结构
        card.innerHTML = `
            <img src="${imageUrl}" alt="${note.title || ''}" class="note-image">
            <div class="note-content">
                <div class="note-title">${note.title || '无标题'}</div>
                <div class="note-description">${note.desc || '暂无描述'}</div>
                <div class="note-meta">
                    <div class="note-author">
                        <img src="${note.avatar || 'https://via.placeholder.com/40x40/fe2c55/ffffff?text=U'}" alt="${note.author || ''}" class="author-avatar">
                        <span>${note.author || '匿名用户'}</span>
                    </div>
                    <div class="note-stats">
                        <div class="note-stat"><i class="fas fa-heart"></i> ${formatNumber(note.likes)}</div>
                        <div class="note-stat"><i class="fas fa-comment"></i> ${formatNumber(note.comments)}</div>
                    </div>
                </div>
            </div>
        `;
        
        // 添加点击事件，打开详情模态框
        card.addEventListener('click', function() {
            openNoteDetail(note);
        });
        
        return card;
    }
    
    // 打开笔记详情模态框
    function openNoteDetail(note) {
        // 创建图片占位符URL
        const coverImageUrl = note.cover || `https://via.placeholder.com/800x600/fe2c55/ffffff?text=${encodeURIComponent(note.title || '小红书笔记')}`;
        
        // 格式化时间
        let publishedTime = '未知时间';
        if (note.published) {
            const date = new Date(note.published);
            publishedTime = isNaN(date) ? note.published : date.toLocaleDateString();
        }
        
        // 构建模态框内容
        modalBody.innerHTML = `
            <div class="modal-note-header">
                <h2 class="modal-note-title">${note.title || '无标题'}</h2>
                <div class="modal-note-author">
                    <img src="${note.avatar || 'https://via.placeholder.com/40x40/fe2c55/ffffff?text=U'}" class="modal-author-avatar">
                    <div class="modal-author-info">
                        <div class="modal-author-name">${note.author || '匿名用户'}</div>
                        <div class="modal-author-date">${publishedTime}</div>
                    </div>
                </div>
            </div>
            
            <div class="modal-note-images">
                <img src="${coverImageUrl}" class="modal-note-image">
                ${generateAdditionalImages(note)}
            </div>
            
            <div class="modal-note-content">
                ${note.content || note.desc || '暂无内容'}
            </div>
            
            <div class="modal-note-stats">
                <div class="modal-note-stat"><i class="fas fa-heart"></i> ${formatNumber(note.likes)} 赞</div>
                <div class="modal-note-stat"><i class="fas fa-comment"></i> ${formatNumber(note.comments)} 评论</div>
                <div class="modal-note-stat"><i class="fas fa-star"></i> ${formatNumber(note.collects)} 收藏</div>
                <div class="modal-note-stat"><i class="fas fa-share"></i> ${formatNumber(note.shares)} 分享</div>
            </div>
        `;
        
        // 显示模态框
        modal.style.display = 'block';
        
        // 阻止滚动
        document.body.style.overflow = 'hidden';
    }
    
    // 生成额外的图片HTML
    function generateAdditionalImages(note) {
        if (!note.images || !Array.isArray(note.images) || note.images.length === 0) {
            return '';
        }
        
        return note.images.map(img => {
            const imgUrl = img || `https://via.placeholder.com/300x300/fe2c55/ffffff?text=图片`;
            return `<img src="${imgUrl}" class="modal-note-image">`;
        }).join('');
    }
    
    // 格式化数字 (例如: 1000 -> 1k)
    function formatNumber(num) {
        if (num === undefined || num === null) return 0;
        
        num = Number(num);
        if (isNaN(num)) return 0;
        
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'm';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'k';
        } else {
            return num;
        }
    }
    
    // 关闭模态框
    function closeNoteDetail() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
    
    // 事件监听：搜索按钮点击
    searchButton.addEventListener('click', function() {
        performSearch(searchInput.value);
    });
    
    // 事件监听：输入框按Enter键
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            performSearch(searchInput.value);
        }
    });
    
    // 事件监听：热门关键词点击
    keywordLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const keyword = this.getAttribute('data-keyword');
            searchInput.value = keyword;
            performSearch(keyword);
        });
    });
    
    // 事件监听：关闭模态框
    closeModal.addEventListener('click', closeNoteDetail);
    
    // 点击模态框外部关闭
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeNoteDetail();
        }
    });
    
    // 按ESC键关闭模态框
    window.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeNoteDetail();
        }
    });

    // === 临时调试功能 - 后续需要删除 ===
    
    // 全局变量存储最后一次搜索的调试数据
    let lastSearchDebugData = null;
    
    // 获取调试相关的DOM元素
    const debugControls = document.getElementById('debug-controls');
    const showDebugBtn = document.getElementById('show-debug-btn');
    const debugModal = document.getElementById('debug-modal');
    const closeDebugModal = document.getElementById('close-debug-modal');
    const debugContent = document.getElementById('debug-content');
    
    // 修改原始的performSearch函数以支持调试
    const originalPerformSearch = performSearch;
    performSearch = function(keyword) {
        // 调用原始搜索函数
        originalPerformSearch(keyword);
        
        // 额外处理：检查是否返回了调试数据
        getRedBookNotes(keyword)
            .then(data => {
                if (data && data.length > 0 && data[0].debug_info && data[0].debug_info.is_debug) {
                    // 如果返回的是调试数据，保存并显示调试按钮
                    lastSearchDebugData = data;
                    debugControls.style.display = 'block';
                    console.log('检测到调试数据，显示调试按钮');
                } else {
                    // 隐藏调试按钮
                    debugControls.style.display = 'none';
                    lastSearchDebugData = null;
                }
            })
            .catch(error => {
                debugControls.style.display = 'none';
                lastSearchDebugData = null;
            });
    };
    
    // 显示调试信息
    function showDebugInfo() {
        if (!lastSearchDebugData || lastSearchDebugData.length === 0) {
            alert('没有可用的调试数据');
            return;
        }
        
        // 构建调试内容HTML
        let debugHTML = '';
        
        lastSearchDebugData.forEach((item, index) => {
            const debugInfo = item.debug_info || {};
            
            debugHTML += `
                <div style="border: 1px solid #ddd; margin-bottom: 20px; padding: 15px; border-radius: 5px; background: white;">
                    <h3 style="color: #333; margin: 0 0 10px 0; font-size: 16px;">
                        📄 调试项目 ${index + 1}: ${item.title}
                    </h3>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                        <div>
                            <strong style="color: #666;">🔗 原始链接:</strong>
                            <div style="background: #f8f9fa; padding: 8px; border-radius: 3px; font-family: monospace; font-size: 12px; word-break: break-all; margin-top: 5px;">
                                ${debugInfo.original_href || '无链接'}
                            </div>
                        </div>
                        
                        <div>
                            <strong style="color: #666;">📝 链接文本:</strong>
                            <div style="background: #f8f9fa; padding: 8px; border-radius: 3px; margin-top: 5px;">
                                ${debugInfo.link_text || '无文本'}
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #666;">📦 父元素内容:</strong>
                        <div style="background: #f8f9fa; padding: 8px; border-radius: 3px; max-height: 100px; overflow-y: auto; margin-top: 5px;">
                            ${debugInfo.parent_text || '无父元素内容'}
                        </div>
                    </div>
                    
                    ${debugInfo.img_src ? `
                    <div style="margin-bottom: 15px;">
                        <strong style="color: #666;">🖼️ 关联图片:</strong>
                        <div style="margin-top: 5px;">
                            <img src="${debugInfo.img_src}" style="max-width: 200px; max-height: 150px; border: 1px solid #ddd; border-radius: 3px;" 
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                            <div style="display: none; background: #f8f9fa; padding: 8px; border-radius: 3px; font-size: 12px;">
                                图片加载失败: ${debugInfo.img_src}
                            </div>
                        </div>
                    </div>
                    ` : ''}
                    
                    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                        <span style="background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 12px; font-size: 12px;">
                            ${debugInfo.link_type === 'other' ? '其他类型链接' : 'Explore链接'}
                        </span>
                        
                        ${debugInfo.original_href ? `
                        <button onclick="window.open('${debugInfo.original_href}', '_blank')" 
                                style="background: #4caf50; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-size: 12px;">
                            🔗 访问原链接
                        </button>
                        ` : ''}
                        
                        <button onclick="copyToClipboard('${(debugInfo.original_href || '').replace(/'/g, "\\'")}', this)" 
                                style="background: #2196f3; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-size: 12px;">
                            📋 复制链接
                        </button>
                    </div>
                </div>
            `;
        });
        
        // 添加统计信息
        const exploreLinks = lastSearchDebugData.filter(item => item.debug_info && item.debug_info.link_type !== 'other').length;
        const otherLinks = lastSearchDebugData.filter(item => item.debug_info && item.debug_info.link_type === 'other').length;
        
        debugHTML = `
            <div style="background: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h3 style="margin: 0 0 10px 0; color: #2e7d32;">📊 调试统计</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">${exploreLinks}</div>
                        <div style="font-size: 12px; color: #666;">Explore链接</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">${otherLinks}</div>
                        <div style="font-size: 12px; color: #666;">其他链接</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">${lastSearchDebugData.length}</div>
                        <div style="font-size: 12px; color: #666;">总计</div>
                    </div>
                </div>
            </div>
        ` + debugHTML;
        
        debugContent.innerHTML = debugHTML;
        debugModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    
    // 复制到剪贴板函数
    window.copyToClipboard = function(text, button) {
        navigator.clipboard.writeText(text).then(function() {
            const originalText = button.innerHTML;
            button.innerHTML = '✅ 已复制';
            button.style.background = '#4caf50';
            setTimeout(function() {
                button.innerHTML = originalText;
                button.style.background = '#2196f3';
            }, 2000);
        }).catch(function(err) {
            console.error('复制失败:', err);
            alert('复制失败，请手动复制');
        });
    };
    
    // 关闭调试模态框
    function closeDebugModalFn() {
        debugModal.style.display = 'none';
        document.body.style.overflow = '';
    }
    
    // 事件监听：显示调试信息按钮
    if (showDebugBtn) {
        showDebugBtn.addEventListener('click', showDebugInfo);
    }
    
    // 事件监听：关闭调试模态框
    if (closeDebugModal) {
        closeDebugModal.addEventListener('click', closeDebugModalFn);
    }
    
    // 点击调试模态框外部关闭
    window.addEventListener('click', function(event) {
        if (event.target === debugModal) {
            closeDebugModalFn();
        }
    });
    
    // ESC键关闭调试模态框
    window.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && debugModal.style.display === 'block') {
            closeDebugModalFn();
        }
    });
    
    // === 临时调试功能结束 ===
    
}); 