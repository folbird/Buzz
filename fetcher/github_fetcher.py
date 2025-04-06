import requests
from bs4 import BeautifulSoup
import json
import time
import os

def fetch_github_trending():
    """
    获取GitHub Trending仓库
    """
    try:
        url = "https://github.com/trending"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
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
                    
                    articles = []
                    repositories = soup.select('article.Box-row')[:10]  # 只取前10条
                    
                    for repo in repositories:
                        # 更新选择器以适应GitHub的新布局
                        title_element = repo.select_one('h2.h3')
                        if title_element:
                            repo_name = title_element.text.strip().replace('\n', '').replace(' ', '')
                            # 从a标签直接获取href
                            repo_link = title_element.select_one('a')
                            if repo_link and repo_link.get('href'):
                                repo_url = f"https://github.com{repo_link['href']}"
                                description = repo.select_one('p')
                                description_text = description.text.strip() if description else ""
                                
                                articles.append({
                                    'title': f"{repo_name} - {description_text}",
                                    'url': repo_url
                                })
                    
                    if articles:
                        return articles
                    
                    print(f"未能获取到任何仓库，重试第 {retry_count + 1} 次")
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
        print(f"获取GitHub数据时发生错误: {e}")
        return []

if __name__ == "__main__":
    # 测试
    print("开始获取GitHub Trending仓库...")
    articles = fetch_github_trending()
    if articles:
        print("\n成功获取到以下仓库：")
        print(json.dumps(articles, ensure_ascii=False, indent=2))
    else:
        print("\n未能获取到任何仓库") 