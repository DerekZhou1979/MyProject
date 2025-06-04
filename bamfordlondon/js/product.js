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
    const mainImage = document.getElementById('main-product-image');
    const thumbs = document.querySelectorAll('.thumb');
    
    thumbs.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // Remove active class from all thumbs
            thumbs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked thumb
            this.classList.add('active');
            
            // Change main image
            const newImage = this.getAttribute('data-image');
            if (mainImage && newImage) {
                mainImage.src = newImage;
                mainImage.style.opacity = '0';
                setTimeout(() => {
                    mainImage.style.opacity = '1';
                }, 50);
            }
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
    
    // ===== Product Customiser Functionality =====
    // Base price
    const basePrice = 6500;
    let currentPrice = basePrice;
    
    // Selected options
    const selectedOptions = {
        case: { value: 'steel', price: 0 },
        dial: { value: 'white', price: 0 },
        strap: { value: 'leather-black', price: 0 },
        engraving: { text: '', price: 0 }
    };
    
    // Option Selection
    const optionItems = document.querySelectorAll('.option-item');
    
    optionItems.forEach(item => {
        item.addEventListener('click', function() {
            const optionType = this.getAttribute('data-option');
            const optionValue = this.getAttribute('data-value');
            const optionPrice = parseInt(this.getAttribute('data-price') || 0);
            
            // Remove active class from siblings
            const siblings = this.parentElement.querySelectorAll('.option-item');
            siblings.forEach(sibling => sibling.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Update selected options
            selectedOptions[optionType] = {
                value: optionValue,
                price: optionPrice
            };
            
            // Update price
            updatePrice();
            
            // Update product image based on selection (mock functionality)
            updateProductImage();
        });
    });
    
    // Engraving Input
    const engravingInput = document.querySelector('.engraving-input input');
    if (engravingInput) {
        engravingInput.addEventListener('input', function() {
            const text = this.value.trim();
            selectedOptions.engraving = {
                text: text,
                price: text ? 150 : 0
            };
            updatePrice();
        });
    }
    
    // Update Price Display
    function updatePrice() {
        let optionsTotal = 0;
        
        for (const option in selectedOptions) {
            optionsTotal += selectedOptions[option].price;
        }
        
        currentPrice = basePrice + optionsTotal;
        
        // Update options price display
        const optionsPriceElement = document.querySelector('#options-price span:last-child');
        if (optionsPriceElement) {
            optionsPriceElement.textContent = `£${optionsTotal.toLocaleString()}`;
        }
        
        // Update total price display
        const totalPriceElement = document.getElementById('total-price');
        if (totalPriceElement) {
            totalPriceElement.textContent = `£${currentPrice.toLocaleString()}`;
        }
    }
    
    // Update Product Image (Mock functionality)
    function updateProductImage() {
        // In a real implementation, this would update the main image
        // based on the selected options combination
        console.log('Updating product image with options:', selectedOptions);
    }
    
    // Add to Cart
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            const product = {
                name: 'TAG Heuer Carrera Customised',
                price: currentPrice,
                options: selectedOptions,
                quantity: 1
            };
            
            console.log('Adding to cart:', product);
            
            // Update cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                const currentCount = parseInt(cartCount.textContent) || 0;
                cartCount.textContent = currentCount + 1;
            }
            
            // Show cart panel
            const cartPanel = document.querySelector('.cart-panel');
            if (cartPanel) {
                cartPanel.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
            
            // Show success message
            showNotification('Product added to cart');
        });
    }
    
    // Save Configuration
    const saveConfigBtn = document.querySelector('.save-config-btn');
    if (saveConfigBtn) {
        saveConfigBtn.addEventListener('click', function() {
            const config = {
                product: 'TAG Heuer Carrera',
                options: selectedOptions,
                price: currentPrice,
                date: new Date().toISOString()
            };
            
            // Save to localStorage (in real app, would save to user account)
            localStorage.setItem('savedConfig', JSON.stringify(config));
            
            showNotification('Configuration saved');
        });
    }
    
    // Product Details Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            this.classList.add('active');
            const targetPane = document.getElementById(targetTab);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
    
    // Show Notification
    function showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: var(--black);
            color: var(--white);
            padding: var(--spacing-sm) var(--spacing-lg);
            font-size: 14px;
            z-index: 3000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Fade in
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Initialize price display
    updatePrice();
    
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