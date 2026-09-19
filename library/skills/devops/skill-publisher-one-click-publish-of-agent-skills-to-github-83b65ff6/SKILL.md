---
name: "skill-publisher"
description: "一键发布 agent skill 到 GitHub，自动验证 SKILL.md、检查或生成 README、创建或更新仓库，并通过 `npx skills` 进行真实安装验证。适用于 `~/.agents/skills/` 目录下的 skill。"
---

# Skill Publisher

一键将 agent skill 发布到 GitHub，自动完成验证、README 质量检查、补全、推送和真实安装验证。

## 前置条件

- 已安装并登录 `gh` CLI（`gh auth status`）
- Skill 目录中包含有效的 `SKILL.md`（必须有 `name` 与 `description`）
- 推荐使用 `~/.agents/skills/<name>` 作为本地源目录；`.codex` / `.claude` 可作兼容入口

## 使用方式

```bash
python3 ~/.agents/skills/qiaomu-skill-publisher/scripts/publish_skill.py <skill_dir> [options]
```

### 参数选项

| 参数 | 说明 |
|------|------|
| `--private` | 创建私有仓库（默认公开） |
| `--dry-run` | 仅检查，不实际发布 |
| `--skip-verify` | 跳过 `npx skills` 验证 |
| `--github-user USER` | 指定 GitHub 用户名（默认自动获取） |
| `--repo-name NAME` | 指定仓库名；默认使用当前 `origin` 或 skill name |
| `--no-symlink` | 跳过同步到 `~/.agents/skills/` 实体目录 |

### 自动化步骤

1. **验证** `SKILL.md` 的 YAML front‑matter（`name` + `description`）
2. **检查** `gh` CLI 状态
3. **创建** `LICENSE`（MIT，若缺失）
4. **生成或检查** `README.md`（禁止出现占位符）
5. **识别仓库名**：优先使用当前 `origin`，防止误发到错误仓库
6. **初始化** Git（如有必要）
7. **创建或更新** GitHub 公共仓库并推送代码
8. **验证** `npx skills add --list` 能发现并在临时目录完成真实安装

## 示例

```bash
# 发布指定 skill
python3 ~/.agents/skills/qiaomu-skill-publisher/scripts/publish_skill.py ~/.agents/skills/yt-search-download

# 在当前目录发布
python3 ~/.agents/skills/qiaomu-skill-publisher/scripts/publish_skill.py .

# 仅检查，不实际发布
python3 ~/.agents/skills/qiaomu-skill-publisher/scripts/publish_skill.py <dir> --dry-run
```

## README 质量检查（发布前必做）

脚本在 `README.md` 不存在时会生成一个基础模板；若已存在，则会拦截明显的占位内容（如 `TODO`、`[问题 1]` 等）。发布前请确保 README 包含以下要素：

1. **价值主张** – 首段明确解决的用户痛点
2. **首屏证据** – 截图、示例输出或 Demo
3. **动态徽章** – stars、forks、issues、last commit、license 等
4. **前置条件** – 使用 Markdown 勾选框列出所有依赖及安装方式
5. **完整安装步骤** – 编号步骤并提供验证命令
6. **自然语言使用示例** – 展示用户会说的触发句子
7. **致谢** – 如基于第三方库，请注明原作者
8. **风险/限制说明** – 费用、账号、操作风险等
9. **常见问题 / Troubleshooting** – 至少 3 条常见报错及解决方案

## 发布完成后

脚本会输出：
- GitHub 仓库 URL
- 安装命令 `npx skills add <user>/<repo>`
- 验证结果（是否成功在临时目录完成安装）

---
