# -*- coding: utf-8 -*-
"""生成 Markdown 格式的评估报告"""

import json
from pathlib import Path
from datetime import datetime


def generate_markdown_report(json_path: str = "outputs/eval_report.json") -> str:
    """读取 JSON 评估报告，生成 Markdown 格式"""
    
    # 读取 JSON 报告
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    
    summary = data["summary"]
    failure = data.get("failure_analysis", {})
    suggestions = data.get("improvement_suggestions", [])
    results = data["results"]
    
    # 生成 Markdown
    md = []
    md.append("# 提示词工程评估报告\n")
    md.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("---\n")
    
    # 1. 总览
    md.append("## 一、评估总览\n")
    md.append("| 指标 | 数值 |")
    md.append("|------|------|")
    md.append(f"| 样本总数 | {summary['total']} |")
    md.append(f"| 通过数 | {summary['passed']} |")
    md.append(f"| 通过率 | {summary['pass_rate'] * 100:.1f}% |")
    md.append("")
    
    # 2. 分类统计
    md.append("## 二、分类通过率\n")
    md.append("| 类别 | 总数 | 通过数 | 通过率 |")
    md.append("|------|------|--------|--------|")
    by_type = summary.get("by_type", {})
    for category, stats in by_type.items():
        rate = (stats["passed"] / stats["total"] * 100) if stats["total"] else 0
        md.append(f"| {category} | {stats['total']} | {stats['passed']} | {rate:.0f}% |")
    md.append("")
    
    # 3. 逐条结果
    md.append("## 三、逐条评估结果\n")
    for item in results:
        status = "✅ 通过" if item["passed"] else "❌ 失败"
        md.append(f"### {item['id']} - {status}\n")
        md.append(f"- **类别**：{item['category']}")
        md.append(f"- **得分**：{item['score']}")
        md.append(f"- **检查项**：")
        for check_name, check_result in item["checks"].items():
            icon = "✅" if check_result else "❌"
            md.append(f"  - {icon} {check_name}")
        
        if item["errors"]:
            md.append(f"- **错误**：")
            for error in item["errors"]:
                md.append(f"  - ⚠️ {error}")
        
        md.append(f"\n**输出内容**：\n")
        md.append("```")
        md.append(item["output"])
        md.append("```\n")
    
    # 4. 错误分析
    md.append("## 四、错误分析\n")
    md.append("| 错误类型 | 数量 |")
    md.append("|----------|------|")
    for error_type, count in failure.items():
        md.append(f"| {error_type} | {count} |")
    md.append("")
    
    # 5. 改进建议
    if suggestions:
        md.append("## 五、提示词改进建议\n")
        for i, sug in enumerate(suggestions, 1):
            md.append(f"{i}. {sug}")
        md.append("")
    else:
        md.append("## 五、提示词改进建议\n")
        md.append("所有样本均通过评估，当前提示词表现良好。\n")
    
    # 6. 附录
    md.append("## 六、附录\n")
    md.append(f"- 原始 JSON 报告：`{json_path}`")
    md.append("- 本报告由 `generate_markdown_report.py` 自动生成\n")
    
    return "\n".join(md)


if __name__ == "__main__":
    # 生成 Markdown 报告
    markdown_content = generate_markdown_report()
    
    # 保存到 outputs 目录
    output_path = Path("outputs/eval_report.md")
    output_path.write_text(markdown_content, encoding="utf-8")
    
    print(f"✅ Markdown 报告已生成：{output_path.absolute()}")
    print(f"   文件大小：{len(markdown_content)} 字符")