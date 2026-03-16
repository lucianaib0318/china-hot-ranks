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
        """获取微博热搜（微博 MCP + Jina Reader 备用方案）"""
        print("\n### 微博热搜")
        print("网站：https://s.weibo.com/top/sum\n")
        
        # 方案 1：使用微博 MCP
        try:
            result = subprocess.run(
                ['mcporter', 'call', 'weibo.get_trendings(limit: 15)'],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                if isinstance(data, list) and len(data) > 0:
                    for i, item in enumerate(data[:10], 1):
                        title = item.get('description', '无标题')
                        url = item.get('url', '')
                        trending = item.get('trending', 0)
                        hot_tag = f" 🔥{trending//10000}万" if trending > 0 else ""
                        print(f"{i}. {title}{hot_tag}")
                        print(f"   {url}\n")
                    return
        except Exception:
            pass
        
        # 方案 2：使用 Jina Reader 读取微博热搜页面
        print("⚠️  微博 MCP 不可用，使用备用方案...\n")
        
        try:
            result = subprocess.run(
                ['curl', '-s', '-A', 'Mozilla/5.0', 'https://r.jina.ai/http://s.weibo.com/top/sum'],
                capture_output=True, text=True, timeout=45
            )
            
            lines = result.stdout.split('\n')
            rank = 1
            for line in lines:
                # 匹配格式：数字。话题 🔥热度
                line = line.strip()
                if len(line) > 5 and not line.startswith('http') and not line.startswith('Image'):
                    # 清理无用前缀
                    if line.startswith('['):
                        line = line.split('](')[-1].split(')')[0] if '](' in line else line
                    if line and len(line) > 3:
                        print(f"{rank}. {line}")
                        rank += 1
                        if rank > 11:
                            break
            
            if rank <= 2:
                print("⚠️  备用方案也未获取到有效数据")
                        
        except subprocess.TimeoutExpired:
            print("❌ 微博热搜获取超时（45 秒）")
        except Exception as e:
            print(f"❌ 备用方案失败：{e}")
    
    def get_bilibili(self):
        """获取 B 站热门（优化解析逻辑）"""
        print("\n### B 站热门")
        print("网站：http://www.bilibili.com/v/popular/rank/all\n")
        
        try:
            result = subprocess.run(
                ['curl', '-s', '-A', 'Mozilla/5.0', 'https://r.jina.ai/http://www.bilibili.com/v/popular/rank/all'],
                capture_output=True, text=True, timeout=30
            )
            
            lines = result.stdout.split('\n')
            videos = []
            
            # 解析 Markdown 格式：[标题](链接) 播放量
            for line in lines:
                # 匹配格式：[视频标题](http://www.bilibili.com/video/BVxxx) xxx 万播放
                if 'bilibili.com/video/' in line and line.strip().startswith('['):
                    # 提取标题
                    title_start = line.find('[') + 1
                    title_end = line.find('](')
                    if title_start > 0 and title_end > title_start:
                        title = line[title_start:title_end]
                        
                        # 提取链接
                        url_start = title_end + 2
                        url_end = line.find(')', url_start)
                        if url_end > url_start:
                            url = line[url_start:url_end]
                            
                            # 提取播放量（如果有）
                            views = ''
                            views_pos = line.find('播放', url_end)
                            if views_pos > 0:
                                views_start = line.rfind(' ', url_end, views_pos)
                                if views_start > 0:
                                    views = line[views_start:views_pos+2].strip()
                            
                            videos.append({
                                'title': title,
                                'url': url,
                                'views': views
                            })
            
            # 打印前 10 个视频
            for i, video in enumerate(videos[:10], 1):
                title = video['title']
                url = video['url']
                views = video['views']
                
                # 清理标题中的 Image 等无用信息
                if 'Image' in title:
                    continue
                
                print(f"{i}. {title}{views}")
                print(f"   {url}\n")
            
            if not videos:
                print("⚠️  未解析到视频，可能是格式变化")
                print("原始输出前 500 字符:")
                print(result.stdout[:500])
                        
        except subprocess.TimeoutExpired:
            print("❌ B 站热门获取超时（30 秒）")
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
        """获取 GitHub Trending（带代理支持）"""
        print("\n### GitHub Trending")
        print("网站：https://github.com/trending\n")
        
        # 检测并使用代理
        proxy = self._get_proxy_url()
        curl_cmd = ['curl', '-s', '-A', 'Mozilla/5.0']
        
        if proxy:
            curl_cmd.extend(['-x', proxy])
            print(f"🔑 使用代理：{proxy}\n")
        else:
            print("⚠️  未检测到代理，GitHub 可能访问失败\n")
        
        try:
            curl_cmd.append('https://r.jina.ai/https://github.com/trending')
            result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"❌ 请求失败：{result.stderr[:200] if result.stderr else '无响应'}")
                return
            
            # 解析 Markdown 格式
            lines = result.stdout.split('\n')
            repos = []
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                # 匹配格式：[组织/项目名](链接)
                if line.startswith('[') and '](' in line and 'github.com' in line:
                    title_end = line.find('](')
                    title = line[1:title_end]
                    
                    url_start = title_end + 2
                    url_end = line.find(')', url_start)
                    url = line[url_start:url_end] if url_end > url_start else ''
                    
                    # 查找描述和 star 数
                    desc = ''
                    stars = ''
                    if i + 1 < len(lines):
                        desc = lines[i + 1].strip()
                    if i + 2 < len(lines):
                        star_line = lines[i + 2]
                        if 'star' in star_line.lower():
                            # 提取 star 数
                            import re
                            star_match = re.search(r'[\d,]+', star_line)
                            if star_match:
                                stars = f" ⭐{star_match.group()}"
                    
                    if title and url:
                        repos.append({
                            'title': title,
                            'url': url,
                            'desc': desc,
                            'stars': stars
                        })
                    i += 3
                else:
                    i += 1
            
            # 打印前 10 个项目
            for i, repo in enumerate(repos[:10], 1):
                print(f"{i}. {repo['title']}{repo['stars']}")
                if repo['desc']:
                    print(f"   {repo['desc'][:80]}")
                print(f"   {repo['url']}\n")
            
            if not repos:
                print("⚠️  未解析到项目，可能是格式变化或需要代理")
                        
        except subprocess.TimeoutExpired:
            print("❌ GitHub Trending 获取超时（60 秒）")
        except Exception as e:
            print(f"❌ GitHub Trending 获取失败：{e}")
    
    def _get_proxy_url(self) -> str:
        """获取代理 URL"""
        import os
        
        # 检查环境变量
        proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
        if proxy:
            return proxy
        
        # 常用代理地址
        common_proxies = [
            'http://127.0.0.1:7890',  # Clash
            'http://127.0.0.1:10808',  # v2ray
            'http://127.0.0.1:8888',   # Charles
        ]
        
        # 快速测试哪个代理可用
        for p in common_proxies:
            try:
                result = subprocess.run(
                    ['curl', '-s', '-x', p, '--connect-timeout', '2', '-o', '/dev/null', 'https://www.google.com'],
                    capture_output=True, timeout=4
                )
                if result.returncode == 0:
                    return p
            except:
                pass
        
        return ''
    
    def get_zhihu(self):
        """获取知乎热榜（Jina Reader + 备用方案）"""
        print("\n### 知乎热榜")
        print("网站：https://www.zhihu.com/hot\n")
        
        try:
            result = subprocess.run(
                ['curl', '-s', '-A', 'Mozilla/5.0', 'https://r.jina.ai/http://www.zhihu.com/hot'],
                capture_output=True, text=True, timeout=45
            )
            
            if result.stdout.strip() and '热榜' in result.stdout:
                lines = result.stdout.split('\n')
                rank = 1
                for line in lines:
                    line = line.strip()
                    # 匹配知乎热榜条目
                    if line and len(line) > 5 and not line.startswith('http') and not line.startswith('Image'):
                        if line.startswith('['):
                            # 提取标题
                            title_end = line.find('](')
                            if title_end > 0:
                                line = line[1:title_end]
                        if line and len(line) > 3:
                            print(f"{rank}. {line}")
                            rank += 1
                            if rank > 11:
                                break
                if rank > 2:
                    return
        except Exception:
            pass
        
        # 备用方案：显示提示
        print("⚠️  知乎热榜暂时无法获取，可能是被限流")
        print("💡 建议直接访问：https://www.zhihu.com/hot\n")
    
    def get_douyin(self):
        """获取抖音热榜（Jina Reader + Tavily 备用方案）"""
        print("\n### 抖音热榜")
        print("网站：https://www.douyin.com/hot\n")
        
        # 方案 1：使用 Jina Reader 读取抖音热榜页面
        try:
            result = subprocess.run(
                ['curl', '-s', '-A', 'Mozilla/5.0', 'https://r.jina.ai/http://www.douyin.com/hot'],
                capture_output=True, text=True, timeout=45
            )
            
            if result.stdout.strip() and 'SecurityCompromiseError' not in result.stdout:
                lines = result.stdout.split('\n')
                rank = 1
                for line in lines:
                    line = line.strip()
                    # 匹配抖音热榜条目
                    if line and len(line) > 5 and not line.startswith('http') and not line.startswith('Image'):
                        if line.startswith('['):
                            # 提取标题
                            title_end = line.find('](')
                            if title_end > 0:
                                line = line[1:title_end]
                        if line and len(line) > 3:
                            print(f"{rank}. {line}")
                            rank += 1
                            if rank > 11:
                                break
                if rank > 2:
                    return
        except Exception as e:
            pass
        
        # 方案 2：使用 Tavily 搜索抖音热榜
        print("⚠️  Jina Reader 被限流，使用 Tavily 搜索...\n")
        
        try:
            result = subprocess.run(
                ['curl', '-s', '-X', 'POST', 'https://api.tavily.com/search',
                 '-H', 'Content-Type: application/json',
                 '-d', '{"api_key": "' + os.environ.get('TAVILY_API_KEY', '') + '", "query": "抖音热榜 2026", "search_depth": "basic", "max_results": 10}'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                results = data.get('results', [])
                if results:
                    for i, item in enumerate(results[:10], 1):
                        title = item.get('title', '无标题')
                        url = item.get('url', '')
                        print(f"{i}. {title}")
                        if url:
                            print(f"   {url}\n")
                    return
        except Exception:
            pass
        
        # 都失败：显示提示
        print("⚠️  抖音热榜暂时无法获取（可能因访问频繁被限流）")
        print("💡 建议直接访问：https://www.douyin.com/hot\n")
    
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
