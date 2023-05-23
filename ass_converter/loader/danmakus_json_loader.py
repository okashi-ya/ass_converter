from loader.base_loader import BaseLoader
from filter.danmu_filter import DanmuFilter
from log.logger import Logger


class DanmakusJSONLoader(BaseLoader):
    def _data_analyse_handle(self, analysing_data):
        json_dict = analysing_data
        channel_info = json_dict["channel"]
        danmus = json_dict["danmakus"]
        self._dst_danmu_data["dst_file_name"] = f"{channel_info['uName']} {channel_info['title']}.ass"
        self._dst_danmu_data["start_time"] = int(json_dict["live"]["startDate"]) / 1e3

        Logger.debug(f"src_file_name = {self._dst_danmu_data['src_file_name']} danmu_count = {len(danmus)}")
        for danmu in danmus:
            if danmu.get("price") is not None:
                # 礼物 舰长 SC全都是
                continue
            assert danmu.get("ct") is not None  # 有ct这个字段
            # 有可能会有图片 不过过滤同传弹幕的话是肯定会过滤掉的
            danmu_text = danmu["message"]
            danmu_time = (int(danmu["sendDate"]) - int(json_dict["live"]["startDate"])) / 1e3  # 计算开播后的时间
            if DanmuFilter.filter_check(danmu_text):
                self._dst_danmu_data["data"].append(
                    {
                        "time": danmu_time,
                        # 完整弹幕则主动筛选出同传弹幕 否则直接将所有弹幕接入
                        "text": DanmuFilter.filter_sub(danmu_text),
                        "prefix": DanmuFilter.filter_get_danmu_prefix(danmu_text)
                    }
                )
