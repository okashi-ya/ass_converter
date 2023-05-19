import re
from loader.base_loader import BaseLoader
from config import AssConverterConfig
from filter.danmu_filter import DanmuFilter
from log.logger import Logger

class DanmakusXMLLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data.getElementsByTagName("tmp")[0]

        channel_info = dom_tree.getElementsByTagName("channel")[0]
        live_info = dom_tree.getElementsByTagName("live")[0]

        user_name = channel_info.getElementsByTagName("uName")[0].firstChild.data
        user_title = live_info.getElementsByTagName("title")[0].firstChild.data
        danmus = dom_tree.getElementsByTagName("danmakus")
        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {user_title}.ass"

        start_date = int(live_info.getElementsByTagName("startDate")[0].firstChild.data)
        self._dst_danmu_data["start_time"] = start_date / 1e3

        for danmu in danmus:

            if len(danmu.getElementsByTagName("price")) != 0:
                continue
            # 有可能会有图片 不过过滤同传弹幕的话是肯定会过滤掉的
            danmu_text = danmu.getElementsByTagName("message")[0].firstChild.data
            danmu_time = \
                (int(danmu.getElementsByTagName("sendDate")[0].firstChild.data) - start_date) / 1e3  # 计算开播后的时间
            if DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        # 完整弹幕则主动筛选出同传弹幕 否则直接将所有弹幕接入
                        "text": re.sub("[【】]", "", danmu_text) if AssConverterConfig.MatsuriICUFullDanmu else danmu_text
                    }
                )
