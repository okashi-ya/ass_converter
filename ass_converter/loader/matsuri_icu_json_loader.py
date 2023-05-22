import re
from loader.base_loader import BaseLoader
from config import AssConverterConfig
from filter.danmu_filter import DanmuFilter


class MatsuriICUJSONLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        json_dict = analysing_data
        live_info = json_dict["info"]
        danmus = json_dict["full_comments"]
        self._dst_danmu_data["dst_file_name"] = f"{live_info['name']} {live_info['title']}.ass"
        self._dst_danmu_data["start_time"] = int(live_info["start_time"]) / 1e3

        for danmu in danmus:
            if danmu.get("gift_name") is not None or \
                    danmu.get("superchat_price") is not None:
                # 如果有gift_name字段说明是礼物弹幕
                # 如果有superchat_price字段说明是SC
                continue
            danmu_text = danmu["text"]
            danmu_time = (int(danmu["time"]) - live_info["start_time"]) / 1e3  # 计算开播后的时间
            if not AssConverterConfig.MatsuriICUFullDanmu or DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        # 完整弹幕则主动筛选出同传弹幕 否则直接将所有弹幕接入
                        "text": DanmuFilter.filter_sub(danmu_text) if AssConverterConfig.MatsuriICUFullDanmu else danmu_text
                    }
                )
