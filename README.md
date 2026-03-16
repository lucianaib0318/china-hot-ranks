# 中国热榜聚合器 📊

> **一键获取全网热点，掌握流量密码**

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

---

## ✨ 特性

- 🎯 **7 大平台覆盖** - 微博、B 站、百度、CSDN、GitHub、知乎、抖音
- 🚀 **一键获取** - 单命令获取所有平台热榜
- 📝 **格式化输出** - 带链接、热度指数、播放量等详细信息
- 🔧 **灵活选择** - 支持获取全部或指定平台
- 🌐 **代理支持** - GitHub 等平台自动检测并使用代理
- 🔄 **备用方案** - 每个平台都有备用获取方式
- 📦 **开箱即用** - 无需 API Key，基于现有工具链

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/lucianaib0318/china-hot-ranks.git
cd china-hot-ranks
```

### 2. 检查依赖

```bash
# 检查 Python 版本（需要 3.6+）
python3 --version

# 检查 curl 是否安装
curl --version
```

### 3. 运行

```bash
# 获取所有热榜
python3 hot_ranks.py

# 获取指定平台
python3 hot_ranks.py weibo      # 微博热搜
python3 hot_ranks.py bilibili   # B 站热门
python3 hot_ranks.py baidu      # 百度热搜
python3 hot_ranks.py github     # GitHub Trending
```

---

## 📊 支持平台

| 平台 | 获取方式 | 数据内容 | 状态 |
|-----|---------|---------|------|
| **微博热搜** | 微博 MCP / Jina Reader | 热搜话题 + 热度指数 | ✅ 正常 |
| **B 站热门** | Jina Reader | 视频标题 + 播放量 | ✅ 正常 |
| **百度热搜** | Jina Reader | 热搜话题 + 热度标记 | ✅ 正常 |
| **CSDN 热榜** | Jina Reader | 技术文章 + 浏览量 | ✅ 正常 |
| **GitHub Trending** | Jina Reader + 代理 | 开源项目 + Star 数 | ✅ 需代理 |
| **知乎热榜** | Jina Reader | 热门问题 | ✅ 正常 |
| **抖音热榜** | Jina Reader / Tavily | 热门视频 + 热度值 | ⚠️ 可能限流 |

---

## 🔧 高级配置

### 配置 MCP 服务器（推荐）

MCP 服务器可以提供更准确、实时的数据。

#### 1. 安装 mcporter

```bash
# 使用 npm 安装
npm install -g mcporter

# 验证安装
mcporter --version
```

#### 2. 配置 MCP 服务器

```bash
# 创建配置目录
mkdir -p ~/.mcporter

# 复制项目配置（如果已安装微博/抖音 MCP）
cp /path/to/china-hot-ranks/config/mcporter.json ~/.mcporter/

# 或者手动创建配置
cat > ~/.mcporter/mcporter.json << 'EOF'
{
  "mcpServers": {
    "weibo": {
      "command": "mcp-server-weibo"
    },
    "douyin": {
      "baseUrl": "http://localhost:18070/mcp"
    }
  }
}
EOF
```

#### 3. 启动 MCP 服务器

```bash
# 查看已配置的服务器
mcporter list

# 应该显示：
# - weibo (10 tools)
# - douyin (5 tools)
```

#### 4. 验证微博 MCP

```bash
# 测试微博热搜 API
mcporter call "weibo.get_trendings(limit: 5)"

# 应该返回 JSON 格式的微博热搜数据
```

如果未配置 MCP 服务器，程序会自动使用备用方案（Jina Reader），但可能遇到限流。

### 配置 GitHub 代理（推荐）

GitHub 在中国大陆访问可能需要代理。

**方法 1：环境变量**
```bash
export HTTPS_PROXY=http://127.0.0.1:7890
python3 hot_ranks.py github
```

**方法 2：自动检测**
程序会自动检测常见代理端口：
- `7890` (Clash)
- `10808` (v2ray)
- `8888` (Charles)

---

## 📝 输出示例

### 微博热搜
```
### 微博热搜
网站：https://s.weibo.com/top/sum

1. 胖东来 169 元 1 克拉方糖戒指再上架 🔥77 万
   https://m.weibo.cn/search?...

2. 美宜佳被曝光后半小时无一人进店 🔥54 万
   https://m.weibo.cn/search?...
```

### B 站热门
```
### B 站热门
网站：http://www.bilibili.com/v/popular/rank/all

1. 当面一套，背后一套 - 小潮院长 175.5 万播放
   http://www.bilibili.com/video/BV1BbwFznEpm

2. 开拓者去欢愉打工然后丧失仅存的一丝梦想 166 万播放
   http://www.bilibili.com/video/BV1M5NFzrEKK
```

### GitHub Trending
```
### GitHub Trending
网站：https://github.com/trending

🔑 使用代理：http://127.0.0.1:7890

1. freeCodeCamp/freeCodeCamp ⭐380,000
   freeCodeCamp.org's open-source codebase and curriculum
   https://github.com/freeCodeCamp/freeCodeCamp
```

---

## 🛠️ 高级用法

### 导出为 Markdown

```bash
# 导出今日热榜
python3 hot_ranks.py > hot_ranks_$(date +%Y%m%d).md

