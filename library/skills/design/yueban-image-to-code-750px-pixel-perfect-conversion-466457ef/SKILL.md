---
name: "yueban-image-to-code"
description: "像素级 750px 图片转代码与切图工作流。将 UI 截图、设计稿或 Figma 导出图精准等比缩放至 750px 宽度，生成对应的代码、透明 PNG 切图以及 layers.manifest.json，确保 1:1 视觉还原。"
---

# Yueban Image To Code

## 目标
把用户提供或当前选中的 UI 图片还原为代码，并导出必要的独立切图资源。原图即视觉合同，禁止任何自动排版优化或主观调整。

## 最高优先级规则
- 画板宽度必须 **精确 750 px**，高度按等比计算。
- 所有元素使用同一全局缩放比例，保持相对位置、大小、层级、颜色、透明度等属性。
- 禁止自动布局、合并元素、替换图标或使用相似素材。
- 仅在需要切图时导出独立 PNG，切图必须基于 manifest 中的 bbox。

## 跨目录调用一致性
每次调用都必须重新读取、测量并生成当前源图的层级表和 manifest，不能复用旧项目的素材或布局参数。

## 执行流程
1. **检查输入**：确认图片尺寸、目标平台、技术栈、输出需求（代码、切图或两者）。
2. **750 px 等比归一化**：`scale = 750 / source_width`，将所有坐标、尺寸、圆角、阴影等乘以同一 `scale`。
3. **生成 `layers.manifest.json`**：记录每个图层的原始 bbox、缩放后 bbox、类型、z‑index、导出文件名等。
4. **依据 manifest 导出 PNG**：使用 `scripts/extract_png_asset.py`（或等效工具）按 bbox 导出透明 PNG。
5. **在 750 px 画板中实现代码**：使用绝对定位或 CSS 变量，严格按照 manifest 坐标绘制。
6. **分模块校验**：分别检查矢量、文本、位图切图的准确性。
7. **整页叠图复核**：将生成的页面截图与归一化原图叠加对比。
8. **迭代修正**：根据差异继续调整 manifest、切图或代码。
9. **交付**：代码、切图资源、`layers.manifest.json` 与简短还原报告。

## 输入检查
- 原图尺寸与宽高比
- 目标类型（网页、移动端、组件、海报等）
- 项目框架/技术栈
- 输出需求（代码、切图或两者）
- 必须可编辑的文字
- 需要保留为 PNG 的复杂图形

## 750 px 等比归一化公式
```text
scale = 750 / source_width
final_width = 750
final_height = round(source_height * scale)
scaled_x = original_x * scale
scaled_y = original_y * scale
scaled_width = original_width * scale
scaled_height = original_height * scale
```
同一 `scale` 适用于坐标、尺寸、圆角、描边、阴影、渐变、文字字号等所有属性。

## 强制 Manifest 示例
```json
{
  "id": "card-wallet-illustration",
  "type": "bitmap",
  "source_bbox": { "x": 338, "y": 520, "width": 116, "height": 122 },
  "scaled_bbox": { "x": 338, "y": 520, "width": 116, "height": 122 },
  "z_index": 24,
  "asset": "assets/illustrations/card-wallet-illustration.png",
  "transparent_required": true,
  "notes": "从当前源图裁切，保持原图露出比例"
}
```
- `source_bbox` 必须直接测量得到。
- `scaled_bbox` 必须由同一 `scale` 计算。
- 每个代码层必须能追溯到 manifest 条目。

## Bbox 测量与预览
1. 在原图尺寸上测量 `source_bbox`（不要在浏览器缩放后估算）。
2. 使用 `scripts/preview_bboxes.py` 将 manifest 中的 bbox 绘制在源图上生成预览。
3. 仅当预览框完全覆盖目标元素且不包含相邻内容时才进行切图。
4. 如有不确定，生成 2‑3 个候选 bbox 并选取最安全的。

## 图层分类规则
- **文本层**：完整还原为可编辑文本，保留字体、字号、字重、行高、颜色、透明度、对齐等。
- **简单矢量/规则图形**：矩形、圆形、线条、按钮背景等转为 CSS 或原生 SVG。
- **位图/图标**：所有图标、头像、插画、复杂位图必须从源图裁切为独立透明 PNG，禁止使用相似图标库或 CSS 绘制替代。
- **复杂图表/可视化**：整体保留为 PNG，文字部分单独提取为文本层。

## 代码实现要点
- 在 750 px 画板中使用 **绝对定位** 或 **CSS 变量** 实现像素级定位。
- 禁止使用自动布局（flex/grid）除非坐标完全匹配 manifest。
- 代码结构保持与原图层级一致，避免额外的容器或装饰层。
- 响应式适配是第二阶段任务，不能影响 750 px 定稿。

## 验收与复核
1. 启动本地服务器，截取 750 px 画板截图。
2. 与归一化原图进行叠图对比。
3. 使用 `scripts/compare_images.py`（或等效工具）检查像素差异。
4. 逐项校验矢量、文本、位图切图的坐标、尺寸、颜色、透明度。
5. 运行 `scripts/audit_png_assets.py --require-transparent-bg` 确认 PNG 透明度与边界。
6. 记录所有校验步骤并在交付报告中说明。

## 交付说明
- 代码文件（HTML/CSS/JS 或 React/Vite）
- 切图资源目录（PNG）
- `layers.manifest.json`
- Bbox 预览图或等效说明
- QA 对照截图与差异报告
- PNG 审计结果
- 已知限制（缺少原字体、遮挡元素等）

---
