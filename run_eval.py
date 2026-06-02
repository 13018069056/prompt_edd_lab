# -*- coding: utf-8 -*-
"""
批量评估主脚本
串联样本集、目标系统、评估器和错误分析模块，
生成完整的 JSON 评估报告
"""

import json
from pathlib import Path

from evaluators import evaluate_case
from samples import SAMPLES
from target_system import target_answer
from error_analysis import summarize_failures, suggest_prompt_changes


def summarize(results: list[dict]) -> dict:
    """
    生成评估结果摘要
    
    Args:
        results: 所有样本的评估结果列表
        
    Returns:
        包含总数、通过数和分类统计的摘要字典
    """
    total = len(results)
    passed = sum(1 for item in results if item["passed"])
    
    # 按类别统计
    by_type = {}
    for item in results:
        stat = by_type.setdefault(item["category"], {"total": 0, "passed": 0})
        stat["total"] += 1
        stat["passed"] += int(item["passed"])
    
    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4) if total else 0,
        "by_type": by_type,
    }


def main() -> None:
    """
    主函数：执行批量评估流程
    """
    # 1. 对所有样本进行评估
    results = []
    for sample in SAMPLES:
        output = target_answer(sample["user_input"])
        results.append(evaluate_case(sample, output))

    # 2. 生成摘要统计
    report_summary = summarize(results)
    
    # 3. 进行错误分析
    failure_summary = summarize_failures(results)
    improvement_suggestions = suggest_prompt_changes(failure_summary)

    # 4. 构建完整报告
    report = {
        "summary": report_summary,
        "failure_analysis": failure_summary,
        "improvement_suggestions": improvement_suggestions,
        "results": results,
    }

    # 5. 保存报告到文件
    Path("outputs").mkdir(exist_ok=True)
    report_path = Path("outputs/eval_report.json")
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 6. 打印控制台输出
    print("=" * 60)
    print("评估报告摘要")
    print("=" * 60)
    print(json.dumps(report_summary, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("错误分析摘要")
    print("=" * 60)
    print(json.dumps(failure_summary, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("提示词改进建议")
    print("=" * 60)
    for i, sug in enumerate(improvement_suggestions, 1):
        print(f"{i}. {sug}")
    
    print(f"\n完整报告已保存到: {report_path.absolute()}")


if __name__ == "__main__":
    main()