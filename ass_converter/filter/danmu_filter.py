import re
from config import AssConverterConfig

pattern_str = ""
for i in range(0, len(AssConverterConfig.DanmuFilters)):
    pattern_str += f"({AssConverterConfig.DanmuFilters[i]})"
    if i != len(AssConverterConfig.DanmuFilters) - 1:
        pattern_str += "|"
pattern = re.compile(f"{pattern_str}")


# 弹幕过滤器
class DanmuFilter:
    @classmethod
    def filter_check(cls, text: str) -> bool:
        return pattern.search(text) is not None
