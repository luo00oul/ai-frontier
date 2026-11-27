# 每周 AI 前沿探索：接入与边界

计划沿用现有“每周 AI 前沿探索”任务，时间为每周五 19:00 Asia/Shanghai。2026-11-27 本次可见任务查询返回 0 项；不能因此断言用户其他会话/账号内没有该任务。为避免重复，本次没有新建或修改任务。

## 已准备的两条发布路径

### 直接内容提交

每周任务读取目标仓库最新内容，核对原始来源，生成单期 JSON，执行：

```sh
python3 scripts/add_issue.py /path/to/issue.json --dry-run
python3 scripts/add_issue.py /path/to/issue.json
python3 scripts/build.py
```

经授权提交 `site/data/issues.json` 到 main 后，Pages 工作流自动更新。若受分支保护限制，创建内容 PR 并准确报告等待合并状态，不绕过保护。

### 授权调用 GitHub Actions

`publish-issue.yml` 接受 `workflow_dispatch` 的 `issue_json` 字符串输入。已登录且具有目标仓库 Actions 写权限的环境可以调用：

```sh
gh workflow run publish-issue.yml --repo luo00oul/ai-frontier --ref main --json < inputs.json
```

其中 inputs.json 是 `{"issue_json":"完整单期 JSON 序列化字符串"}`。工作流仅接受 main，验证后提交内容、构建并直接部署。使用 GITHUB_TOKEN 的提交通常不会再触发另一个 push 工作流，所以这个入口在同一工作流内显式部署，避免把“提交了”误称为“已更新网站”。工作流调用还须轮询运行结果并验证公开 URL。

这条路径不需要外部模型 API 密钥，但仍需要有权生成并提交内容的 ChatGPT 任务环境。GitHub Actions 本身不会研究和撰写每周专题。工作流仅提供发布入口，不能替代周任务。

## 接通前必须确认

- 找到原任务的真实 ID，检查标题、完整原 prompt、是否启用、时区、BYDAY=FR、19:00 和执行环境。
- 保留既有研究/主题偏好，只追加目标仓库和发布步骤。不能直接用本文覆盖未知的原 prompt。
- 验证定时执行环境能够访问连接账号并写目标仓库。当前交互会话连接成功，不代表后台任务继承相同写权限。
- 以一次真实新期内容端到端验证生成、校验、提交、部署、公开访问后，才宣布每周自动更新已接通。
- 不能访问用户浏览器 localStorage。需用户主动导出笔记并提供后，才可将兴趣作为选题依据。

## 给原任务追加的指令草案

在原有研究任务完成后，将本期内容按目标仓库 `site/data/issues.json` 的 schema 组织为新的单期对象。使用独立且稳定的 ID、真实发布日期与核对日期；覆盖核心问题、技术原理、近期进展、代表论文与团队、产业应用、未解决问题、入门路线、可运行实践，并逐条提供原始来源。优先论文与团队原文，明确区分已验证事实、官方报告和推断。

读取 luo00oul/ai-frontier 的最新状态，先校验再以最小差异追加，绝不覆盖历史专题、静态资源或无关仓库。使用已授权的连接或工作流完成提交发布，并检查运行与公开页面。无写入权限、缺少执行环境、来源不可核验或部署失败时，保留待发布 JSON 并说明阻塞，不声称已更新。

目标账号已核实为 luo00oul，仓库为公开的 luo00oul/ai-frontier；任务 ID 不得猜测。本文件不表示自动化已启用。
