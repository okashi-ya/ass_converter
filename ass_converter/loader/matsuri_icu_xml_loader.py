import re
from loader.base_loader import BaseLoader
from config import AssConverterConfig
from filter.danmu_filter import DanmuFilter
from log.logger import Logger

class MatsuriICUXmlLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data

        # xml内没有直播开始时间的信息 需要从文件名去获取
        file_name_data = re.split("[_.]", self._src_file_name)
        assert(len(file_name_data) >= 4)    # XXX_XXX_XXX.xml
        user_name = file_name_data[0]
        user_title = ""
        for i in range(1, len(file_name_data) - 2):
            user_title += f"_{file_name_data[i]}"

        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {user_title}.ass"
        self._dst_danmu_data["start_time"] = int(file_name_data[-2]) / 1e3

        danmus = dom_tree.getElementsByTagName("d")
        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            # 这个xml缺失的内容特别多 SC和礼物无法区分 直接全体遍历
            danmu_text = danmu.firstChild.data
            danmu_time_text = danmu.getAttribute("p")
            danmu_time = float(danmu_time_text.split(",", 1)[0])
            if not AssConverterConfig.MatsuriICUFullDanmu or DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        # 完整弹幕则主动筛选出同传弹幕 否则直接将所有弹幕接入
                        "text": DanmuFilter.filter_sub(danmu_text)
                    }
                )