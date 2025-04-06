import requests
from bs4 import BeautifulSoup
import time
import os
import feedparser

def fetch_economist_news(limit=10):
    """
    从经济学人RSS源抓取指定数量的文章数据。
    """
    # 使用经济学人的RSS源
    rss_urls = [
        "https://www.economist.com/the-world-this-week/rss.xml",
        "https://www.economist.com/finance-and-economics/rss.xml"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # 设置代理
    proxies = None
    try:
        # 从环境变量获取代理，如果没有则使用默认代理
        http_proxy = os.getenv('HTTP_PROXY', 'http://127.0.0.1:10808')
        https_proxy = os.getenv('HTTPS_PROXY', 'http://127.0.0.1:10808')
        
        proxies = {
            'http': http_proxy,
            'https': https_proxy
        }
        print(f"使用代理: {proxies}")
    except Exception as e:
        print(f"代理设置失败: {e}")
        proxies = None
    
    all_entries = []
    
    try:
        for rss_url in rss_urls:
            print(f"\n尝试获取RSS源: {rss_url}")
            try:
                # 使用requests获取RSS内容
                response = requests.get(rss_url, headers=headers, proxies=proxies, timeout=10)
                response.raise_for_status()
                
                # 使用feedparser解析RSS内容
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    print(f"成功从 {rss_url} 获取到 {len(feed.entries)} 篇文章")
                    all_entries.extend(feed.entries)
                else:
                    print(f"未从 {rss_url} 获取到任何文章")
                    
            except Exception as e:
                print(f"获取RSS源 {rss_url} 失败: {e}")
                continue
        
        # 对所有文章按发布时间排序（如果有发布时间的话）
        all_entries.sort(key=lambda x: x.get('published_parsed', 0), reverse=True)
        
        # 提取前limit篇文章
        headlines = []
        for entry in all_entries[:limit]:
            # 获取文章图片
            image_url = None
            if 'media_content' in entry:
                for media in entry.media_content:
                    if 'url' in media and media.get('type', '').startswith('image/'):
                        image_url = media['url']
                        break
            
            # 如果没有找到图片，尝试从文章内容中提取
            if not image_url and 'content' in entry:
                soup = BeautifulSoup(entry.content[0].value, 'html.parser')
                img_tag = soup.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    image_url = img_tag['src']
            
            headlines.append({
                'title': entry.get('title', '').strip(),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'summary': entry.get('summary', ''),
                'image_url': image_url
            })
            
        return headlines
            
    except Exception as e:
        print(f"发生未知错误: {e}")
        return []

if __name__ == "__main__":
    print("开始获取经济学人文章...")
    economist_data = fetch_economist_news(10)  # 获取前 10 篇文章
    if economist_data:
        print("\n成功获取到以下文章：")
        for item in economist_data:
            print(f"标题: {item['title']}")
            print(f"链接: {item['link']}")
            if item.get('published'):
                print(f"发布时间: {item['published']}")
            if item.get('image_url'):
                print(f"图片链接: {item['image_url']}")
            print("-" * 20)
    else:
        print("\n未能获取到任何文章")