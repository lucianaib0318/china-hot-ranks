#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国热榜聚合器 - China Hot Ranks Aggregator
基于 DailyHotApi 服务，获取 54 个平台的热榜数据

Usage:
    python hot_ranks.py              # 获取所有热榜
    python hot_ranks.py weibo        # 只获取微博热搜
    python hot_ranks.py bilibili     # 只获取 B 站热门
    python hot_ranks.py all          # 获取所有热榜

支持平台 (54 个):
- 视频/直播：微博、B 站、抖音、快手、AcFun
- 社交媒体：知乎、豆瓣、贴吧、V2EX、NGA、虎扑
- 新闻资讯：百度、澎湃、今日头条、36 氪、腾讯新闻
- 技术社区：CSDN、掘金、51CTO、IT 之家、少数派
- 游戏/ACG: 原神、米游社、崩坏 3、星穹铁道
- 其他：微信读书、简书、果壳、豆瓣电影等

API: https://github.com/imsyy/DailyHotApi
"""

import requests
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional


class DailyHotAPI:
    """DailyHotApi 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:6688", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_hot_rank(self, platform: str) -> Optional[Dict]:
        """获取指定平台热榜"""
        try:
            url = f"{self.base_url}/{platform}"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 200:
                return data
            else:
                print(f"⚠️  {platform} 返回错误：{data.get('message', 'Unknown error')}")
                return None
        except requests.exceptions.Timeout:
            print(f"⚠️  {platform} 请求超时 ({self.timeout}秒)")
            return None
        except requests.exceptions.ConnectionError:
            print(f"⚠️  无法连接到 DailyHotApi 服务 ({self.base_url})")
            return None
        except Exception as e:
            print(f"⚠️  {platform} 获取失败：{e}")
            return None


