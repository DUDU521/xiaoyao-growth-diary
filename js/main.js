// 逍遥成长日记网站交互脚本

document.addEventListener('DOMContentLoaded', function() {
    // 导航栏滚动效果
    const header = document.querySelector('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // 向下滚动 - 隐藏导航栏
            header.classList.add('hidden');
        } else {
            // 向上滚动 - 显示导航栏
            header.classList.remove('hidden');
        }
        lastScrollTop = scrollTop;
    });
    
    // 分类筛选功能
    const categoryFilters = document.querySelectorAll('.category-filter');
    const posts = document.querySelectorAll('.post-item');
    
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // 更新激活状态
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            // 筛选文章
            posts.forEach(post => {
                if (category === 'all' || post.dataset.categories.includes(category)) {
                    post.style.display = 'block';
                } else {
                    post.style.display = 'none';
                }
            });
        });
    });
    
    // 搜索功能
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            posts.forEach(post => {
                const title = post.querySelector('.post-title').textContent.toLowerCase();
                const content = post.querySelector('.post-excerpt').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    post.style.display = 'block';
                } else {
                    post.style.display = 'none';
                }
            });
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
    
    // 动态统计更新
    updateStats();
});

function updateStats() {
    const statsElement = document.getElementById('stats-count');
    if (statsElement) {
        const now = new Date();
        const startDate = new Date('2026-03-18'); // 项目开始日期
        const daysActive = Math.floor((now - startDate) / (1000 * 60 * 60 * 24));
        
        // 模拟统计数据（实际数据可以从API获取）
        const stats = {
            totalRecords: 157,
            methodologyCount: 42,
            pitfallCount: 38,
            toolDiscoveryCount: 29,
            lastUpdate: now.toLocaleDateString('zh-CN')
        };
        
        statsElement.innerHTML = `
            <div class="stat-item">
                <span class="stat-number">${stats.totalRecords}</span>
                <span class="stat-label">总记录数</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${stats.methodologyCount}</span>
                <span class="stat-label">方法论</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${stats.pitfallCount}</span>
                <span class="stat-label">踩坑记录</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${stats.toolDiscoveryCount}</span>
                <span class="stat-label">工具发现</span>
            </div>
        `;
    }
}

// 主题切换功能
function toggleTheme() {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
        themeToggle.textContent = '🌙';
    } else {
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
        themeToggle.textContent = '☀️';
    }
}

// 初始化主题
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const themeToggle = document.getElementById('theme-toggle');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        if (themeToggle) themeToggle.textContent = '☀️';
    } else {
        if (themeToggle) themeToggle.textContent = '🌙';
    }
}

// 页面加载完成后初始化主题
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}