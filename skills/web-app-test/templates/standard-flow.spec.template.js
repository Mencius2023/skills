// <产品名> 浏览器 E2E + API 契约测试 - 真实后端集成
// 前提：后端运行在 localhost:<后端端口>，前端运行在 localhost:<前端端口>
//
// 模板说明：落地到具体项目时替换 <...> 占位符，按真实 API 契约/选择器补全断言。
// 本 spec 必须在 TEST_SPECIFICATION.md「附录 D：脚本清单」中登记并链接。
//
// 本 spec 含两部分，设计策略不同（见 SKILL.md「测试分类」）：
//   A. API 契约断言（纯 HTTP，不经浏览器）—— 属程序测试，【落地即写】，覆盖主要端点
//   B. 浏览器流程（Playwright 驱动浏览器）—— 【不预先写满】，由 AI 动态测完判断需回归后
//      才沉淀到此处；下方浏览器用例仅为「页面加载」「核心全流程」两条稳定示例骨架
//
// 脆弱、易变的浏览器 UI 交互不写在这里，由 AI 动态接入浏览器执行（参考 ../L4_OPERATION_GUIDE.md）；
// 测完判断需回归且流程稳定，再补充为下方 describe 中的一条 test 并登记到附录 D。
import { test, expect } from '@playwright/test'

const BACKEND = 'http://localhost:<后端端口>'

// 与离线测试共用的标准 fixture（见 TEST_SPECIFICATION.md 附录 B）
const FIXTURE = {
  // <标准 fixture 数据>
}

// ---------------------------------------------------------------------------
// A. API 契约断言（纯 HTTP，不经浏览器，稳定可批量复跑）— 落地即写，覆盖主要端点
// ---------------------------------------------------------------------------
test.describe('<产品名> API 契约', () => {
  // T4-A1 健康检查与配置
  test('健康检查与配置', async ({ request }) => {
    const health = await request.get(`${BACKEND}/api/health`)
    expect(health.ok()).toBeTruthy()
    expect((await health.json()).<就绪标志>).toBe(true)

    const config = await request.get(`${BACKEND}/api/config`)
    expect(config.ok()).toBeTruthy()
    const configBody = await config.json()
    expect(configBody).toHaveProperty('<关键配置字段>')
  })

  // T4-A2 API 错误处理
  test('错误处理', async ({ request }) => {
    const r1 = await request.post(`${BACKEND}/api/<主端点>`, { data: {} })
    expect([400, 422]).toContain(r1.status())

    const r2 = await request.get(`${BACKEND}/api/nonexistent`)
    expect(r2.status()).toBe(404)
  })

  // T4-An <其他主要端点的契约用例，如 CRUD>
  // test('<用例名>', async ({ request }) => { ... })
})

// ---------------------------------------------------------------------------
// B. 浏览器流程（Playwright 驱动浏览器）— 不预先写满，仅沉淀稳定流程
//    下面两条是「页面加载」「核心全流程」示例骨架；其余浏览器用例由 AI 动态测完按需补入
// ---------------------------------------------------------------------------
test.describe('<产品名> 浏览器流程（真实后端）', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('[data-testid=<主输入元素>]')).toBeVisible({ timeout: 20000 })
  })

  // T4-B1 页面加载与初始状态
  test('页面加载与初始状态', async ({ page }) => {
    await expect(page.locator('[data-testid=<配置元素>]')).toHaveValue('<默认值>')
    await expect(page.locator('[data-testid=<主按钮>]')).toBeVisible()
  })

  // T4-B2 核心业务全流程
  test('核心业务全流程', async ({ page }) => {
    await page.locator('[data-testid=<主输入元素>]').fill('<示例输入>')
    await page.locator('[data-testid=<主按钮>]').click()
    // 对不确定输出用「至少 N 个」而非精确数
    await expect(page.locator('<结果元素>').first()).toBeVisible({ timeout: 180000 })
    const count = await page.locator('<结果元素>').count()
    expect(count).toBeGreaterThanOrEqual(1)
  }, { timeout: 600000 })
})
