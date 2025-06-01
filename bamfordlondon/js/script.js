document.addEventListener('DOMContentLoaded', function() {
    // 侧边菜单交互
    const menuToggle = document.querySelector('.menu-toggle');
    const sideMenu = document.querySelector('.side-menu');
    const closeMenu = document.querySelector('.close-menu');
    const body = document.body;

    menuToggle.addEventListener('click', function() {
        sideMenu.classList.add('active');
        body.style.overflow = 'hidden';
    });

    closeMenu.addEventListener('click', function() {
        sideMenu.classList.remove('active');
        body.style.overflow = '';
    });

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

    // 搜索面板交互
    const searchIcon = document.querySelector('.search-icon');
    const searchPanel = document.querySelector('.search-panel');
    const closeSearch = document.querySelector('.close-search');

    searchIcon.addEventListener('click', function() {
        searchPanel.classList.add('active');
        body.style.overflow = 'hidden';
    });

    closeSearch.addEventListener('click', function() {
        searchPanel.classList.remove('active');
        body.style.overflow = '';
    });

    // 购物车面板交互
    const cartIcon = document.querySelector('.cart-icon');
    const cartPanel = document.querySelector('.cart-panel');
    const closeCart = document.querySelector('.close-cart');

    cartIcon.addEventListener('click', function() {
        cartPanel.classList.add('active');
        body.style.overflow = 'hidden';
    });

    closeCart.addEventListener('click', function() {
        cartPanel.classList.remove('active');
        body.style.overflow = '';
    });

    // 点击外部关闭菜单、搜索和购物车
    document.addEventListener('click', function(event) {
        // 侧边菜单
        if (sideMenu.classList.contains('active') && 
            !sideMenu.contains(event.target) && 
            !menuToggle.contains(event.target)) {
            sideMenu.classList.remove('active');
            body.style.overflow = '';
        }
        
        // 搜索面板
        if (searchPanel.classList.contains('active') && 
            !searchPanel.contains(event.target) && 
            !searchIcon.contains(event.target)) {
            searchPanel.classList.remove('active');
            body.style.overflow = '';
        }
        
        // 购物车面板
        if (cartPanel.classList.contains('active') && 
            !cartPanel.contains(event.target) && 
            !cartIcon.contains(event.target)) {
            cartPanel.classList.remove('active');
            body.style.overflow = '';
        }
    });

    // 首页轮播功能
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev-slide');
    const nextBtn = document.querySelector('.next-slide');
    let currentSlide = 0;
    const slideCount = slides.length;
    
    // 自动轮播
    let slideInterval = setInterval(nextSlide, 5000);
    
    // 切换到指定幻灯片
    function showSlide(n) {
        // 移除所有幻灯片的current类
        slides.forEach(slide => {
            slide.classList.remove('current');
        });
        
        // 移除所有点的active类
        dots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // 设置当前幻灯片和点的活动状态
        currentSlide = (n + slideCount) % slideCount;
        slides[currentSlide].classList.add('current');
        dots[currentSlide].classList.add('active');
    }
    
    // 下一张幻灯片
    function nextSlide() {
        showSlide(currentSlide + 1);
    }
    
    // 上一张幻灯片
    function prevSlide() {
        showSlide(currentSlide - 1);
    }
    
    // 点击控制按钮
    prevBtn.addEventListener('click', function() {
        clearInterval(slideInterval);
        prevSlide();
        slideInterval = setInterval(nextSlide, 5000);
    });
    
    nextBtn.addEventListener('click', function() {
        clearInterval(slideInterval);
        nextSlide();
        slideInterval = setInterval(nextSlide, 5000);
    });
    
    // 点击指示点
    dots.forEach((dot, index) => {
        dot.addEventListener('click', function() {
            clearInterval(slideInterval);
            showSlide(index);
            slideInterval = setInterval(nextSlide, 5000);
        });
    });
    
    // 鼠标悬停时暂停轮播
    const sliderContainer = document.querySelector('.hero-slider');
    sliderContainer.addEventListener('mouseenter', function() {
        clearInterval(slideInterval);
    });
    
    sliderContainer.addEventListener('mouseleave', function() {
        slideInterval = setInterval(nextSlide, 5000);
    });

    // 导航栏滚动效果
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 115) {
            // 向下滚动
            header.style.transform = 'translateY(-100%)';
        } else {
            // 向上滚动
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // 滚动时添加阴影
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 创建图片占位符
    function createPlaceholderImages() {
        // 轮播图片
        const heroImages = document.querySelectorAll('.hero-slider .slide img');
        const heroTitles = ['三足金乌三问报时', '斗转星移中华年历', '曜翼立体陀飞轮'];
        
        heroImages.forEach((img, index) => {
            if (index < heroTitles.length) {
                img.src = `https://via.placeholder.com/1920x1080/000000/ffffff?text=${heroTitles[index]}`;
            } else {
                img.src = `https://via.placeholder.com/1920x1080/000000/ffffff?text=海鸥腕表${index + 1}`;
            }
        });
        
        // 产品卡片图片
        const productImages = document.querySelectorAll('.product-card img');
        const productNames = ['大师海鸥', '大国工匠', '飞行系列', '海洋系列', '征途系列', '时间有她', '超凡系列', '边界系列'];
        
        productImages.forEach((img, index) => {
            if (index < productNames.length) {
                img.src = `https://via.placeholder.com/600x600/000000/ffffff?text=${productNames[index]}`;
            }
        });
        
        // 特色产品图片
        const featuredImage = document.querySelector('.featured-image img');
        if (featuredImage) {
            featuredImage.src = 'https://via.placeholder.com/800x1000/000000/ffffff?text=龙首磬音三合一机械腕表';
        }
        
        // 经典腕表图片
        const watchImages = document.querySelectorAll('.watch-item img');
        const watchNames = ['龙首磬音', '三足金乌', '斗转星移', '双秒追针', '五星表', '九龙图'];
        
        watchImages.forEach((img, index) => {
            if (index < watchNames.length) {
                img.src = `https://via.placeholder.com/400x400/000000/ffffff?text=${watchNames[index]}`;
            } else {
                img.src = `https://via.placeholder.com/400x400/000000/ffffff?text=经典腕表${index + 1}`;
            }
        });
        
        // 品牌特色图片
        const featureImages = document.querySelectorAll('.feature-image img');
        const featureTitles = ['复杂制表技术', '中国传统手艺'];
        
        featureImages.forEach((img, index) => {
            if (index < featureTitles.length) {
                img.src = `https://via.placeholder.com/800x500/000000/ffffff?text=${featureTitles[index]}`;
            }
        });
        
        // 新闻图片
        const newsImages = document.querySelectorAll('.news-item img');
        newsImages.forEach((img, index) => {
            img.src = `https://via.placeholder.com/600x400/000000/ffffff?text=新闻资讯${index + 1}`;
        });
        
        // 二维码图片
        const qrImages = document.querySelectorAll('.qr-code img');
        const qrTitles = ['防伪查询', '关注我们', '微信小程序'];
        
        qrImages.forEach((img, index) => {
            if (index < qrTitles.length) {
                img.src = `https://via.placeholder.com/150x150/000000/ffffff?text=${qrTitles[index]}`;
            }
        });
    }
    
    // 创建占位图片
    createPlaceholderImages();
}); 