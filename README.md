# canlab

车载 CAN 日志的自动体检工具。读日志 → 按 DBC 解信号 → 自动找出周期抖动 / 丢帧 / 信号越界 → 一条命令跑完台架点检 → 接成每日回归。

> 12 周学习路线（W1–W12）的产物仓库。所有数据由 `tools/` 下的脚本生成，仓库里不放任何二进制日志。

## 现在能做什么

| 阶段 | 命令 | 状态 |
|---|---|---|
| W0 | `python check_env.py` | ✅ 环境自检 |
| W3 | 待定（`src/insight/analyze.py`） | ⏳ |
| W4 | 待定（`src/canlog/io.py`） | ⏳ |
| W8 | 待定（`steps/` + `run.py`） | ⏳ |

## 环境复现

要求：Windows · Python **3.12**（不要用 3.13，PyCharm 2024.1 不支持）

```bat
git clone <你的仓库地址> canlab
cd canlab
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python check_env.py
```

## 目录说明

```
src/canlog/   核心包：日志解析、DBC 解码、异常检测
src/insight/  W3 的数据分析
tools/        数据生成器（测试结果 / CAN 日志 / 故障样本）
tests/        pytest 用例
steps/        W8 台架步骤，一个文件一步
data/         生成的数据（不进仓库）
out/          图 / CSV / HTML 报告（不进仓库）
notes/        每周笔记、复盘、errors.md
week01-03/    前期语法练习
progress.md   12 周进度与「啊哈时刻」
```

## 约定

- 只用本项目的 `.venv`，不碰任何 conda 环境
- 数据只能由 `tools/` 生成，禁止把外部文件拷进 `data/`
- 每次提交前跑：`ruff check . --fix` + `mypy src` + `pytest`
