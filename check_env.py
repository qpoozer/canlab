"""W0 环境自检 —— 全绿才算装修完。

用法（在项目根目录、终端提示符带 (.venv) 时）：
    python check_env.py

退出码 0 = 全通过；1 = 有未通过项。
"""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_fail = 0


def _check(cond: bool, ok_text: str, bad_text: str | None = None) -> None:
    global _fail
    if cond:
        print(f"  [ OK ] {ok_text}")
    else:
        print(f"  [FAIL] {bad_text or ok_text}")
        _fail += 1


def main() -> int:
    global _fail

    print("=" * 64)
    print("canlab 环境自检")
    print("=" * 64)

    # 1. 解释器 ----------------------------------------------------------
    print("\n[1] 解释器")
    in_venv = sys.prefix != sys.base_prefix
    _check(in_venv, f"已在虚拟环境中: {sys.prefix}",
           f"不在虚拟环境中: {sys.prefix}（应先激活 .venv）")
    _check(sys.version_info[:2] == (3, 12),
           f"Python {sys.version.split()[0]}",
           f"Python {sys.version.split()[0]}，要求 3.12（PyCharm 2024.1 不支持 3.13）")
    _check(Path(sys.prefix).name == ".venv",
           "解释器指向本项目的 .venv",
           f"解释器指向 {sys.prefix}，不是本项目 .venv（可能装到 conda 里了）")

    # 2. 依赖 ------------------------------------------------------------
    print("\n[2] 依赖")
    need = {
        "can": "python-can",
        "cantools": "cantools",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "pytest": "pytest",
        "serial": "pyserial",
        "msgpack": "msgpack",
    }
    for mod, name in need.items():
        try:
            m = importlib.import_module(mod)
            ver = getattr(m, "VERSION", None) or getattr(m, "__version__", "?")
            print(f"  [ OK ] {name:<12} {ver}")
        except Exception as exc:  # noqa: BLE001
            print(f"  [FAIL] {name:<12} 未安装（{type(exc).__name__}）")
            _fail += 1

    # 3. 目录结构 --------------------------------------------------------
    print("\n[3] 目录结构")
    for d in ("src/canlog", "src/insight", "tools", "tests", "steps",
              "data", "out", "notes", "week01", "week02", "week03"):
        _check((ROOT / d).is_dir(), f"{d}/", f"{d}/ 不存在")

    # 4. Git -------------------------------------------------------------
    print("\n[4] Git")
    _check(shutil.which("git") is not None, "git 可执行", "找不到 git")
    _check((ROOT / ".git").exists(), "已是 Git 仓库",
           "还不是 Git 仓库（PyCharm 新建时勾「创建 Git 仓库」，或手动 git init）")
    for key in ("user.name", "user.email"):
        r = subprocess.run(["git", "config", "--global", key],
                           capture_output=True, text=True)
        val = r.stdout.strip()
        _check(bool(val), f"git {key} = {val}", f"git {key} 未配置（提交作者会是电脑默认名）")

    # 5. 跨进程虚拟总线（W8 依赖） ---------------------------------------
    print("\n[5] CAN 虚拟总线")
    try:
        import can  # noqa: PLC0415

        bus = can.Bus(interface="udp_multicast", channel="239.74.163.1")
        bus.shutdown()
        _check(True, "udp_multicast 可用（W8 跨进程收发靠它）")
    except Exception as exc:  # noqa: BLE001
        _check(False, "", f"udp_multicast 不可用: {type(exc).__name__}: {exc}")

    # 汇总 ---------------------------------------------------------------
    print("\n" + "=" * 64)
    if _fail == 0:
        print("全部通过 —— W0 装修完成，可以进 W1。")
    else:
        print(f"{_fail} 项未通过 —— 先修完再进 W1。")
    print("=" * 64)
    return 0 if _fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
