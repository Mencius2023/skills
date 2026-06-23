# 模板目录（templates/）

本目录存放**项目无关**的脚手架，用于为一个**新接入的项目**从头创建测试说明文档与脚本。模板从 BTGen 项目的真实 `TEST_SPECIFICATION.md` 与 `scripts/` 提炼而来，去掉了 BTGen 专属内容，保留可复用的结构与约定。

> 模板本身是通用资产，**不要项目化**。为某个项目落地时，把模板**拷贝到被测项目根目录的 `web-app-test/`**（脚本进 `web-app-test/scripts/`），再按该项目的真实情况填写占位符 `<...>`，删除用不到的层级/用例。落地产物属于被测项目，应进项目自己的 git 仓库——**不要写回 skill 目录**。

## 何时使用

当 `TEST_SPECIFICATION.md` 与 `scripts/` **不存在**、或**是从别的项目拷来的**（即不针对当前项目）时，说明这是一个新接入的项目。此时：

1. 先阅读当前项目的前端源码、后端源码、API 文档、用户指南；
2. 以本目录的模板为骨架，**从头**为当前项目创建 `TEST_SPECIFICATION.md` 与 `scripts/`；
3. 按下文「占位符」逐项替换，覆盖该项目真实的功能点、API 契约、选择器契约、目录与端口。

详见 `../SKILL.md`「项目专属内容：每次测试前先审查」。

## 文件清单

| 模板文件 | 落地为（被测项目根 `web-app-test/`） | 用途 |
|---------|--------|------|
| `TEST_SPECIFICATION.template.md` | `web-app-test/TEST_SPECIFICATION.md` | 测试说明文档（主文档）骨架。开头声明所属产品，**按功能域组织用例、层（单测/构建/API/E2E）作命名列、ID=域.序**，附录登记选择器契约、fixture、环境配置、**脚本清单与链接** |
| `run_regression.template.py` | `web-app-test/scripts/run_regression.py` | 非交互回归运行器（CI 入口），按 单测→构建→API→E2E 分层 fail-fast。**预先设计**，落地即填好 |
| `playwright.config.template.js` | `web-app-test/scripts/playwright.config.js` | Playwright 配置（baseURL、产物目录、webServer 自动拉起）。**预先设计** |
| `standard-flow.spec.template.js` | `web-app-test/scripts/<flow>.spec.js` | API 契约 + 浏览器流程 spec 骨架。**API 契约部分预先写满、覆盖主要端点**；**浏览器流程部分不预先写满**，由 AI 动态测完后按需沉淀时参考此骨架 |

## 占位符约定

模板中用尖括号包裹的 `<...>` 均为待替换占位符，常见的有：

| 占位符 | 含义 | BTGen 示例 |
|--------|------|-----------|
| `<产品名>` | 被测产品名称 | BTGen 行为树生成系统 |
| `<前端目录>` | 前端工程相对路径 | `behavior-tree-editor` |
| `<后端启动命令>` | 后端服务启动命令 | `cd bt_server && python server.py` |
| `<前端端口>` / `<后端端口>` | 固定端口 | 5173 / 8085 |
| `<前端健康检查>` / `<后端健康检查>` | 健康检查命令 | `curl -s localhost:8085/api/health` |
| `<产物目录>` | 截图/报告/trace 输出目录 | `testing_script/artifacts/playwright/` |
| `<环境前提>` | conda/node 等运行前提 | conda 环境 `nl2bt` |
| `<testid-*>` | 前端 data-testid 选择器 | `prompt-textarea` 等 |

## 核心约定（落地时必须遵守）

1. **测试说明文档开头必须声明所属产品**：第一段写清「本文档是 `<产品名>` 的测试用例规格书」，让任何人一眼知道这套测试针对哪个产品。
2. **所有脚本都必须被测试说明文档管理并链接**：`scripts/` 下的每个可执行脚本，都要在 `TEST_SPECIFICATION.md` 的「脚本清单」附录里登记——脚本路径、对应哪些用例、复跑命令。规格书是脚本的唯一索引，不允许出现「孤儿脚本」（存在于 `scripts/` 但文档里查不到）。
3. **测试层按种类命名，不用 L0–L5 之类层号**（理由见 `../SKILL.md`「测试分层与规格书组织」）：四个层为 **单测 / 构建 / API / E2E**；正文按功能域组织、层作命名列、用例 ID=`域.序`。
4. **脚本设计策略分两类**：
   - **程序测试脚本（单测 / 构建 / API）必须预先设计**，并覆盖产品主要功能（核心数据、关键配置、核心流程、主要 API、错误处理、生产构建等）。`run_regression.py` 与各后端测试脚本属于此类，落地时就要写好。
   - **E2E 浏览器流程的 Playwright spec 不预先设计**，由 AI 动态接入浏览器测完功能后，现场判断是否需回归再沉淀。`standard-flow.spec.template.js` 只是一个**沉淀时**可参考的骨架，不要求落地即写满所有 E2E 用例。
5. **规格书不是设计文档**：每条用例必须挂有实际可执行资源（脚本 / 可直接运行的命令）或明确标为 AI 动态执行。
