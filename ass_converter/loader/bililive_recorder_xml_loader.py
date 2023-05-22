import pandas
from loader.base_loader import BaseLoader
from filter.danmu_filter import DanmuFilter
from log.logger import Logger


class BililiveRecorderXMLLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        dom_tree = analysing_data
        danmus = dom_tree.getElementsByTagName("d")  # 弹幕
        recorder_info = dom_tree.getElementsByTagName("BililiveRecorderRecordInfo")
        assert len(recorder_info) == 1

        start_time_arr = recorder_info[0].getAttribute("start_time").split("+")  # 时间 + 时区
        user_name = recorder_info[0].getAttribute("name")
        user_title = recorder_info[0].getAttribute("title")
        self._dst_danmu_data["dst_file_name"] = \
            f"{user_name} {user_title}.ass"
        self._dst_danmu_data["start_time"] = \
            pandas.to_datetime(
                start_time_arr[0],
                utc=False,
                format="%Y-%m-%dT%H:%M:%S.%f"
            ).tz_localize('Asia/Shanghai').timestamp()

        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            danmu_text = danmu.firstChild.data
            if DanmuFilter.filter_check(danmu_text):
                danmu_time_text = danmu.getAttribute("p")
                danmu_time = float(danmu_time_text.split(",", 1)[0])
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        "text": DanmuFilter.filter_sub(danmu_text)
                    }
                )
