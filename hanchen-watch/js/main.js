document.addEventListener('DOMContentLoaded', function() {
    // 导航栏滚动效果
    const header = document.querySelector('header');
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const navIcons = document.querySelector('.nav-icons');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            header.style.height = '70px';
        } else {
            header.style.boxShadow = '0 1px 5px rgba(0, 0, 0, 0.1)';
            header.style.height = '80px';
        }
    });
    
    // 移动端菜单切换
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        
        if (hamburger.classList.contains('active')) {
            navLinks.style.display = 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '80px';
            navLinks.style.left = '0';
            navLinks.style.width = '100%';
            navLinks.style.backgroundColor = '#fff';
            navLinks.style.padding = '20px';
            navLinks.style.boxShadow = '0 5px 10px rgba(0, 0, 0, 0.1)';
            
            navIcons.style.display = 'flex';
            navIcons.style.position = 'absolute';
            navIcons.style.top = '250px';
            navIcons.style.left = '0';
            navIcons.style.width = '100%';
            navIcons.style.justifyContent = 'center';
            navIcons.style.padding = '20px';
            navIcons.style.backgroundColor = '#fff';
            navIcons.style.boxShadow = '0 5px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navLinks.style.display = '';
            navIcons.style.display = '';
        }
    });
    
    // 动态加载城市选项
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    
    if (provinceSelect && citySelect) {
        const cityData = {
            'beijing': ['东城区', '西城区', '朝阳区', '海淀区', '丰台区'],
            'shanghai': ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区'],
            'guangdong': ['广州市', '深圳市', '珠海市', '汕头市', '佛山市']
        };
        
        provinceSelect.addEventListener('change', function() {
            const selectedProvince = this.value;
            citySelect.innerHTML = '<option value="">选择城市</option>';
            
            if (selectedProvince && cityData[selectedProvince]) {
                cityData[selectedProvince].forEach(function(city) {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    citySelect.appendChild(option);
                });
            }
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 图片懒加载
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // 回退方案
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
    
    // 动画效果
    function animateOnScroll() {
        const elements = document.querySelectorAll('.feature, .series-item, .craft-item, .news-item');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animate');
            }
        });
    }
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // 初始检查
}); 