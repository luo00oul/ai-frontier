# GitHub Pages 发布与验收

目标仅为当前用户个人账号下的公开仓库 `ai-frontier`。先取得已认证用户名，不猜测账号或组织；不改动其他仓库。

## 权限检查

1. 用已连接 GitHub 读取本人 login、安装的仓库范围与目标仓库权限。新建仓库通常仍需相应账号权限；连接成功不代表能创建仓库。
2. 查询 `<login>/ai-frontier`。不存在且允许创建时，创建公开仓库。403 不应当作 404。
3. 已存在时先读取 README、默认分支、树和权限；只有确认属于本项目才在独立分支追加并审阅差异，不能覆盖无关同名项目。
4. 如连接工具不能创建仓库或管理 Pages，可用已经授权的 `gh`。未登录时停下，不索要在对话中粘贴个人令牌。

## 创建与推送（仅已认证且确认不存在后）

在本工程目录运行，不要在其他项目中运行：

```sh
git init -b main
git add site scripts docs README.md package.json .gitignore .github
git commit -m 'Build AI Frontier Explorer with first world-models issue'
gh repo create ai-frontier --public --source=. --remote=origin --push
```

创建前必须通过 API 证实同名仓库不存在。若创建或推送失败，先读取远程状态，不要重复创建，也不强制推送。

## Pages 设置

在目标仓库 Settings → Pages → Build and deployment → Source 选择 **GitHub Actions**。需要目标仓库管理 Pages 的权限；可能受组织策略限制。发布工作流需要 `pages:write` 与 `id-token:write`。不需要在静态网页中放置任何密钥。

如果已认证 API 支持，可通过 `POST repos/<owner>/ai-frontier/pages` 并设置 `build_type: workflow` 启用。已存在则先读取配置，按需修改；不要用异常当作启用成功。

## 验收

1. 查看 Actions 中 `Validate and deploy GitHub Pages` 成功，以及 Pages API 返回的真实 URL。
2. 对真实 URL 发起公开未认证请求，确认 HTTP 200，页面标题为 AI 前沿探索。
3. 打开首页、归档、专题深链接、实验和来源。资源必须在 `/ai-frontier/` 下可读。
4. 保存兴趣和笔记、刷新后仍保留；验证导入导出。当前端域名变化时，原域名笔记需自行导出再导入。
5. 至少检查 390px 和桌面宽度，确认正文无横向溢出。

任何一步未完成，都必须报告实际状态；本地预览地址不是公开部署地址。

参考：
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
