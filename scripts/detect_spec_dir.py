#!/usr/bin/env python3
"""
自动检测当前 Git 分支对应的 Spec 目录

使用方法:
    python detect_spec_dir.py

返回:
    - 如果找到匹配的 spec 目录，输出目录路径
    - 如果未找到，输出错误信息和建议
"""

import subprocess
import os
from pathlib import Path


def get_current_branch() -> str:
    """获取当前 Git 分支名称"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def find_spec_dir(branch_name: str, specs_root: Path) -> Path | None:
    """
    查找与分支名匹配的 spec 目录
    
    匹配规则:
    1. 精确匹配: specs/{branch_name}/
    2. 模糊匹配: specs/{branch_name 去除数字前缀}/
    3. 包含匹配: specs/ 下任何包含分支关键词的目录
    """
    if not specs_root.exists():
        return None
    
    # 1. 精确匹配
    exact_match = specs_root / branch_name
    if exact_match.exists() and exact_match.is_dir():
        return exact_match
    
    # 2. 获取所有 spec 目录
    spec_dirs = [d for d in specs_root.iterdir() if d.is_dir()]
    
    # 3. 模糊匹配 - 去除数字前缀
    # 例如: 002-doc-chunking-opt -> doc-chunking-opt
    branch_without_prefix = branch_name.lstrip('0123456789-')
    for spec_dir in spec_dirs:
        dir_without_prefix = spec_dir.name.lstrip('0123456789-')
        if dir_without_prefix == branch_without_prefix:
            return spec_dir
    
    # 4. 包含匹配 - 提取关键词
    # 例如: 002-doc-chunking-opt -> ["doc", "chunking", "opt"]
    keywords = branch_name.lstrip('0123456789-').split('-')
    for spec_dir in spec_dirs:
        dir_name = spec_dir.name.lower()
        if all(kw.lower() in dir_name for kw in keywords if len(kw) > 2):
            return spec_dir
    
    return None


def main():
    # 获取项目根目录（假设脚本在 .codebuddy/skills/vibe-spec-sync/scripts/ 下）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent.parent
    specs_root = project_root / "specs"
    
    # 获取当前分支
    branch = get_current_branch()
    if not branch:
        print("❌ 错误: 无法获取当前 Git 分支")
        print("   请确保当前目录在 Git 仓库中")
        return 1
    
    print(f"📌 当前分支: {branch}")
    
    # 查找 spec 目录
    spec_dir = find_spec_dir(branch, specs_root)
    
    if spec_dir:
        print(f"✅ 找到 Spec 目录: {spec_dir.relative_to(project_root)}")
        
        # 检查关键文件
        key_files = ["spec.md", "tasks.md", "data-model.md", "api.md"]
        print("\n📁 Spec 文件状态:")
        for f in key_files:
            file_path = spec_dir / f
            status = "✓ 存在" if file_path.exists() else "✗ 不存在"
            print(f"   - {f}: {status}")
        
        # 检查 decisions 目录
        decisions_dir = spec_dir / "decisions"
        if decisions_dir.exists():
            adr_count = len(list(decisions_dir.glob("ADR-*.md")))
            print(f"   - decisions/: ✓ 存在 ({adr_count} 个 ADR)")
        else:
            print("   - decisions/: ✗ 不存在")
        
        return 0
    else:
        print(f"❌ 未找到匹配的 Spec 目录")
        print(f"\n💡 建议:")
        print(f"   1. 创建目录: specs/{branch}/")
        print(f"   2. 或手动指定 spec 目录路径")
        
        if specs_root.exists():
            available_dirs = [d.name for d in specs_root.iterdir() if d.is_dir()]
            if available_dirs:
                print(f"\n📂 现有 Spec 目录:")
                for d in sorted(available_dirs):
                    print(f"   - {d}")
        
        return 1


if __name__ == "__main__":
    exit(main())
