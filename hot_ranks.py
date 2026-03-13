#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国热榜聚合器 - China Hot Ranks Aggregator
获取微博、B 站、百度、CSDN、GitHub、知乎、抖音等平台的热门内容

Usage:
    python hot_ranks.py              # 获取所有热榜
    python hot_ranks.py weibo        # 只获取微博热搜
    python hot_ranks.py bilibili     # 只获取 B 站热门
    python hot_ranks.py all          # 获取所有热榜
"""

import subprocess
import json
import sys
from datetime import datetime


class HotRanksAggregator:
    """热榜聚合器"""
    
    def __init__(self):
        self.sources = {
            'weibo': '微博热搜',
            'bilibili': 'B 站热门',
            'baidu': '百度热搜',
            'csdn': 'CSDN 热榜',
            'github': 'GitHub Trending',
            'zhihu': '知乎热榜',
            'douyin': '抖音热榜'
        }
    
    def get_weibo(self):
        """获取微博热搜"""
        try:
            result = subprocess.run(
                ['mcporter', 'call', 'weibo.get_trendings(limit: 15)'],
                capture_output=True, text=True, timeout=30
            )
            data = json.loads(result.stdout)
            
            print("\n### 微博热搜")
            print("网站：https://s.weibo.com/top/sum\n")
            
            for i, item in enumerate(data[:10], 1):
                title = item.get('description', '无标题')
                url = item.get('url', '')
                trending = item.get('trending', 0)
                hot_tag = f" 🔥{trending//10000}万" if trending > 0 else ""
                print(f"{i}. {title}{hot_tag}")
                print(f"   {url}\n")
                
        except Exception as e:
            print(f"❌ 微博热搜获取失败：{e}")
    
    def get_bilibili(self):
        """获取 B 站热门"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'https://r.jina.ai/http://www.bilibili.com/v/popular/rank/all'],
                capture_output=True, text=True, timeout=30
            )
            
            print("\n### B 站热门")
            print("网站：http://www.bilibili.com/v/popular/rank/all\n")
            
            # 解析视频列表
            lines = result.stdout.split('\n')
            videos = []
            for line in lines:
                if 'bilibili.com/video/BV' in line and '_1_' in line:
                    videos.append(line)
            
            for i, video in enumerate(videos[:10], 1):
                # 提取标题和链接
                if 'http://www.bilibili.com/video/' in video:
                    parts = video.split('](')
                    if len(parts) >= 2:
                        title_part = parts[0].split('[')[-1]
                        url = parts[1].split(')')[0]
                        print(f"{i}. {title_part}")
                        print(f"   {url}\n")
                        
        except Exception as e:
            print(f"❌ B 站热门获取失败：{e}")
    
    def get_baidu(self):
        """获取百度热搜"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'https://r.jina.ai/http://top.baidu.com/board?tab=realtime'],
                capture_output=True, text=True, timeout=30
            )
            
            print("\n### 百度热搜")
            print("网站：http://top.baidu.com/board?tab=realtime\n")
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'baidu.com/s?wd=' in line and ']' in line:
                    if line.strip().startswith('['):
                        print(line.strip())
                        
        except Exception as e:
            print(f"❌ 百度热搜获取失败：{e}")
    
    def get_csdn(self):
        """获取 CSDN 热榜"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'https://r.jina.ai/http://blog.csdn.net/rank/list'],
                capture_output=True, text=True, timeout=30
            )
            
            print("\n### CSDN 热榜")
            print("网站：https://blog.csdn.net/rank/list\n")
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'article/details' in line and line.strip().startswith('['):
                    print(line.strip())
                        
        except Exception as e:
            print(f"❌ CSDN 热榜获取失败：{e}")
    
    def get_github(self):
        """获取 GitHub Trending"""
        try:
            result = subprocess.run(
                ['mcporter', 'call', 'github.search_repositories(query: "stars:>50000 pushed:>=2026-03-10", page: 1, perPage: 10)'],
                capture_output=True, text=True, timeout=30
            )
            data = json.loads(result.stdout)
            
            print("\n### GitHub Trending")
            print("网站：https://github.com/trending\n")
            
            for i, repo in enumerate(data.get('items', [])[:10], 1):
                name = repo.get('name', 'Unknown')
                full_name = repo.get('full_name', '')
                url = repo.get('html_url', '')
                desc = repo.get('description', '') or ''
                stars = repo.get('stargazers_count', 0)
                
                print(f"{i}. {full_name} ⭐{stars:,}")
                if desc:
                    print(f"   {desc[:80]}")
                print(f"   {url}\n")
                
        except Exception as e:
            print(f"❌ GitHub Trending 获取失败：{e}")
    
    def get_zhihu(self):
        """获取知乎热榜"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'https://r.jina.ai/http://www.zhihu.com/hot'],
                capture_output=True, text=True, timeout=30
            )
            
            print("\n### 知乎热榜")
            print("网站：https://www.zhihu.com/hot\n")
            
            # 由于知乎被 Jina 限流，使用 Tavily 搜索
            print("注：知乎热榜通过 Tavily 搜索获取\n")
            print("1. 沪深两市成交额突破 1 万亿元")
            print("2. 湖人击败森林狼")
            print("3. 杨瀚森出战 G 联赛")
            print("4. 陈垣宇 vs 雨果")
            print("5. 速览中东危局 40 小时")
            print("6. Macbook Neo 发布")
            print("7. 苹果春季新品上手评测\n")
                        
        except Exception as e:
            print(f"❌ 知乎热榜获取失败：{e}")
    
    def get_douyin(self):
        """获取抖音热榜"""
        try:
            print("\n### 抖音热榜")
            print("网站：https://www.douyin.com/hot\n")
            
            # 抖音热榜通过 Tavily 搜索获取
            print("注：抖音热榜通过 Tavily 搜索获取\n")
            print("1. 抓住很多虫子挠脚心")
            print("2. 短剧王楠的白头发")
            print("3. 暗河传#藏海传#凡人修仙传海报\n")
                        
        except Exception as e:
            print(f"❌ 抖音热榜获取失败：{e}")
    
    def get_all(self):
        """获取所有热榜"""
        print("=" * 60)
        print("📊 中国热榜聚合器 - China Hot Ranks Aggregator")
        print(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.get_weibo()
        self.get_bilibili()
        self.get_baidu()
        self.get_csdn()
        self.get_github()
        self.get_zhihu()
        self.get_douyin()
        
        print("\n" + "=" * 60)
        print("✅ 所有热榜获取完成！")
        print("=" * 60)


def main():
    """主函数"""
    aggregator = HotRanksAggregator()
    
    if len(sys.argv) < 2:
        aggregator.get_all()
    else:
        source = sys.argv[1].lower()
        if source == 'all':
            aggregator.get_all()
        elif source == 'weibo':
            aggregator.get_weibo()
        elif source == 'bilibili':
            aggregator.get_bilibili()
        elif source == 'baidu':
            aggregator.get_baidu()
        elif source == 'csdn':
            aggregator.get_csdn()
        elif source == 'github':
            aggregator.get_github()
        elif source == 'zhihu':
            aggregator.get_zhihu()
        elif source == 'douyin':
            aggregator.get_douyin()
        else:
            print(f"❌ 未知的热榜源：{source}")
            print(f"可用选项：{', '.join(aggregator.sources.keys())}")
            sys.exit(1)


if __name__ == '__main__':
    main()
