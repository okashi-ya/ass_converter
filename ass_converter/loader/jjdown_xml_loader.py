import re
import time
from loader.base_loader import BaseLoader
from filter.danmu_filter import DanmuFilter
from log.logger import Logger


class JJDownXMLLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data

        file_name_data = re.split("[-.(]", self._src_file_name)
        assert (len(file_name_data) >= 5)  # XXX - n.XXX(AvXXX,PX).xml
        user_name = "【未知用户】"  # 唧唧Down的所有信息都不包含用户名 只能填空
        user_title = file_name_data[2]

        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {user_title}.ass"
        self._dst_danmu_data["start_time"] = 0  # 唧唧Down也不包含时间信息 填0

        danmus = dom_tree.getElementsByTagName("d")
        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            # 这个xml缺失的内容特别多 SC和礼物无法区分 直接全体遍历
            danmu_text = danmu.firstChild.data
            danmu_time_text = danmu.getAttribute("p")
            danmu_time = float(danmu_time_text.split(",", 1)[0])
            if DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        "text": DanmuFilter.filter_sub(danmu_text),
                        "prefix": DanmuFilter.filter_get_danmu_prefix(danmu_text)
                    }
                )
