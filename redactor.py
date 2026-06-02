
"""
敏感信息脱敏模块
使用正则表达式识别并替换手机号、API Key 等敏感信息
"""

import re

# 匹配中国大陆手机号的正则表达式
PHONE_RE = re.compile(r"1[3-9]\d{9}")

# 匹配 API Key 格式的正则表达式（以 sk- 开头）
API_KEY_RE = re.compile(r"sk-[A-Za-z0-9_-]+")


def redact_sensitive(text: str) -> str:
    """
    对文本中的敏感信息进行脱敏处理
    
    Args:
        text: 原始文本
        
    Returns:
        脱敏后的文本，手机号替换为 [PHONE]，API Key 替换为 [API_KEY]
    """
    text = PHONE_RE.sub("[PHONE]", text)
    text = API_KEY_RE.sub("[API_KEY]", text)
    return text


# 模块自测代码
if __name__ == "__main__":
    test_text = "客户手机号是 13812345678，密钥是 sk-test-123456"
    result = redact_sensitive(test_text)
    print(f"原始文本: {test_text}")
    print(f"脱敏后: {result}")
    # 期望输出: 客户手机号是 [PHONE]，密钥是 [API_KEY]