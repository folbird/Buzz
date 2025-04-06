import requests
from bs4 import BeautifulSoup
import json

def fetch_weibo_hot():
    """
    获取微博热搜榜
    """
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        articles = []
        for item in data.get('data', {}).get('realtime', [])[:10]:  # 只取前10条
            title = item.get('note', '')
            url = f"https://s.weibo.com/weibo?q={requests.utils.quote(title)}"
            
            articles.append({
                'title': title,
                'url': url
            })
            
        return articles
    except Exception as e:
        print(f"Error fetching Weibo data: {e}")
        return []

if __name__ == "__main__":
    # 测试
    articles = fetch_weibo_hot()
    print(json.dumps(articles, ensure_ascii=False, indent=2)) 