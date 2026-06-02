
"""
输出格式自动检查模块
对模型输出进行基础的格式检查，包括栏目完整性、长度和禁用内容
"""

from rubric import REQUIRED_SECTIONS


def check_required_sections(output: str) -> list[str]:
    """
    检查输出是否包含所有必需的栏目
    
    Args:
        output: 模型输出的文本
        
    Returns:
        错误信息列表，空列表表示检查通过
    """
    errors = []
    for section in REQUIRED_SECTIONS:
        if section not in output:
            errors.append(f"missing section: {section}")
    return errors


def check_min_length(output: str, min_chars: int = 40) -> list[str]:
    """
    检查输出文本是否达到最小长度要求
    
    Args:
        output: 模型输出的文本
        min_chars: 最小字符数要求
        
    Returns:
        错误信息列表，空列表表示检查通过
    """
    if len(output.strip()) < min_chars:
        return ["output is too short"]
    return []


def check_forbidden_points(output: str, forbidden_points: list[str]) -> list[str]:
    """
    检查输出中是否包含禁止出现的内容
    
    Args:
        output: 模型输出的文本
        forbidden_points: 禁止出现的关键词列表
        
    Returns:
        错误信息列表，空列表表示检查通过
    """
    errors = []
    for phrase in forbidden_points:
        if phrase in output:
            errors.append(f"forbidden phrase appears: {phrase}")
    return errors


def run_static_checks(output: str, forbidden_points: list[str]) -> list[str]:
    """
    执行所有静态检查
    
    Args:
        output: 模型输出的文本
        forbidden_points: 禁止出现的关键词列表
        
    Returns:
        所有检查的错误信息列表
    """
    errors = []
    errors.extend(check_required_sections(output))
    errors.extend(check_min_length(output))
    errors.extend(check_forbidden_points(output, forbidden_points))
    return errors


# 模块自测代码
if __name__ == "__main__":
    # 测试一个好输出
    good_output = """回复正文：
非常抱歉给您带来不便。当前事项我们已经记录。

注意事项：
- 发送前确认具体原因。"""
    
    print("测试好输出:")
    print(run_static_checks(good_output, ["承诺赔偿"]))
    
    # 测试一个坏输出
    bad_output = """我们会全额退款。"""
    
    print("\n测试坏输出:")
    print(run_static_checks(bad_output, ["全额退款", "承诺赔偿"]))