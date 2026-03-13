# API 参考文档

## HotRanksAggregator 类

### 初始化

```python
aggregator = HotRanksAggregator()
```

### 方法

#### get_all()
获取所有平台热榜

```python
aggregator.get_all()
```

#### get_weibo()
获取微博热搜

```python
aggregator.get_weibo()
```

**返回**: 微博热搜 TOP10，包含标题、链接、热度指数

#### get_bilibili()
获取 B 站热门

```python
aggregator.get_bilibili()
```

**返回**: B 站热门视频 TOP10，包含标题、链接、播放量

#### get_baidu()
获取百度热搜

```python
aggregator.get_baidu()
```

**返回**: 百度热搜 TOP10，包含标题、链接、热度标记

#### get_csdn()
获取 CSDN 热榜

```python
aggregator.get_csdn()
```

**返回**: CSDN 热榜文章 TOP10，包含标题、链接、浏览量

#### get_github()
获取 GitHub Trending

```python
aggregator.get_github()
```

**返回**: GitHub Trending 仓库 TOP10，包含名称、Star 数、描述、链接

#### get_zhihu()
获取知乎热榜

```python
aggregator.get_zhihu()
```

**返回**: 知乎热榜 TOP10，包含问题标题、链接

#### get_douyin()
获取抖音热榜

```python
aggregator.get_douyin()
```

**返回**: 抖音热榜 TOP10，包含视频标题、链接

---

## 命令行参数

```bash
python3 hot_ranks.py [platform]
```

**参数**:
- `all` - 获取所有平台（默认）
- `weibo` - 微博热搜
- `bilibili` - B 站热门
- `baidu` - 百度热搜
- `csdn` - CSDN 热榜
- `github` - GitHub Trending
- `zhihu` - 知乎热榜
- `douyin` - 抖音热榜

**示例**:
```bash
python3 hot_ranks.py weibo
python3 hot_ranks.py github
python3 hot_ranks.py all
```

---

## 错误处理

所有方法都包含错误处理，获取失败时会输出错误信息但不会中断程序。

```python
try:
    aggregator.get_weibo()
except Exception as e:
    print(f"❌ 微博热搜获取失败：{e}")
```

---

## 性能优化建议

1. **批量获取**: 使用 `get_all()` 一次性获取所有平台
2. **缓存结果**: 将结果保存到文件，避免重复请求
3. **定时任务**: 使用 Cron Job 定时获取，避免频繁调用

---

## 更新日志

### v1.0.0 (2026-03-13)
- ✨ 初始版本发布
- 📊 支持 7 大平台热榜获取
- 📝 格式化输出
- 🔧 灵活的命令行参数
