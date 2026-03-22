# 🔥 中国热榜聚合器 - China Hot Ranks Aggregator

基于 [DailyHotApi](https://github.com/imsyy/DailyHotApi) 的热榜聚合工具，支持 **35 个平台** 的热榜抓取。

---

## 🎯 特性

- ✅ **35 个平台**：微博、知乎、B 站、抖音、CSDN、掘金等
- ✅ **稳定可靠**：本地服务调用，无网络限流问题
- ✅ **快速高效**：单次抓取 <10 秒
- ✅ **易于扩展**：新增平台只需一行配置
- ✅ **多种输出**：终端显示、Markdown 导出

---

## 🚀 快速开始

### 1. 部署 DailyHotApi 服务

```bash
# 克隆 DailyHotApi
cd /tmp
git clone https://github.com/imsyy/DailyHotApi.git
cd DailyHotApi

# 安装依赖并启动
npm install
npm run build
pm2 start ecosystem.config.cjs

# 验证服务
curl http://localhost:6688/weibo
```

### 2. 使用热榜聚合器

```bash
# 克隆项目
git clone https://github.com/lucianaib0318/china-hot-ranks.git
cd china-hot-ranks

# 安装依赖
pip install requests

# 获取所有默认平台热榜（6 大主流）
python3 hot_ranks.py

# 获取单个平台
python3 hot_ranks.py weibo
python3 hot_ranks.py zhihu
python3 hot_ranks.py bilibili

# 获取多个平台
python3 hot_ranks.py weibo,zhihu,bilibili

# 列出所有支持的平台
python3 hot_ranks.py --list

# 导出 Markdown
python3 hot_ranks.py --output hot-ranks.md
```

---

## 📊 支持平台

### 默认平台（6 个）
| 平台 | API 名称 | 官方链接 |
|------|---------|---------|
| 微博热搜 | `weibo` | https://s.weibo.com/top/summary/ |
| 知乎热榜 | `zhihu` | https://www.zhihu.com/hot |
| B 站热门 | `bilibili` | https://www.bilibili.com/v/popular/rank/all |
| 抖音热点 | `douyin` | https://www.douyin.com/hot |
| CSDN 热榜 | `csdn` | https://blog.csdn.net/rank/list |
| 掘金热榜 | `juejin` | https://juejin.cn/hot/items |

### 全部平台（35 个）

**🎬 视频/直播 (4)**
- bilibili, douyin, kuaishou, acfun

**💬 社交媒体 (7)**
- weibo, zhihu, zhihu-daily, tieba, douban-group, hupu, ngabbs

**📰 新闻资讯 (10)**
- baidu, thepaper, toutiao, 36kr, qq-news, sina, sina-news, netease-news, huxiu, ifanr

**💻 技术社区 (6)**
- ithome, sspai, csdn, juejin, 51cto, hellogithub

**🎮 游戏/ACG (5)**
- genshin, miyoushe, honkai, starrail, lol

**📚 阅读/文化 (4)**
- jianshu, guokr, weread, douban-movie

---

## 📖 使用示例

### 示例 1：获取微博热搜 TOP10

```bash
python3 hot_ranks.py weibo
```

输出：
```
### 微博热搜
网站：https://s.weibo.com/top/summary/

1. 月鳞绮纪
   🔗 https://s.weibo.com/weibo?q=月鳞绮纪
2. 爱吃荔枝的人今年天塌了
   🔗 https://s.weibo.com/weibo?q=爱吃荔枝的人今年天塌了
...
```

### 示例 2：获取 6 大平台热榜

```bash
python3 hot_ranks.py all
```

### 示例 3：导出 Markdown 报告

```bash
python3 hot_ranks.py --output 2026-03-22.md
```

### 示例 4：在 Python 脚本中使用

```python
from hot_ranks import HotRanksAggregator

aggregator = HotRanksAggregator()
results = aggregator.fetch_all(['weibo', 'zhihu', 'bilibili'])

for platform, data in results.items():
    print(f"\n{data['name']}")
    for item in data['items'][:5]:
        print(f"  {item['title']}")
```

---

## 🔧 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DAILY_HOT_API_URL` | `http://localhost:6688` | DailyHotApi 服务地址 |
| `DAILY_HOT_TIMEOUT` | `30` | 请求超时时间（秒） |

### 自定义 API 地址

```bash
# 远程服务器
python3 hot_ranks.py --api http://192.168.1.100:6688

# Docker 容器
python3 hot_ranks.py --api http://host.docker.internal:6688
```

---

## 🏗️ 架构

```
用户请求 → hot_ranks.py → DailyHotApi (localhost:6688) → 35 个热榜源
```

### 组件说明

| 组件 | 职责 |
|------|------|
| **hot_ranks.py** | 热榜聚合器客户端 |
| **DailyHotApi** | 独立服务，抓取/聚合热榜数据 |
| **PM2** | 进程管理，确保服务稳定运行 |

---

## 📦 依赖

- Python 3.7+
- requests
- DailyHotApi 服务

安装依赖：
```bash
pip install requests
```

---

## 🎯 定时任务

### Cron 配置（每天早上 9 点推送）

```bash
# 编辑 crontab
crontab -e

# 添加任务
0 9 * * * cd /path/to/china-hot-ranks && python3 hot_ranks.py >> /var/log/hot-ranks.log 2>&1
```

### OpenClaw Cron

已在 `/root/.openclaw/workspace/heartbeat-workspace/morning-hot-ranks/morning-hot-ranks.sh` 配置

---

## 📝 更新日志

**v2.0.0** (2026-03-22)
- ✨ 重构：改用 DailyHotApi 服务，支持 35 个平台
- ✨ 新增：知乎、B 站、抖音、掘金等平台
- ✨ 优化：抓取速度从 180 秒降至 10 秒
- ✨ 修复：网络限流导致的失败问题
- 🐛 移除：旧版 MCP/Jina Reader 抓取方案

**v1.0.0** (2026-03-17)
- 初始版本
- 支持微博、B 站、百度、CSDN、GitHub、知乎、抖音

---

## 🤝 致谢

- [DailyHotApi](https://github.com/imsyy/DailyHotApi) - 提供热榜源 API
- [OpenClaw](https://github.com/openclaw/openclaw) - AI 助手平台

---

## 📄 许可证

MIT License

---

## 📞 问题反馈

如有问题或建议，欢迎提 Issue 或 PR！
