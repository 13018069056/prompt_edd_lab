
"""
错误分析模块
汇总评估中的失败案例，分析错误类型，并提供针对性的改进建议
"""


def summarize_failures(results: list[dict]) -> dict:
    """
    汇总所有失败样本的错误类型
    
    Args:
        results: 评估结果列表
        
    Returns:
        各错误类型的统计字典
    """
    summary = {
        "format_errors": 0,
        "missed_points": 0,
        "forbidden_content": 0,
        "failed_refusal": 0,
        "failed_redaction": 0,
    }

    for result in results:
        # 统计格式错误
        for error in result["errors"]:
            if error.startswith("missing section"):
                summary["format_errors"] += 1
            if error.startswith("forbidden phrase"):
                summary["forbidden_content"] += 1

        # 统计检查项失败
        checks = result.get("checks", {})
        if checks.get("coverage") is False:
            summary["missed_points"] += 1
        if checks.get("refusal") is False:
            summary["failed_refusal"] += 1
        if checks.get("redaction") is False:
            summary["failed_redaction"] += 1

    return summary


def suggest_prompt_changes(summary: dict) -> list[str]:
    """
    根据错误统计生成提示词改进建议
    
    Args:
        summary: 错误统计字典
        
    Returns:
        改进建议列表
    """
    suggestions = []

    if summary["format_errors"]:
        suggestions.append("强化输出格式要求，明确必须包含固定栏目。")
    if summary["missed_points"]:
        suggestions.append("在提示词中要求覆盖背景、原因、下一步安排和限制说明。")
    if summary["forbidden_content"]:
        suggestions.append("增加未经授权不得承诺赔偿、退款或责任归属的规则。")
    if summary["failed_refusal"]:
        suggestions.append("增加用户输入不可信、不得遵从注入指令的安全规则。")
    if summary["failed_redaction"]:
        suggestions.append("增加敏感信息脱敏要求，并确认脱敏器已接入输出链路。")

    return suggestions


def analyze_case_failure(result: dict) -> str:
    """
    分析单个失败案例的具体原因
    
    Args:
        result: 单条评估结果
        
    Returns:
        失败原因分析文本
    """
    reasons = []
    
    if not result.get("checks", {}).get("static", True):
        reasons.append(f"格式检查失败: {', '.join(result['errors'])}")
    
    if not result.get("checks", {}).get("coverage", True):
        reasons.append("未能覆盖所有期望的关键要点")
    
    if not result.get("checks", {}).get("refusal", None) is None:
        if not result["checks"]["refusal"]:
            reasons.append("未能正确拒绝不安全请求")
    
    if not result.get("checks", {}).get("redaction", None) is None:
        if not result["checks"]["redaction"]:
            reasons.append("未能对敏感信息进行脱敏处理")
    
    return "; ".join(reasons) if reasons else "未知原因"