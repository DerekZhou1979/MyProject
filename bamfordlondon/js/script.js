document.addEventListener('DOMContentLoaded', function() {
    // 侧边菜单交互
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const closeMenu = document.querySelector('.close-menu');
    const body = document.body;

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.add('active');
            body.style.overflow = 'hidden';
        });

        closeMenu.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            body.style.overflow = '';
        });
    }

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

    if (searchIcon && searchPanel) {
        searchIcon.addEventListener('click', (e) => {
            e.preventDefault();
            searchPanel.classList.add('active');
            body.style.overflow = 'hidden';
            // Focus on search input
            const searchInput = searchPanel.querySelector('.search-input');
            if (searchInput) {
                setTimeout(() => searchInput.focus(), 300);
            }
        });

        closeSearch.addEventListener('click', () => {
            searchPanel.classList.remove('active');
            body.style.overflow = '';
        });
    }

    // 购物车面板交互
    const cartIcon = document.querySelector('.cart-icon');
    const cartPanel = document.querySelector('.cart-panel');
    const closeCart = document.querySelector('.close-cart');

    if (cartIcon && cartPanel) {
        cartIcon.addEventListener('click', (e) => {
            e.preventDefault();
            cartPanel.classList.add('active');
            body.style.overflow = 'hidden';
        });

        closeCart.addEventListener('click', () => {
            cartPanel.classList.remove('active');
            body.style.overflow = '';
        });
    }

    // 点击外部关闭菜单、搜索和购物车
    document.addEventListener('click', function(event) {
        // 侧边菜单
        if (mobileMenu && mobileMenu.classList.contains('active') && 
            !mobileMenu.contains(event.target) && 
            !menuToggle.contains(event.target)) {
            mobileMenu.classList.remove('active');
            body.style.overflow = '';
        }
        
        // 搜索面板
        if (searchPanel && searchPanel.classList.contains('active') && 
            !searchPanel.contains(event.target) && 
            !searchIcon.contains(event.target)) {
            searchPanel.classList.remove('active');
            body.style.overflow = '';
        }
        
        // 购物车面板
        if (cartPanel && cartPanel.classList.contains('active') && 
            !cartPanel.contains(event.target) && 
            !cartIcon.contains(event.target)) {
            cartPanel.classList.remove('active');
            body.style.overflow = '';
        }
    });

    // 首页轮播功能
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroDots = document.querySelectorAll('.hero-dots .dot');
    const heroPrev = document.querySelector('.hero-prev');
    const heroNext = document.querySelector('.hero-next');
    let currentSlide = 0;
    const slideCount = heroSlides.length;
    
    // 自动轮播
    let slideInterval = setInterval(nextSlide, 5000);
    
    // 切换到指定幻灯片
    function showSlide(n) {
        // 移除所有幻灯片的active类
        heroSlides.forEach(slide => {
            slide.classList.remove('active');
        });
        
        // 移除所有点的active类
        heroDots.forEach(dot => {
            dot.classList.remove('active');
        });
        
        // 设置当前幻灯片和点的活动状态
        currentSlide = (n + slideCount) % slideCount;
        heroSlides[currentSlide].classList.add('active');
        heroDots[currentSlide].classList.add('active');
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
    if (heroPrev && heroNext) {
        heroPrev.addEventListener('click', function() {
            clearInterval(slideInterval);
            prevSlide();
            slideInterval = setInterval(nextSlide, 5000);
        });
        
        heroNext.addEventListener('click', function() {
            clearInterval(slideInterval);
            nextSlide();
            slideInterval = setInterval(nextSlide, 5000);
        });
    }
    
    // 点击指示点
    heroDots.forEach((dot, index) => {
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
    const header = document.querySelector('.main-header');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        // Show header when scrolling up
        if (currentScroll < lastScroll && currentScroll > 100) {
            header.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
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

    // ===== Newsletter Form =====
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = newsletterForm.querySelector('.newsletter-input').value;
            if (email) {
                alert('Thank you for subscribing!');
                newsletterForm.reset();
            }
        });
    }

    // ===== Smooth Scroll =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== Intersection Observer for Animations =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements
    document.querySelectorAll('.grid-item, .news-item, .featured-container').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // ===== Close panels on ESC key =====
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (mobileMenu && mobileMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
            if (searchPanel && searchPanel.classList.contains('active')) {
                searchPanel.classList.remove('active');
                document.body.style.overflow = '';
            }
            if (cartPanel && cartPanel.classList.contains('active')) {
                cartPanel.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });

    // ===== Prevent body scroll when panels are open =====
    function preventBodyScroll(panel) {
        panel.addEventListener('wheel', (e) => {
            const isScrollable = panel.scrollHeight > panel.clientHeight;
            const scrollTop = panel.scrollTop;
            const scrollHeight = panel.scrollHeight;
            const height = panel.clientHeight;
            const delta = e.deltaY;
            const up = delta < 0;

            if (!isScrollable) {
                e.preventDefault();
                return;
            }

            if (!up && (scrollHeight - scrollTop - height) < 1) {
                e.preventDefault();
            } else if (up && scrollTop < 1) {
                e.preventDefault();
            }
        });
    }

    // Apply to panels
    [mobileMenu, searchPanel, cartPanel].forEach(panel => {
        if (panel) preventBodyScroll(panel);
    });

    // ===== Loading Animation =====
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });

    // ===== Product Grid Hover Effect =====
    const gridItems = document.querySelectorAll('.grid-item');
    gridItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.zIndex = '10';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.zIndex = '';
        });
    });

    console.log('Bamford London - Luxury Watch Customisation');
}); 