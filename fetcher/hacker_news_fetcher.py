import requests
import time
from bs4 import BeautifulSoup

def fetch_hacker_news(limit=10):
    """
    从 Hacker News 获取指定数量的热门文章数据。
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    try:
        # 设置超时时间为 5 秒
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        top_story_ids = response.json()[:limit]
        stories = []
        
        # 使用并发请求来加快速度
        for story_id in top_story_ids:
            try:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=3)
                story_response.raise_for_status()
                story_data = story_response.json()
                
                if story_data and 'title' in story_data and 'url' in story_data:
                    # 获取文章图片
                    image_url = None
                    try:
                        # 尝试从文章页面获取图片
                        article_response = requests.get(story_data['url'], timeout=5)
                        if article_response.status_code == 200:
                            soup = BeautifulSoup(article_response.content, 'html.parser')
                            # 尝试不同的图片选择器
                            img_selectors = [
                                'meta[property="og:image"]',
                                'meta[name="twitter:image"]',
                                'img[src*="http"]'
                            ]
                            for selector in img_selectors:
                                img_tag = soup.select_one(selector)
                                if img_tag:
                                    if selector.startswith('meta'):
                                        image_url = img_tag.get('content')
                                    else:
                                        image_url = img_tag.get('src')
                                    if image_url:
                                        break
                    except Exception as e:
                        print(f"获取文章图片失败: {e}")
                    
                    stories.append({
                        'title': story_data.get('title', ''),
                        'url': story_data.get('url', ''),
                        'score': story_data.get('score', 0),
                        'by': story_data.get('by', 'Unknown'),
                        'time': story_data.get('time', 0),
                        'image_url': image_url
                    })
            except (requests.exceptions.RequestException, KeyError) as e:
                print(f"获取故事 {story_id} 失败: {e}")
                continue
                
        return stories
    except requests.exceptions.RequestException as e:
        print(f"获取 Hacker News 数据失败: {e}")
        return []
    except Exception as e:
        print(f"发生未知错误: {e}")
        return []

if __name__ == "__main__":
    hn_data = fetch_hacker_news(5)  # 获取前 5 篇文章作为示例
    for item in hn_data:
        print(f"标题: {item.get('title')}")
        print(f"链接: {item.get('url')}")
        if item.get('image_url'):
            print(f"图片链接: {item.get('image_url')}")
        print("-" * 20)