// Playwright 配置 - <产品名> 浏览器 E2E
//
// 模板说明：落地到具体项目时替换 <...> 占位符（前端目录、端口、产物目录、复用环境变量名）。
// 本配置文件必须在 TEST_SPECIFICATION.md「附录 D：脚本清单」中登记并链接。
import { defineConfig, devices } from '@playwright/test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
// 落地后本文件位于 <被测项目根>/web-app-test/scripts/，往上 2 级到项目根
const PROJECT_ROOT = path.resolve(__dirname, '..', '..')
const EDITOR_ROOT = path.join(PROJECT_ROOT, '<前端目录>')
const ARTIFACTS = path.join(PROJECT_ROOT, '<产物目录>')

const REUSE = process.env.<REUSE_FLAG> === '1'

export default defineConfig({
  testDir: __dirname,
  testMatch: '**/*.spec.js',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [['list'], ['html', { outputFolder: path.join(ARTIFACTS, 'report'), open: 'never' }]],
  outputDir: path.join(ARTIFACTS, 'test-results'),
  use: {
    baseURL: 'http://localhost:<前端端口>',
    headless: true,
    viewport: { width: 1366, height: 900 },
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'off',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: {
    command: 'npm run dev -- --host localhost --port <前端端口> --strictPort',
    cwd: EDITOR_ROOT,
    url: 'http://localhost:<前端端口>',
    timeout: 60_000,
    reuseExistingServer: REUSE,
    stdout: 'ignore',
    stderr: 'pipe',
  },
})
