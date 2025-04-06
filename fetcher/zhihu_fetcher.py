import requests
from bs4 import BeautifulSoup
import json

def fetch_zhihu_hot():
    """
    获取知乎热榜数据
    """
    try:
        # 知乎热榜API
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        articles = []
        for item in data.get('data', [])[:10]:  # 只取前10条
            title = item.get('target', {}).get('title', '')
            url = f"https://www.zhihu.com/question/{item.get('target', {}).get('id')}"
            
            articles.append({
                'title': title,
                'url': url
            })
            
        return articles
    except Exception as e:
        print(f"Error fetching Zhihu data: {e}")
        return []

if __name__ == "__main__":
    # 测试
    articles = fetch_zhihu_hot()
    print(json.dumps(articles, ensure_ascii=False, indent=2)) 