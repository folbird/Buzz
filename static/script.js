document.addEventListener('DOMContentLoaded', function() {
    // 为每个新闻项添加点击效果
    const newsItems = document.querySelectorAll('.news-item');
    newsItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // 防止点击链接时触发背景效果
            if (e.target.tagName.toLowerCase() === 'a') {
                return;
            }
            const originalBg = this.style.backgroundColor;
            this.style.backgroundColor = '#f0f8ff';
            setTimeout(() => {
                this.style.backgroundColor = originalBg;
            }, 200);
        });
    });

    // 添加页面加载动画
    const container = document.querySelector('.container');
    container.style.opacity = '0';
    container.style.transition = 'opacity 0.5s ease-in-out';
    
    setTimeout(() => {
        container.style.opacity = '1';
    }, 100);
}); 