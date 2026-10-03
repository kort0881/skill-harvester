---
name: "china-hot-ranks"
description: "中国热榜聚合器 - 一键获取微博、B 站、百度、CSDN、GitHub、知乎、抖音等 7 大平台的热门内容，支持全量获取和单平台查询，输出格式化热榜数据。"
---

# 中国热榜聚合器 📊

> **一键获取全网热点，掌握流量密码**

支持 7 大主流平台的热门内容获取：微博、B 站、百度、CSDN、GitHub、知乎、抖音。

## ✨ 特性

- 🎯 **7 大平台覆盖** – 社交媒体、视频、搜索、技术社区全覆盖
- 🚀 **一键获取** – 单命令获取所有平台热榜
- 📝 **格式化输出** – 带链接、热度指数、播放量等详细信息
- 🔧 **灵活选择** – 支持获取全部或指定平台
- 📦 **开箱即用** – 无需 API Key，基于现有工具链（可选 Tavily / GitHub Token）

## 🚀 快速开始

### 方式一：直接运行脚本

```bash
# 获取所有热榜
python3 hot_ranks.py

# 获取指定平台
python3 hot_ranks.py weibo      # 微博热搜
python3 hot_ranks.py bilibili   # B 站热门
python3 hot_ranks.py github     # GitHub Trending
```

### 方式二：使用 Skill 命令（mcporter）

```bash
# 通过 mcporter 调用全部热榜
mcporter call 'hot_ranks.get_all()'

# 获取单个平台
mcporter call 'hot_ranks.get_weibo()'
mcporter call 'hot_ranks.get_bilibili()'
```

## 📊 支持平台

| 平台 | 获取方式 | 数据内容 | 更新频率 |
|------|----------|----------|----------|
| 微博热搜 | mcporter (weibo MCP) | 热搜话题 + 热度指数 | 实时 |
| B 站热门 | Jina Reader | 视频标题 + 播放量 | 实时 |
| 百度热搜 | Jina Reader | 热搜话题 + 热度标记 | 实时 |
| CSDN 热榜 | Jina Reader | 技术文章 + 浏览量 | 小时级 |
| GitHub Trending | GitHub MCP API | 开源项目 + Star 数 | 日级 |
| 知乎热榜 | Tavily 搜索 | 热门问题 | 小时级 |
| 抖音热榜 | Tavily 搜索 | 热门视频 | 实时 |

## 📝 输出示例

### 微博热搜
```
1. 习近平总书记的 2026 全国两会日历
   https://m.weibo.cn/search?...
2. 微信 朋友圈编辑 🔥113 万
   https://m.weibo.cn/search?...
3. 国产手机涨价 2000 元 🔥84 万
   https://m.weibo.cn/search?...
```

### B 站热门
```
1. 当面一套，背后一套 - 小潮院长 175.5 万播放
   http://www.bilibili.com/video/BV1BbwFznEpm
2. 开拓者去欢愉打工然后丧失仅存的一丝梦想 - 觅 2 166 万播放
   http://www.bilibili.com/video/BV1M5NFzrEKK
```

### GitHub Trending
```
1. freeCodeCamp/freeCodeCamp ⭐380,000
   freeCodeCamp.org's open-source codebase and curriculum
   https://github.com/freeCodeCamp/freeCodeCamp
2. EbookFoundation/free-programming-books ⭐350,000
   Freely available programming books
   https://github.com/EbookFoundation/free-programming-books
```

## 🔧 依赖要求

**必需**
- Python 3.6+
- curl
- mcporter

**可选（增强功能）**
- Tavily API Key（用于知乎/抖音热榜）
- GitHub Token（用于 GitHub Trending）

## 📁 项目结构
```
china-hot-ranks/
├── hot_ranks.py              # 主程序
├── SKILL.md                  # 本文档
├── README.md                 # 项目说明
├── requirements.txt          # Python 依赖
├── examples/
│   └── output_sample.md      # 输出示例
├── docs/
│   └── api_reference.md      # API 参考
└── LICENSE                   # MIT 许可证
```

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

### 在 Python 项目中集成
```python
from hot_ranks import HotRanksAggregator

aggregator = HotRanksAggregator()

# 获取微博热搜
weibo_data = aggregator.get_weibo()

# 获取所有热榜
all_data = aggregator.get_all()
```

## 🎯 使用场景

- **内容创作者**：追踪热点话题，快速选题。
- **市场营销**：监控品牌舆情，发现流行趋势。
- **开发者**：关注技术趋势和开源项目。
- **研究人员**：分析社交媒体行为和兴趣分布。

## ⚠️ 注意事项

1. **API 限制**
   - 微博热搜依赖 weibo MCP 服务。
   - GitHub 需要有效 Token。
   - 知乎/抖音通过 Tavily 搜索，受调用配额限制。
2. **数据时效性**：不同平台更新频率不同，请根据需求选择。
3. **网络要求**：需要能够访问国内平台，GitHub 可能需要代理。

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起 Pull Request

## 📄 许可证

MIT 许可证 – 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [weibo-mcp](https://github.com/ModelContextProtocol/servers) – 微博 MCP 服务
- [Jina AI](https://jina.ai/) – 网页读取服务
- [GitHub MCP](https://github.com/modelcontextprotocol/servers) – GitHub MCP 服务
- [Tavily](https://tavily.com/) – 搜索服务

**Made with ❤️ by lucianaib0318**
