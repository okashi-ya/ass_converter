import re


# 弹幕过滤器
class DanmuFilter:
    @classmethod
    def filter_check(cls, text: str) -> bool:
        return re.match(r".{0,4}【", text) is not None

    @classmethod
    def filter_sub(cls, text: str):
        if text[0] != "【":
            # 同传弹幕格式前有内容
            text = re.sub(r"\w*【", "", text)
        return re.sub("[【】]", "", text)

    @classmethod
    def filter_get_danmu_prefix(cls, text: str):
        return text[0:text.find("【")]
