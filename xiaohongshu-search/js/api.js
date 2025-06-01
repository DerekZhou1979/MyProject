/**
 * 小红书笔记搜索API接口
 * 与Python后端服务通信
 */

// API基础URL
const API_BASE_URL = 'http://localhost:8080/api';

/**
 * 获取小红书热门笔记
 * @param {string} keyword - 搜索关键词
 * @returns {Promise} - 返回包含笔记数据的Promise
 */
async function getRedBookNotes(keyword) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?keyword=${encodeURIComponent(keyword)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP错误! 状态: ${response.status}`);
        }
        
        const data = await response.json();
        return data.notes || [];
    } catch (error) {
        console.error('获取小红书笔记失败:', error);
        throw error;
    }
}

/**
 * 获取笔记详情
 * @param {string} noteId - 笔记ID
 * @returns {Promise} - 返回包含笔记详情的Promise
 */
async function getNoteDetail(noteId) {
    try {
        const response = await fetch(`${API_BASE_URL}/note/${noteId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP错误! 状态: ${response.status}`);
        }
        
        const data = await response.json();
        return data.note || null;
    } catch (error) {
        console.error('获取笔记详情失败:', error);
        throw error;
    }
}

/**
 * 获取热门搜索关键词
 * @returns {Promise} - 返回包含热门关键词的Promise
 */
async function getHotKeywords() {
    try {
        const response = await fetch(`${API_BASE_URL}/hot-keywords`);
        
        if (!response.ok) {
            throw new Error(`HTTP错误! 状态: ${response.status}`);
        }
        
        const data = await response.json();
        return data.keywords || [];
    } catch (error) {
        console.error('获取热门关键词失败:', error);
        return ['口红', '护肤品', '连衣裙', '耳机', '咖啡']; // 默认关键词
    }
} 