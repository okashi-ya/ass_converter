from abc import ABC, abstractmethod

'''
_dst_danmu_data 结构：
{
    "src_file_name": str,   # 默认填充
    "dst_file_name": str,
    "start_time": float,
    "data": [
        { "time": float, "text": str, "prefix": str }...
    ]
}
'''


# 基本读取类
class BaseLoader(ABC):

    def __init__(self, src_file_name, analysing_data):
        self._src_file_name = src_file_name
        self._dst_danmu_data = {
            "src_file_name": self._src_file_name,   # 有些弹幕内没有直播信息 需要原文件名来提供
            "data": [],
        }
        self._data_analyse_handle(analysing_data)

    # 获取通用弹幕结构
    def get_danmu_data(self):
        return self._dst_danmu_data

    # 数据处理
    # analysing_data 解析中的数据 为xml.dom.minidom.Document类型 或
    @abstractmethod
    def _data_analyse_handle(self, analysing_data):
        pass

    _src_file_name: str
    _dst_file_name: str
    _dst_danmu_data: dict
