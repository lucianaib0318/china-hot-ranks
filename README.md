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
- 📦 **开箱即用** - 无需 API Key，基于现有工具链

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/lucianaib0318/china-hot-ranks.git
cd china-hot-ranks

# 无需额外依赖（使用系统工具）
python3 hot_ranks.py --help
```

### 使用

```bash
# 获取所有热榜
python3 hot_ranks.py

# 获取指定平台
python3 hot_ranks.py weibo      # 微博热搜
python3 hot_ranks.py bilibili   # B 站热门
python3 hot_ranks.py github     # GitHub Trending
```

---

## 📊 支持平台

| 平台 | 获取方式 | 数据内容 | 状态 |
|-----|---------|---------|------|
| **微博热搜** | 微博 MCP | 热搜话题 + 热度指数 | ⚠️ 需启动 MCP 服务器 |
| **B 站热门** | Jina Reader | 视频标题 + 播放量 | ✅ 正常 |
| **百度热搜** | Jina Reader | 热搜话题 + 热度标记 | ✅ 正常 |
| **CSDN 热榜** | Jina Reader | 技术文章 + 浏览量 | ✅ 正常 |
| **GitHub Trending** | Jina Reader + 代理 | 开源项目 + Star 数 | ✅ 需代理 |
| **知乎热榜** | 备用方案 | 热门问题 | ⚠️ 模拟数据 |
| **抖音热榜** | 备用方案 | 热门视频 | ⚠️ 模拟数据 |

---

## 🔧 依赖要求

### 必需
- Python 3.6+
- curl
- mcporter (可选，用于微博热搜)

### 可选（增强功能）
- HTTP 代理（用于 GitHub）
- 微博 MCP 服务器 (`mcp-server-weibo`)

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

## 📁 项目结构

```
china-hot-ranks/
├── hot_ranks.py              # 主程序
├── SKILL.md                  # Skill 文档
├── README.md                 # 项目说明
├── requirements.txt          # Python 依赖
├── examples/
│   └── output_sample.md      # 输出示例
├── docs/
│   └── api_reference.md      # API 参考
└── LICENSE                   # MIT 许可证
```

---

## 🛠️ 高级用法

### 导出为 Markdown

```bash
python3 hot_ranks.py > hot_ranks_$(date +%Y%m%d).md
```

### 定时获取（Cron Job）

```bash
# 每天早上 9 点获取热榜
0 9 * * * cd /path/to/china-hot-ranks && python3 hot_ranks.py >> hot_ranks.log
```

### 集成到工作流

```python
from hot_ranks import HotRanksAggregator

aggregator = HotRanksAggregator()

# 获取微博热搜
weibo_data = aggregator.get_weibo()

# 获取所有热榜
all_data = aggregator.get_all()
```

---

## 🎯 使用场景

### 内容创作者
- 追踪热点话题，创作爆款内容
- 了解平台趋势，优化选题方向

### 市场营销
- 监控品牌提及和舆情
- 发现热门话题，借势营销

### 开发者
- 关注技术趋势和开源项目
- 学习热门技术栈

### 研究人员
- 分析社交媒体趋势
- 研究用户行为和兴趣

---

## ⚠️ 注意事项

1. **微博 MCP**
   - 需要安装并启动 `mcp-server-weibo`
   - 配置在 `/root/.openclaw/workspace/config/mcporter.json`

2. **GitHub 代理**
   - 自动检测常见代理端口（7890、10808、8888）
   - 可设置环境变量 `HTTPS_PROXY`

3. **数据时效性**
   - 微博/B 站/抖音：实时更新
   - CSDN/知乎：小时级更新
   - GitHub：日级更新

4. **网络要求**
   - 需要访问国内平台（微博、B 站等）
   - GitHub 需要代理

---

## 🔧 故障排查

### 微博热搜失败
```bash
# 检查微博 MCP 服务器
mcporter list

# 应该显示 weibo (10 tools)
```

### GitHub 无法访问
```bash
# 设置代理
export HTTPS_PROXY=http://127.0.0.1:7890

# 或检查代理是否可用
curl -x http://127.0.0.1:7890 https://www.google.com
```

### B 站解析失败
- 可能是 Jina Reader 格式变化
- 检查原始输出：`curl https://r.jina.ai/http://www.bilibili.com/v/popular/rank/all`

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 🙏 致谢

- [微博 MCP](https://github.com/modelcontextprotocol/servers) - 微博数据源
- [Jina AI](https://jina.ai/) - 网页读取服务
- [mcporter](https://github.com/modelcontextprotocol/mcporter) - MCP 运行时

---

**Made with ❤️ by lucianaib0318**
