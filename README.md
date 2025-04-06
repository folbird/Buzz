# Buzz - 多源资讯聚合平台

Buzz 是一个强大的资讯聚合平台，实时汇总多个热门网站的最新信息，让您轻松掌握全球科技、新闻和社交媒体动态。

## 功能特点

- 🌐 多源聚合：同时获取多个平台的热门信息
  - Hacker News - 科技新闻
  - The Economist - 经济新闻
  - 知乎热榜
  - V2EX 热门话题
  - GitHub Trending
  - 微博热搜

- ⚡ 高效运行：
  - 多线程并行抓取
  - 智能缓存机制（30分钟自动更新）
  - 快速响应的 Web 界面

- 🛠 技术特点：
  - 基于 Flask 的轻量级架构
  - 模块化的爬虫设计
  - 响应式网页界面

## 环境要求

- Python 3.8+
- pip（Python 包管理器）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/folbird/Buzz.git
cd Buzz
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动应用：
```bash
python app.py
```

2. 打开浏览器访问：
```
http://localhost:5000
```

## 项目结构

```
Buzz/
├── app.py              # 主应用文件
├── requirements.txt    # 项目依赖
├── fetcher/           # 数据获取模块
│   ├── hacker_news_fetcher.py
│   ├── economist_fetcher.py
│   ├── zhihu_fetcher.py
│   ├── v2ex_fetcher.py
│   ├── github_fetcher.py
│   └── weibo_fetcher.py
├── static/           # 静态资源文件
│   ├── css/
│   └── js/
└── templates/        # HTML 模板文件
```

## 更新频率

- 所有数据每 30 分钟自动更新一次
- 访问首页时如果缓存过期会触发更新
- 首次启动时会自动获取所有数据

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

## 许可证

MIT License 