document.addEventListener('DOMContentLoaded', function() {
    // 侧边菜单中的多级导航
    const dropdownToggles = document.querySelectorAll('.side-nav .dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // 阻止默认行为，防止点击链接时立即跳转
            e.preventDefault();
            
            // 切换当前菜单项的active状态
            this.classList.toggle('active');
            
            // 获取下一级菜单
            const dropdownMenu = this.nextElementSibling;
            
            // 切换下一级菜单的显示状态
            if (dropdownMenu) {
                dropdownMenu.classList.toggle('show');
            }
        });
    });
    
    // 图片切换功能
    const mainImage = document.getElementById('main-image');
    const thumbs = document.querySelectorAll('.thumb');
    
    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // 获取当前缩略图的图片路径
            const imagePath = this.getAttribute('data-image');
            
            // 更新主图
            mainImage.src = imagePath;
            
            // 更新active状态
            thumbs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // 颜色选项
    const colorOptions = document.querySelectorAll('.color-option');
    
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            colorOptions.forEach(o => o.classList.remove('active'));
            this.classList.add('active');
            
            // 可以在这里添加更新产品图片的逻辑，例如：
            // const color = this.getAttribute('data-color');
            // updateProductImages(color);
        });
    });
    
    // 表带选项
    const strapOptions = document.querySelectorAll('.strap-option');
    
    strapOptions.forEach(option => {
        option.addEventListener('click', function() {
            strapOptions.forEach(o => o.classList.remove('active'));
            this.classList.add('active');
            
            // 可以在这里添加更新价格或产品图片的逻辑
        });
    });
    
    // 数量控制
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.plus');
    const quantityInput = document.querySelector('.quantity-input');
    
    minusBtn.addEventListener('click', function() {
        let value = parseInt(quantityInput.value);
        if (value > 1) {
            quantityInput.value = value - 1;
        }
    });
    
    plusBtn.addEventListener('click', function() {
        let value = parseInt(quantityInput.value);
        if (value < parseInt(quantityInput.max)) {
            quantityInput.value = value + 1;
        }
    });
    
    // 确保数量输入框的值在范围内
    quantityInput.addEventListener('change', function() {
        let value = parseInt(this.value);
        const min = parseInt(this.min);
        const max = parseInt(this.max);
        
        if (value < min) {
            this.value = min;
        } else if (value > max) {
            this.value = max;
        }
    });
    
    // 加入购物车按钮
    const addToCartBtn = document.querySelector('.add-to-cart');
    
    addToCartBtn.addEventListener('click', function() {
        const quantity = parseInt(quantityInput.value);
        const selectedColor = document.querySelector('.color-option.active').getAttribute('data-color');
        const selectedStrap = document.querySelector('.strap-option.active').getAttribute('data-strap');
        
        // 模拟添加到购物车
        alert(`已添加到购物车：「三足金乌」三问报时金雕动偶腕表\n表壳材质：${selectedColor}\n表带：${selectedStrap}\n数量：${quantity}`);
        
        // 在实际应用中，这里会发送AJAX请求到服务器
    });
    
    // 选项卡切换
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 获取目标选项卡
            const targetTab = this.getAttribute('data-tab');
            
            // 移除所有按钮的active类
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // 为当前按钮添加active类
            this.classList.add('active');
            
            // 隐藏所有选项卡内容
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // 显示目标选项卡内容
            document.getElementById(targetTab).classList.add('active');
        });
    });
    
    // 创建产品图片占位符
    function createProductPlaceholders() {
        // 主图片
        if (mainImage) {
            mainImage.src = 'https://via.placeholder.com/600x600/000000/ffffff?text=三足金乌三问报时金雕动偶腕表';
        }
        
        // 缩略图
        const thumbImages = document.querySelectorAll('.thumb img');
        const thumbTitles = ['正面', '侧面', '背面', '细节'];
        thumbImages.forEach((img, index) => {
            if (index < thumbTitles.length) {
                img.src = `https://via.placeholder.com/100x100/000000/ffffff?text=${thumbTitles[index]}`;
            } else {
                img.src = `https://via.placeholder.com/100x100/000000/ffffff?text=细节${index + 1}`;
            }
        });
        
        // 相关产品图片
        const relatedImages = document.querySelectorAll('.related-item img');
        const relatedTitles = ['斗转星移', '九龙图', '龙首磬音', '曜翼'];
        relatedImages.forEach((img, index) => {
            if (index < relatedTitles.length) {
                img.src = `https://via.placeholder.com/300x300/000000/ffffff?text=${relatedTitles[index]}`;
            } else {
                img.src = `https://via.placeholder.com/300x300/000000/ffffff?text=相关产品${index + 1}`;
            }
        });
    }
    
    // 创建占位图片
    createProductPlaceholders();
}); 