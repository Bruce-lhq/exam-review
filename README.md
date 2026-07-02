# exam-review · 期末复习资料生成器

> 读取一门课程的全部资料（课件 / 笔记 / 真题 / 作业），通过交互式对话确认范围与难度，自动生成两份交互式 HTML：一份完整的复习笔记 + 三套难度递进的全真模拟卷。

清华大学人工智能创新大赛 · 技能开发专项赛参赛作品 · 清小搭技能库

---

## 解决什么问题

期末复习时，一门课的资料往往分散成几十个文件：PDF 课件、Word 笔记、PPT、历年真题、作业……学生要自己通读、提炼重点、归纳题型、找模拟题——耗时且容易遗漏。**exam-review 把这整个流程自动化**：吃透全部资料，生成结构化、可交互、可自测的复习材料。

## 核心能力

- **多格式资料统一读取**：PDF / DOCX / PPTX / XLS / EPUB / MD，统一用 `markitdown` 提取文本
- **逐项确认的对话流程**：资料清单 → 知识大纲 → 知识点标签 → 题型分布 → 难度，每一步等用户确认，不擅自决定
- **复习笔记 HTML**：核心概念 / 题型归纳 / 易错点 / 真题详解 / 习题大全；双栏对齐（通用解法 ↔ 具体例题）；跨 Part 交叉引用导航栈
- **全真模拟卷 HTML**：A 基础 / B 综合 / C 冲刺三卷；倒计时器、自评计分、localStorage 持久化
- **增量更新**：新增 / 修改 / 删除资料后，对照 manifest 精准更新对应 Part，不必从头再来

## 依赖与安装

需 Python ≥ 3.9。

各系统安装依赖：

| 系统 | 命令 |
|---|---|
| Windows | `pip install -r requirements.txt` |
| macOS | `pip3 install -r requirements.txt` |
| Linux | `pip install -r requirements.txt` |

或跨平台统一写法（推荐）：`python -m pip install -r requirements.txt`

唯一核心依赖是 [`markitdown[all]`](https://github.com/microsoft/markitdown)（微软开源，统一文档转 Markdown）。**无 MCP 依赖、不调用任何外部 skill——本 skill 完全自包含。**

## 快速上手

把课程资料放在一个目录里，对搭载本 skill 的 agent 说：

> 帮我整理《XXX》的期末复习

或直接触发 `/exam-review`。skill 会：

1. 扫描目录，展示**资料清单**和**知识大纲**，等你确认范围
2. 提取**知识点标签**，等你审核增删
3. 确认**模拟卷题型分布**与**难度**（先出代表题校准）
4. 生成两份 HTML 到课程目录

用浏览器打开即可使用。

## 产出示例

真实案例：**《概率论与数理统计》**——85+ 份资料（14 份 PDF 课件 + 15 份课堂笔记 + 14 份小结 + 习题课 + 真题 + 作业）→ `概统期末复习.html`（5 个 Part、81 张卡片）+ `期末模拟真题.html`（3 卷、48 题）。

- 完整使用流程：见 [`tests/example-usage.md`](tests/example-usage.md)
- 复习笔记 demo（浏览器可直开，Part A–E + 全部交互）：见 [`resources/example-math-review.html`](resources/example-math-review.html)
- 模拟卷 demo（浏览器可直开，三卷 Tab + 倒计时 + 自评计分）：见 [`resources/example-math-exam.html`](resources/example-math-exam.html)

## 目录结构

```
exam-review/
├── SKILL.md                         # 主入口：YAML 元数据 + 执行指令
├── README.md                        # 本文件
├── requirements.txt                 # markitdown[all]
├── scripts/
│   └── extract.py                   # markitdown 统一读取入口（文件/目录）
├── templates/
│   ├── math/                        # 数学型模板（特有规格见 templates/math/README.md）
│   └── physics/                     # 物理型模板（力学/热/电/光，见 templates/physics/README.md）
├── tests/
│   └── example-usage.md             # 详细使用示例（概统真实案例）
└── resources/
    ├── example-math-review.html     # 数学复习笔记 demo（Part A–E）
    ├── example-math-exam.html       # 数学模拟卷 demo（三卷 + 计分）
    ├── example-physics-review.html  # 物理复习笔记 demo（Part A–E，C 为模型图鉴 + SVG）
    └── example-physics-exam.html    # 物理模拟卷 demo（完整三卷，120 分钟保真）
```

## 设计亮点

- **逐项确认纪律**：内置"一次一问、确认后再进下一步"的对话纪律，杜绝一口气抛结果或替用户决定
- **双栏对齐**：每道例题的「通用解法」与「具体推导」逐行横向对齐——复习笔记最核心的交互
- **导航栈交叉引用**：Part 间链接支持跳转 + 面包屑多级回退，永远不丢位置
- **难度可调**：模拟卷生成前先出代表题校准难度，循环至满意再生成完整卷
- **可增量更新**：基于 manifest 的文件 hash 追踪，新增资料精准并入对应 Part

## 适用场景

以「定义 → 定理 → 公式 → 题型」为主干的理工课程：高等数学、线性代数、概率统计、离散数学、电路等。其他学科可通过内置流程扩展专属模板。

---

版本 v1.0.0 · 2026-07 · 清华大学人工智能创新大赛参赛作品