# 导出指定平台
python3 hot_ranks.py weibo > weibo_$(date +%Y%m%d).md
```

### 定时获取（Cron Job）

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点获取热榜
0 9 * * * cd /path/to/china-hot-ranks && python3 hot_ranks.py >> hot_ranks.log 2>&1

# 每小时获取一次微博热搜
0 * * * * cd /path/to/china-hot-ranks && python3 hot_ranks.py weibo >> weibo.log 2>&1
```

### 集成到 Python 项目

```python
from hot_ranks import HotRanksAggregator

# 创建聚合器
aggregator = HotRanksAggregator()

# 获取微博热搜
weibo_data = aggregator.get_weibo()

# 获取 B 站热门
bilibili_data = aggregator.get_bilibili()

# 获取所有热榜
all_data = aggregator.get_all()
```

### 导出为 JSON

```python
import json
from hot_ranks import HotRanksAggregator

aggregator = HotRanksAggregator()

# 获取数据后导出
with open('hot_ranks.json', 'w', encoding='utf-8') as f:
    json.dump(aggregator.get_all(), f, ensure_ascii=False, indent=2)
```

---

## 🎯 使用场景

### 内容创作者
- 📈 追踪热点话题，创作爆款内容
- 🎯 了解平台趋势，优化选题方向
- ⏰ 定时监控，抓住最佳发布时间

### 市场营销
- 📊 监控品牌提及和舆情
- 🔥 发现热门话题，借势营销
- 📉 分析竞品动态

### 开发者
- 💻 关注技术趋势和开源项目
- 📚 学习热门技术栈
- 🔍 发现优质开源项目

### 研究人员
- 📈 分析社交媒体趋势
- 👥 研究用户行为和兴趣
- 📊 数据采集与分析

---

## ⚠️ 故障排查

### 微博热搜失败

**问题**: 显示"微博 MCP 不可用"

**解决方案**:
```bash
# 1. 检查微博 MCP 是否安装
which mcp-server-weibo

# 2. 查看 MCP 服务器列表
mcporter list

# 3. 如果未显示 weibo，需要安装
# 参考：https://github.com/modelcontextprotocol/servers

# 4. 使用备用方案（自动）
# 程序会自动切换到 Jina Reader 备用方案
```

### GitHub 无法访问

**问题**: 请求超时或无响应

**解决方案**:
```bash
# 方法 1：设置代理
export HTTPS_PROXY=http://127.0.0.1:7890
python3 hot_ranks.py github

# 方法 2：测试代理是否可用
curl -x http://127.0.0.1:7890 https://www.google.com

# 方法 3：检查常见代理端口
lsof -i :7890  # Clash
lsof -i :10808 # v2ray
lsof -i :8888  # Charles
```

### B 站解析失败

**问题**: 显示"未解析到视频"

**解决方案**:
```bash
# 1. 手动测试 Jina Reader
curl -s 'https://r.jina.ai/http://www.bilibili.com/v/popular/rank/all' | head -50

# 2. 检查网络连接
ping www.bilibili.com

# 3. 更新程序到最新版本
git pull origin main
```

### 抖音无法获取

**问题**: 显示"被限流"或"SecurityCompromiseError"

**原因**: 抖音反爬严格，Jina Reader 可能因访问频繁被临时限制

**解决方案**:
```bash
# 1. 等待一段时间后重试（通常 1-2 小时）

# 2. 使用 Tavily 备用方案（需要 API Key）
export TAVILY_API_KEY=your_api_key
python3 hot_ranks.py douyin

# 3. 直接访问官网
https://www.douyin.com/hot
```

**注意**: 抖音 MCP 服务器主要用于视频解析，不提供热榜功能。

### 知乎无法获取

**问题**: 显示"暂时无法获取"

**说明**: 知乎热榜由于反爬限制，可能偶尔无法获取

**解决方案**:
```bash
# 直接访问官网
https://www.zhihu.com/hot
```

---

## 📁 项目结构

```
china-hot-ranks/
├── hot_ranks.py              # 主程序（热榜聚合器）
├── SKILL.md                  # OpenClaw Skill 定义
├── README.md                 # 项目说明（本文件）
├── README_CN.md              # 中文文档
├── requirements.txt          # Python 依赖
├── examples/                 # 使用示例
│   └── output_sample.md      # 输出示例
├── docs/                     # 文档
│   └── api_reference.md      # API 参考
└── LICENSE                   # MIT 许可证
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 添加新平台

1. 在 `HotRanksAggregator` 类中添加新方法：
```python
def get_new_platform(self):
    """获取新平台热榜"""
    print("\n### 新平台热榜")
    print("网站：https://example.com\n")
    # 实现获取逻辑
```

2. 在 `__init__` 的 `self.sources` 中添加平台信息

3. 在 `main()` 函数中添加命令行支持

4. 更新本文档

### 提交流程

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [微博 MCP](https://github.com/modelcontextprotocol/servers) - 微博数据源
- [抖音 MCP](https://github.com/modelcontextprotocol/servers) - 抖音数据源
- [Jina AI](https://jina.ai/) - 网页读取服务
- [mcporter](https://github.com/modelcontextprotocol/mcporter) - MCP 运行时

---

## 📮 联系方式

- **GitHub**: [@lucianaib0318](https://github.com/lucianaib0318)
- **Issues**: [问题反馈](https://github.com/lucianaib0318/china-hot-ranks/issues)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by lucianaib0318

</div>
