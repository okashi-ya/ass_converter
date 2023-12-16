import re
import datetime
from loader.base_loader import BaseLoader
from config import AssConverterConfig
from filter.danmu_filter import DanmuFilter
from log.logger import Logger


class OksyXMLLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data

        live_info_el = dom_tree.getElementsByTagName("live_info")[0]
        start_time = live_info_el.getElementsByTagName("start_time")[0].firstChild.data
        user_name = live_info_el.getElementsByTagName("uname")[0].firstChild.data
        user_title = live_info_el.getElementsByTagName("title")[0].firstChild.data

        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {user_title}.ass"
        self._dst_danmu_data["start_time"] = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp()

        danmus = dom_tree.getElementsByTagName("d")
        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            # 只保留弹幕
            if danmu.getAttribute("type") != "danmu":
                continue
            danmu_text = danmu.firstChild.data
            danmu_time_text = danmu.getAttribute("duration")
            re_groups = re.match(r"(\w*):(\w*):(\w*)", danmu_time_text).groups()
            danmu_time = int(re_groups[0]) * 3600 + int(re_groups[1]) * 60 + int(re_groups[2])
            if not AssConverterConfig.matsuriicu_full_danmu or DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        "text": DanmuFilter.filter_sub(danmu_text),
                        "prefix": DanmuFilter.filter_get_danmu_prefix(danmu_text)
                    }
                )
