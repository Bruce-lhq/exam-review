#!/usr/bin/env python3
"""exam-review skill · 文件提取入口

统一用 markitdown 把 PDF / DOCX / PPTX / XLS / EPUB / HTML 等格式转为 Markdown 文本，
作为 Phase 1 资料分析的输入。

用法：
    python scripts/extract.py <文件>                  # 文本输出到 stdout
    python scripts/extract.py <文件> -o output.md     # 写入指定文件
    python scripts/extract.py <目录>                  # 批量提取目录下所有支持的文件
"""

import argparse
import sys
from pathlib import Path

SUPPORTED_EXT = {
    ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
    ".epub", ".html", ".htm", ".csv", ".json", ".xml", ".md", ".txt",
}


def convert_one(md, src: Path, out: Path | None) -> int:
    """提取单个文件，返回字符数。"""
    try:
        result = md.convert(str(src))
    except Exception as e:
        sys.stderr.write(f"⚠️  提取失败 {src}: {e}\n")
        return 0
    text = result.text_content or ""
    if out:
        out.write_text(text, encoding="utf-8")
        sys.stderr.write(f"✓ {src.name} → {out}（{len(text)} 字符）\n")
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    return len(text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="用 markitdown 统一提取课程资料文本（exam-review skill）",
    )
    parser.add_argument("path", help="要提取的文件或目录路径")
    parser.add_argument("-o", "--out", help="输出文件（仅单文件模式）；默认输出到 stdout")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        sys.exit(f"❌ 路径不存在：{target}")

    try:
        from markitdown import MarkItDown
    except ImportError:
        sys.exit(
            "❌ 未安装 markitdown。\n"
            "   安装依赖：uv pip install -r requirements.txt\n"
            "   或单独安装：uv pip install 'markitdown[all]'"
        )

    md = MarkItDown()

    if target.is_file():
        convert_one(md, target, Path(args.out) if args.out else None)
    elif target.is_dir():
        files = sorted(
            f for f in target.rglob("*") if f.suffix.lower() in SUPPORTED_EXT and f.is_file()
        )
        if not files:
            sys.exit(f"❌ 目录中没有支持的文件：{target}")
        sys.stderr.write(f"找到 {len(files)} 个文件，开始提取…\n\n")
        total = 0
        for f in files:
            total += convert_one(md, f, None)
        sys.stderr.write(f"\n共提取 {len(files)} 个文件，{total} 字符。\n")
    else:
        sys.exit(f"❌ 不是文件也不是目录：{target}")


if __name__ == "__main__":
    main()
