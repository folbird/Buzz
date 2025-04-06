import requests
from bs4 import BeautifulSoup
import json
import time
import os

def fetch_v2ex_hot():
    """
    获取V2EX热门话题
    """
    try:
        url = "https://v2ex.com/?tab=hot"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://v2ex.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
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
        
        # 添加重试机制
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 使用代理发送请求
                response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
                response.raise_for_status()
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 打印页面内容，用于调试
                    print("页面标题:", soup.title.text if soup.title else "无标题")
                    
                    # 查找所有话题项
                    topics = soup.select('div.cell.item')
                    
                    if not topics:
                        print("未找到话题，尝试备用选择器")
                        # 备用选择器
                        topics = soup.select('.topic-link')
                    
                    articles = []
                    for topic in topics[:10]:  # 只取前10条
                        if isinstance(topic, str):
                            continue
                            
                        # 主选择器
                        title_element = topic.select_one('span.item_title a')
                        if not title_element:
                            # 备用选择器
                            title_element = topic.select_one('a.topic-link')
                            
                        if title_element:
                            title = title_element.text.strip()
                            # 确保URL是完整的
                            url = title_element.get('href', '')
                            if url.startswith('/'):
                                url = f"https://v2ex.com{url}"
                            elif not url.startswith('http'):
                                url = f"https://v2ex.com/{url}"
                                
                            if title and url:
                                articles.append({
                                    'title': title,
                                    'url': url
                                })
                    
                    if articles:
                        return articles
                    
                    print(f"未能获取到任何文章，重试第 {retry_count + 1} 次")
                    retry_count += 1
                    time.sleep(2)  # 等待2秒后重试
                    
            except requests.RequestException as e:
                print(f"请求错误: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)  # 等待2秒后重试
                continue
                
        return []
    except Exception as e:
        print(f"获取V2EX数据时发生错误: {e}")
        return []

if __name__ == "__main__":
    # 测试
    print("开始获取V2EX热门话题...")
    articles = fetch_v2ex_hot()
    if articles:
        print("\n成功获取到以下话题：")
        print(json.dumps(articles, ensure_ascii=False, indent=2))
    else:
        print("\n未能获取到任何话题") 