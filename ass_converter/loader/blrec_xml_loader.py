import re
import time
from loader.base_loader import BaseLoader
from filter.danmu_filter import DanmuFilter
from log.logger import Logger


class BlrecXMLLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data

        user_name = dom_tree.getElementsByTagName("user_name")[0].firstChild.data
        room_title = dom_tree.getElementsByTagName("room_title")[0].firstChild.data
        live_start_time_str = dom_tree.getElementsByTagName("live_start_time")
        record_start_time_str = dom_tree.getElementsByTagName("record_start_time")
        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {room_title}.ass"
        self._dst_danmu_data["start_time"] = int(
            time.mktime(time.strptime(
                re.sub(r"\+.*", "", live_start_time_str[0].firstChild.data), "%Y-%m-%dT%H:%M:%S")))
        record_start_time = int(
            time.mktime(time.strptime(
                re.sub(r"\+.*", "", record_start_time_str[0].firstChild.data), "%Y-%m-%dT%H:%M:%S")))
        danmus = dom_tree.getElementsByTagName("d")

        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            if len(danmu.getElementsByTagName("price")) != 0:
                continue
            danmu_text = danmu.firstChild.data
            danmu_time = float(danmu.getAttribute("p").split(",", 1)[0]) + \
                (record_start_time - self._dst_danmu_data["start_time"])  # 计算开播后的时间
            if DanmuFilter.filter_check(danmu_text):
                translate_man_name = danmu.getAttribute("user")
                danmu_text = danmu_text.replace(f"{translate_man_name}: ", "")  # blrec的弹幕会在文本内容里加上发送者名字
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        "text": DanmuFilter.filter_sub(danmu_text),
                        "prefix": DanmuFilter.filter_get_danmu_prefix(danmu_text)
                    }
                )
