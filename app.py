from flask import Flask, render_template
from fetcher.hacker_news_fetcher import fetch_hacker_news
from fetcher.economist_fetcher import fetch_economist_news
from fetcher.zhihu_fetcher import fetch_zhihu_hot
from fetcher.v2ex_fetcher import fetch_v2ex_hot
from fetcher.github_fetcher import fetch_github_trending
from fetcher.weibo_fetcher import fetch_weibo_hot
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# 缓存文件路径
CACHE_FILE = 'news_cache.json'

def load_cache():
    """从文件加载缓存数据"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('news', {}), datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
        except:
            return {}, None
    return {}, None

def save_cache(news_data):
    """保存缓存数据到文件"""
    cache_data = {
        'news': news_data,
        'timestamp': datetime.now().isoformat()
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def should_fetch_new_data():
    """检查是否需要重新获取数据"""
    news_cache, last_fetch_time = load_cache()
    if last_fetch_time is None:
        return True
    # 如果超过30分钟，返回True
    return datetime.now() - last_fetch_time > timedelta(minutes=30)

def fetch_all_news():
    """并行获取所有新闻数据"""
    with ThreadPoolExecutor(max_workers=6) as executor:
        # 并行执行所有爬取任务
        futures = {
            'hacker_news': executor.submit(fetch_hacker_news),
            'economist': executor.submit(fetch_economist_news),
            'zhihu': executor.submit(fetch_zhihu_hot),
            'v2ex': executor.submit(fetch_v2ex_hot),
            'github': executor.submit(fetch_github_trending),
            'weibo': executor.submit(fetch_weibo_hot)
        }
        
        # 获取所有结果
        news_data = {key: future.result() for key, future in futures.items()}
        
        # 保存到缓存文件
        save_cache(news_data)
        
        return news_data

@app.route('/')
def index():
    # 检查是否需要重新获取数据
    if should_fetch_new_data():
        print("Fetching new data...")  # 调试信息
        news_data = fetch_all_news()
    else:
        print("Using cached data...")  # 调试信息
        news_data, _ = load_cache()
    
    # 渲染模板
    return render_template('index.html',
                         hacker_news=news_data.get('hacker_news', []),
                         economist=news_data.get('economist', []),
                         zhihu=news_data.get('zhihu', []),
                         v2ex=news_data.get('v2ex', []),
                         github=news_data.get('github', []),
                         weibo=news_data.get('weibo', []))

if __name__ == '__main__':
    # 启动时先获取一次数据
    if should_fetch_new_data():
        fetch_all_news()
    app.run(debug=True)