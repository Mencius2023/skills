#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<产品名> 非交互测试运行器（CI 首选入口）。

模板说明：本文件是通用脚手架，落地到某个项目时把 <...> 占位符替换为该项目的真实
脚本路径、命令与目录，并删除用不到的层级。本运行器**必须**在 TEST_SPECIFICATION.md
的「附录 D：脚本清单」中登记并链接（见 SKILL.md 约定：所有脚本由规格书管理）。

按测试金字塔由快到慢、由轻到重的顺序执行，任一层失败立即中断并返回该退出码（fail-fast）。
层按种类命名（不用 L0–L5 之类层号，理由见 SKILL.md「测试分层与规格书组织」）：
  单测   冒烟 + 数据完整性 + 前端单元测试（存在才跑）+ 配置回归 + 离线核心功能
  构建   前端生产构建
  E2E    浏览器（Playwright，连真实后端）

E2E 这步跑 spec 中两部分：预先设计的 API 契约断言（覆盖主要端点）+ 已沉淀的稳定浏览器流程。
脆弱、易变的浏览器 UI 交互不在本运行器内——由 AI 动态接入浏览器执行（参考 E2E_OPERATION_GUIDE.md），
测完后判断需回归才沉淀为 spec。

注意：AI 手动执行测试时不受本运行器的 fail-fast 约束（fail-fast 只为节省 CI 资源），
应尽量跑完所有用例再一次报告（见 SKILL.md 核心原则）。

用法（在项目根目录）：
  python .claude/skills/web-app-test/scripts/run_regression.py
  python .claude/skills/web-app-test/scripts/run_regression.py --skip-browser
  python .claude/skills/web-app-test/scripts/run_regression.py --quick
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List

# 落地后本脚本位于 <被测项目根>/web-app-test/scripts/run_regression.py
SCRIPTS_DIR = Path(__file__).resolve().parent          # web-app-test/scripts/
PROJECT_ROOT = SCRIPTS_DIR.parent.parent               # 被测项目根
EDITOR_ROOT = PROJECT_ROOT / "<前端目录>"
# 后端测试脚本所在目录（按项目实际填写）
BACKEND_TESTS = PROJECT_ROOT / "<后端测试脚本目录>"


def npm() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


def npx() -> str:
    return "npx.cmd" if sys.platform == "win32" else "npx"


def run(label: str, command: List[str], cwd: Path, allow_fail: bool = False) -> None:
    print("=" * 80)
    print(f"[RUN] {label}")
    print(f"[CWD] {cwd}")
    print(f"[CMD] {' '.join(str(c) for c in command)}")
    print("=" * 80)
    result = subprocess.run(command, cwd=str(cwd))
    if result.returncode != 0:
        if allow_fail:
            # 非阻塞：打印警告但不中断套件（用于会如实报出预存数据问题的审计步骤）
            print(f"[WARN] {label} (exit {result.returncode}) — 非阻塞，继续执行")
            return
        print(f"[FAIL] {label} (exit {result.returncode})")
        raise SystemExit(result.returncode)
    print(f"[PASS] {label}")


def has_unit_test_script() -> bool:
    """前端补齐单元测试后，package.json 会有 test:unit 脚本。"""
    pkg = EDITOR_ROOT / "package.json"
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
        return "test:unit" in data.get("scripts", {})
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="<产品名> 非交互测试运行器")
    parser.add_argument("--skip-browser", action="store_true", help="跳过浏览器 E2E（无 Chromium 环境）")
    parser.add_argument("--quick", action="store_true", help="只跑单测快检")
    parser.add_argument("--reuse-ui", action="store_true", help="复用已运行的前端做 E2E")
    args = parser.parse_args()

    config = SCRIPTS_DIR / "playwright.config.js"

    # 单测 · 冒烟 + 数据完整性
    run("单测 · 冒烟测试", [sys.executable, str(BACKEND_TESTS / "<smoke_test.py>")], PROJECT_ROOT)
    # 示例：非阻塞审计步骤（如有），用 allow_fail=True
    # run("单测 · 数据完整性审计", ["node", str(EDITOR_ROOT / "scripts" / "<audit>.mjs")], EDITOR_ROOT, allow_fail=True)

    # 单测 · 前端单元测试（存在才跑）
    if has_unit_test_script():
        run("单测 · 前端单元测试", [npm(), "run", "test:unit"], EDITOR_ROOT)
    else:
        print("[SKIP] 单测 · 前端单元测试：package.json 暂无 test:unit 脚本")

    # 单测 · 配置回归 + 离线核心功能
    run("单测 · 配置回归", [sys.executable, str(BACKEND_TESTS / "<config_regression.py>")], PROJECT_ROOT)
    run("单测 · 离线标准流程", [sys.executable, str(BACKEND_TESTS / "<standard_flow_test.py>")], PROJECT_ROOT)

    if args.quick:
        print("=" * 80)
        print("[PASS] 快检通过（单测核心）")
        return 0

    run("单测 · 核心功能测试", [sys.executable, str(BACKEND_TESTS / "<test_core_functions.py>")], PROJECT_ROOT)

    # 构建 · 前端生产构建
    run("构建 · 前端生产构建", [npm(), "run", "build"], EDITOR_ROOT)

    # E2E · 浏览器（Playwright）— API 契约（预设计）+ 已沉淀的稳定浏览器流程
    if not args.skip_browser:
        env_note = "(复用已运行前端)" if args.reuse_ui else "(自动拉起前端)"
        cmd = [npx(), "playwright", "test", "--config", str(config)]
        run(f"E2E · 浏览器(Playwright){env_note}", cmd, EDITOR_ROOT)
    else:
        print("[SKIP] E2E · 浏览器（--skip-browser）")

    print("=" * 80)
    print("[PASS] <产品名> 回归测试套件全部通过")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
