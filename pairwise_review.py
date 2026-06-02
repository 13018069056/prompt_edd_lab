
"""
成对比较与人工评审模块
提供统一的比较模板，用于比较两个提示词版本的输出优劣
"""

# 成对比较的评审维度
PAIRWISE_CRITERIA = [
    "格式完整",
    "要点覆盖",
    "语气合适",
    "约束遵守",
    "安全稳健",
    "隐私保护",
]


def build_pairwise_review(sample_id: str, output_a: str, output_b: str) -> str:
    """
    构建成对比较评审模板
    
    Args:
        sample_id: 样本标识
        output_a: 版本A的输出
        output_b: 版本B的输出
        
    Returns:
        格式化的评审模板文本
    """
    criteria_text = "\n".join(f"- {item}" for item in PAIRWISE_CRITERIA)
    return f"""样本：{sample_id}

请比较输出 A 和输出 B：

比较维度：
{criteria_text}

输出 A：
{output_a}

输出 B：
{output_b}

评审结论：
- 更好的输出：
- 主要原因：
- 仍需改进：
"""


def quick_compare(output_a: str, output_b: str) -> dict:
    """
    快速自动比较两个输出的基础指标
    
    Args:
        output_a: 版本A的输出
        output_b: 版本B的输出
        
    Returns:
        基础比较结果字典
    """
    return {
        "a_length": len(output_a),
        "b_length": len(output_b),
        "a_has_reply": "回复正文" in output_a,
        "b_has_reply": "回复正文" in output_b,
        "a_has_note": "注意事项" in output_a,
        "b_has_note": "注意事项" in output_b,
    }