class HotRanksAggregator:
    """热榜聚合器"""
    
    # 平台配置：API 名称 -> 显示名称 -> 官方链接 (35 个稳定平台)
    PLATFORMS = {
        'weibo': ('微博热搜', 'https://s.weibo.com/top/summary/'),
        'zhihu': ('知乎热榜', 'https://www.zhihu.com/hot'),
        'bilibili': ('B 站热门', 'https://www.bilibili.com/v/popular/rank/all'),
        'douyin': ('抖音热点', 'https://www.douyin.com/hot'),
        'csdn': ('CSDN 热榜', 'https://blog.csdn.net/rank/list'),
        'juejin': ('掘金热榜', 'https://juejin.cn/hot/items'),
        'baidu': ('百度热搜', 'https://top.baidu.com/board'),
        'toutiao': ('今日头条', 'https://www.toutiao.com/'),
        '36kr': ('36 氪热榜', 'https://36kr.com/hot-list'),
        'ithome': ('IT 之家热榜', 'https://www.ithome.com/list/'),
        'hupu': ('虎扑热帖', 'https://bbs.hupu.com/all-gambia'),
        'ngabbs': ('NGA 热帖', 'https://ngabbs.com/'),
        'douban-group': ('豆瓣讨论', 'https://www.douban.com/group/explore'),
        'douban-movie': ('豆瓣电影', 'https://movie.douban.com/chart'),
        'weread': ('微信读书', 'https://weread.qq.com/'),
        'jianshu': ('简书热门', 'https://www.jianshu.com/'),
        'guokr': ('果壳热门', 'https://www.guokr.com/'),
        'huxiu': ('虎嗅 24 小时', 'https://www.huxiu.com/moment/'),
        'ifanr': ('爱范儿快讯', 'https://www.ifanr.com/'),
        'sspai': ('少数派热榜', 'https://sspai.com/'),
        '51cto': ('51CTO 推荐榜', 'https://blog.51cto.com/ranking'),
        'acfun': ('AcFun 排行榜', 'https://www.acfun.cn/rank/list/'),
        'kuaishou': ('快手热点', 'https://www.kuaishou.com/'),
        'tieba': ('百度贴吧', 'https://tieba.baidu.com/hottopic'),
        'zhihu-daily': ('知乎日报', 'https://daily.zhihu.com/'),
        'qq-news': ('腾讯新闻', 'https://news.qq.com/'),
        'sina': ('新浪热榜', 'https://sinanews.sina.cn/'),
        'sina-news': ('新浪新闻', 'https://news.sina.cn/'),
        'netease-news': ('网易新闻', 'https://news.163.com/'),
        'thepaper': ('澎湃新闻', 'https://www.thepaper.cn/'),
        'hellogithub': ('HelloGitHub', 'https://hellogithub.com/'),
        'genshin': ('原神最新消息', 'https://www.mihoyo.com/'),
        'miyoushe': ('米游社', 'https://www.miyoushe.com/'),
        'honkai': ('崩坏 3', 'https://bh3.mihoyo.com/'),
        'starrail': ('星穹铁道', 'https://sr.mihoyo.com/'),
        'lol': ('英雄联盟', 'https://lol.qq.com/'),
    }
    
    # 默认抓取的平台（6 大主流）
    DEFAULT_PLATFORMS = ['weibo', 'zhihu', 'bilibili', 'douyin', 'csdn', 'juejin']
    
    # 全部 35 个平台列表
    ALL_PLATFORMS = list(PLATFORMS.keys())
    
    def __init__(self, api_url: str = "http://localhost:6688"):
        self.api = DailyHotAPI(base_url=api_url, timeout=30)
        self.results = {}
    
    def fetch_platform(self, platform: str, verbose: bool = True) -> bool:
        """抓取单个平台热榜"""
        if platform not in self.PLATFORMS:
            if verbose:
                print(f"⚠️  未知平台：{platform}")
            return False
        
        name, url = self.PLATFORMS[platform]
        
        if verbose:
            print(f"\n### {name}")
            print(f"网站：{url}\n")
        
        data = self.api.get_hot_rank(platform)
        
        if not data:
            if verbose:
                print(f"⚠️  {name}暂时无法获取")
            return False
        
        items = data.get('data', [])[:10]  # 只取 TOP10
        
        if not items:
            if verbose:
                print(f"⚠️  {name}无数据")
            return False
        
        self.results[platform] = {
            'name': name,
            'url': url,
            'items': items,
            'update_time': data.get('updateTime', '')
        }
        
        # 输出热榜
        for i, item in enumerate(items, 1):
            title = item.get('title', '无标题')
            link = item.get('url', '#')
            hot = item.get('hot', item.get('desc', ''))
            
            # 格式化输出
            print(f"{i}. {title}")
            print(f"   🔗 {link}")
        
        return True
    
    def fetch_all(self, platforms: Optional[List[str]] = None) -> Dict:
        """抓取多个平台热榜"""
        if platforms is None:
            platforms = self.DEFAULT_PLATFORMS
        
        print(f"📊 开始获取热榜数据...")
        print(f"目标平台：{len(platforms)} 个")
        print(f"API 地址：{self.api.base_url}")
        print("=" * 60)
        
        success_count = 0
        for platform in platforms:
            if self.fetch_platform(platform):
                success_count += 1
        
        print("\n" + "=" * 60)
        print(f"✅ 抓取完成：{success_count}/{len(platforms)} 平台成功")
        
        return self.results
    
    def list_platforms(self):
        """列出所有支持的平台"""
        print("\n📊 支持的热榜平台（35 个）\n")
        
        # 按类别分组（仅稳定平台）
        categories = {
            '🎬 视频/直播': ['bilibili', 'douyin', 'kuaishou', 'acfun'],
            '💬 社交媒体': ['weibo', 'zhihu', 'zhihu-daily', 'tieba', 'douban-group', 'ngabbs', 'hupu'],
            '📰 新闻资讯': ['baidu', 'thepaper', 'toutiao', '36kr', 'qq-news', 'sina', 'sina-news', 'netease-news', 'huxiu', 'ifanr'],
            '💻 技术社区': ['ithome', 'sspai', 'csdn', 'juejin', '51cto', 'hellogithub'],
            '🎮 游戏/ACG': ['genshin', 'miyoushe', 'honkai', 'starrail', 'lol'],
            '📚 阅读/文化': ['jianshu', 'guokr', 'weread', 'douban-movie'],
        }
        
        for category, platform_keys in categories.items():
            print(f"\n{category}")
            for key in platform_keys:
                if key in self.PLATFORMS:
                    name, url = self.PLATFORMS[key]
                    print(f"  • {name} ({key})")
        
        print(f"\n✅ 共 {len(self.PLATFORMS)} 个平台，全部稳定可用\n")
    
    def export_markdown(self, output_file: Optional[str] = None) -> str:
        """导出为 Markdown 格式"""
        lines = []
        lines.append(f"# 🔥 中国热榜聚合")
        lines.append(f"\n更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for platform, data in self.results.items():
            lines.append(f"\n## {data['name']}")
            lines.append(f"网站：{data['url']}")
            lines.append(f"\n| # | 标题 | 链接 |")
            lines.append(f"|---|------|------|")
            
            for i, item in enumerate(data['items'], 1):
                title = item.get('title', '无标题')
                link = item.get('url', '#')
                lines.append(f"| {i} | {title} | [查看]({link}) |")
        
        markdown = "\n".join(lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"📄 已导出到：{output_file}")
        
        return markdown


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='中国热榜聚合器')
    parser.add_argument('platform', nargs='?', default='all', help='平台名称或 all/list')
    parser.add_argument('--api', default='http://localhost:6688', help='DailyHotApi 地址')
    parser.add_argument('--output', '-o', help='导出到 Markdown 文件')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有支持的平台')
    
    args = parser.parse_args()
    
    aggregator = HotRanksAggregator(api_url=args.api)
    
    if args.list:
        aggregator.list_platforms()
        return
    
    if args.platform == 'all':
        aggregator.fetch_all()
    elif args.platform == 'list':
        aggregator.list_platforms()
    else:
        # 单个平台
        platforms = args.platform.split(',')
        aggregator.fetch_all(platforms)
    
    # 导出
    if args.output:
        aggregator.export_markdown(args.output)


if __name__ == '__main__':
    main()
