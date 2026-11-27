# AI 前沿探索 · AI Frontier Explorer

简体中文个人学习网站，原生 HTML / CSS / JavaScript，无前端依赖。首期为 2026-11-27 世界模型专题，包含八个阅读部分、六个原始来源、浏览器实验与 Python 实践。

## 本地运行

需要 Python 3.10+；Node 仅用于可选 JavaScript 语法检查。

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

打开 http://localhost:8000 。不要直接双击 HTML：浏览器通常不允许 file:// 页面 fetch JSON。

```sh
node --check site/assets/app.js
python3 site/practice/world_model.py
```

## 结构

- `site/index.html`：页面外壳；`site/assets/`：原生交互与响应式样式。
- `site/data/issues.json`：主题注册表与专题内容，schemaVersion 为 1。
- `site/practice/`：可运行教学实践。
- `scripts/content.py`：内容结构、引用、日期与唯一性校验。
- `scripts/add_issue.py`：校验后原子追加专题，相同内容重复导入不改动，拒绝覆盖同 ID 的不同内容。
- `scripts/build.py`：验证并生成 `dist/`。
- `.github/workflows/pages.yml`：推送 main 后验证与发布 Pages；PR 仅验证。
- `.github/workflows/publish-issue.yml`：授权调用后，将单期 JSON 校验、提交并直接发布 Pages。
- `docs/PUBLISHING.md`：GitHub 权限、Pages 启用和验收。
- `docs/AUTOMATION.md`：每周任务接入说明与尚需验证的边界。

站点使用 `#/issue/<id>` 路由和相对资源路径，适配 GitHub Pages `/ai-frontier/` 子目录。归档支持搜索和兴趣过滤。新增主题可加入 topics 注册表，再按 topic 构建对应入口；当前 UI 仅开放“AI 前沿探索”。所有正文以纯文本转义后呈现。

## 兴趣数据

保存在当前域名、当前浏览器的 localStorage，可导出/合并导入 JSON。不会上传到 GitHub，不跨设备同步，不自动传给 ChatGPT 周任务。清理数据、无痕窗口、换域名/浏览器可能丢失。关闭存储权限时会提示内存模式；请立即导出。没有在仓库内附带个人兴趣数据。

## 内容说明

首期为原创教学整理，来源和发布日期逐项列明；产品官方描述不等于独立评测。小实验是一维线性系统的最小二乘拟合，并非 Genie 或 Dreamer 复现。之后每期须重新核查时效与原文。

## 发布状态

工程已准备，但工程中的工作流文件本身不能证明 GitHub 仓库、Pages 或每周自动化已启用。只有远程写入、Actions 成功和公开 URL 实测后，才能宣布上线。实际状态请以本次交付说明和 GitHub Actions 为准。
