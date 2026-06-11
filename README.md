# Claude Skills

个人维护的 [Claude Code / Agent Skills](https://docs.anthropic.com/en/docs/claude-code) 集合。

## 目录

| Skill | 说明 |
|-------|------|
| [`web-app-test`](skills/web-app-test/) | 网页应用自动化测试：用 Playwright 驱动真实浏览器模拟用户操作，连接真实后端做端到端验证，附带后端/API/构建测试脚本作为底层保障。 |

## 安装

### 用 skills.sh CLI（推荐）

精确安装本仓库中的 `web-app-test` skill：

```bash
# 装到当前项目
npx skills add Mencius2023/skills@web-app-test

# 装到全局（所有项目共享）
npx skills add Mencius2023/skills@web-app-test -g -y
```

> `@web-app-test` 精确指定仓库中的某个 skill。省略它（`npx skills add Mencius2023/skills`）会安装仓库内全部 skill —— 仓库内多于一个 skill 时会让你选择。

### 手动安装到全局（所有项目共享）

```bash
git clone https://github.com/Mencius2023/skills.git
cp -r skills/skills/web-app-test ~/.claude/skills/web-app-test
```

更新：`cd skills && git pull && cp -r skills/web-app-test ~/.claude/skills/`

## 结构约定

每个 skill 只包含**通用、可跨项目复用**的内容（`SKILL.md` + `templates/`）。
项目专属的实例（测试规格书、可执行脚本等）由模板在**被测项目内**落地生成，
随该项目自己的仓库走，不纳入本仓库。详见各 skill 的 `SKILL.md`。
