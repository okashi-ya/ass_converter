import copy
import datetime
import re
import numpy
from config import AssConverterConfig
from log.logger import Logger

'''
writer_danmu_data 结构：
    {
        dst_file_name: {
            "start_time": float
            "data" = {
                ... = {...}, # key = 弹幕前缀，用于多人同传标识不同人的弹幕 value = 弹幕数据
                ...
            }
        }
    }...
'''


# ass
class AssWriter:
    def __init__(self):
        self.writer_danmu_data = dict()

    def add_danmu_data(self, danmu_data):
        # 添加从Loader.get_danmu_data()返回的弹幕数据
        danmu_data_this_file = self.writer_danmu_data.get(danmu_data["dst_file_name"])
        if danmu_data_this_file is None:
            # 还没有该文件的记录
            self.writer_danmu_data[danmu_data["dst_file_name"]] = dict()
            self.writer_danmu_data[danmu_data["dst_file_name"]]["start_time"] = danmu_data["start_time"]
            self.writer_danmu_data[danmu_data["dst_file_name"]]["data"] = danmu_data["data"]
        else:
            # 比较时间
            time_this_file = danmu_data_this_file["start_time"]
            time_danmu_data = danmu_data["start_time"]
            offset = abs(time_this_file - time_danmu_data)
            if time_this_file > time_danmu_data:
                # 已有记录中的时间更大 说明已有记录更靠后 需要将已有记录中所有时间增大offset
                for single_data in danmu_data_this_file["data"]:
                    single_data["time"] = round(single_data["time"] + offset, 2)  # 保留两位小数
            elif time_this_file < time_danmu_data:
                # 参数传递进来的时间更大 说明已有纪录更靠前 需要将参数传递进来的所有时间增大offset
                # 拷贝一份 不影响源数据
                dc_danmu_data = copy.deepcopy(danmu_data)
                for single_data in dc_danmu_data["data"]:
                    single_data["time"] = round(single_data["time"] + offset, 2)  # 保留两位小数
                danmu_data = dc_danmu_data
            # 合并
            danmu_data_this_file["data"] = numpy.hstack((danmu_data_this_file["data"], danmu_data["data"]))

    def write(self):
        ass_head = self.__get_ass_head()

        cur_index = 1
        # 将所有弹幕数据写入到文件中
        for file_name, file_data in self.writer_danmu_data.items():
            Logger.info(f"开始写入弹幕文件，共计{len(self.writer_danmu_data)}个，当前写入第{cur_index}个")
            cp_file_data = copy.deepcopy(file_data["data"])

            sorted_file_data = sorted(cp_file_data, key=lambda x: x["time"])  # 按时间排序

            # 同传给每个人的弹幕应该独立计算间隔时间
            pre_prefix_index_dict = {}
            for i in range(0, len(sorted_file_data)):
                prefix = sorted_file_data[i]["prefix"]
                sorted_file_data[i]["time_final"] = sorted_file_data[i]["time"] + 10  # 10s间隔
                if pre_prefix_index_dict.get(prefix) is not None:
                    # 有值说明是上一次设置的 判断时间间隔
                    pre_prefix_time_final = sorted_file_data[pre_prefix_index_dict[prefix]]["time_final"]
                    if pre_prefix_time_final > sorted_file_data[i]["time"]:
                        # 说明上一次的时间结尾已经比这次的时间开始要大 需要修改上一次的时间结尾
                        sorted_file_data[pre_prefix_index_dict[prefix]]["time_final"] = sorted_file_data[i]["time"]
                # 更新这个索引值
                pre_prefix_index_dict[prefix] = i

            # 时间字符串
            if file_data["start_time"] == 0:
                Logger.warning("start_time时间无效。")
                time_ymd = "【未知时间】"
            else:
                time_ymd = datetime.datetime.fromtimestamp(file_data["start_time"]).strftime("%Y-%m-%d")
            f = open(f"{AssConverterConfig.output_dir}ass_converter {time_ymd} {file_name}", "wb")
            f.write(ass_head.encode("utf-8"))

            for single_danmu_data in sorted_file_data:
                # 下一个弹幕的开始时间
                f.write(self.__single_danmu_data_to_ass_line(single_danmu_data))
            f.close()

            cur_index += 1

    @classmethod
    def __get_ass_head(cls):
        ass_head = ""
        ass_head += "[Script Info]\n"
        ass_head += "; Script generated by Aegisub 3.2.2\n"
        ass_head += "; http://www.aegisub.org/\n"
        ass_head += "Title: Default Aegisub file\n"
        ass_head += "ScriptType: v4.00+\n"
        ass_head += "WrapStyle: 0\n"
        ass_head += "ScaledBorderAndShadow: yes\n"
        ass_head += "YCbCr Matrix: None\n"
        ass_head += "\n"
        ass_head += "[Aegisub Project Garbage]\n"
        ass_head += "Last Style Storage: Default\n"
        ass_head += "\n"
        if len(AssConverterConfig.ass_style) != 0:
            ass_head += "[V4+ Styles]\n"
            ass_head += "Format: Name, Fontname, Fontsize, PrimaryColour, " \
                        "SecondaryColour, OutlineColour, BackColour, " \
                        "Bold, Italic, Underline, StrikeOut, ScaleX, " \
                        "ScaleY, Spacing, Angle, BorderStyle, Outline, " \
                        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            for _, single_style in AssConverterConfig.ass_style.items():
                ass_head += "Style: "
                ass_head += f"{single_style['style']}\n"
            ass_head += "\n"
        ass_head += "[Events]\n"
        ass_head += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        return ass_head

    @classmethod
    def __single_danmu_data_to_ass_line(cls, single_data):
        # 单个弹幕数据转换成ass的一行数据
        time_s = single_data["time"]
        next_time_s = single_data["time_final"]
        time_str_start = cls.__get_ass_time_str(time_s)
        time_str_end = cls.__get_ass_time_str(next_time_s)
        style = "Default"

        prefix = re.sub(r"\W", "", single_data["prefix"])   # 转发同传会加一个特殊符号 这个符号一般来说是可以用\W过滤的
        text = re.sub(r"\W", "", single_data["text"])
        if AssConverterConfig.ass_style.get(prefix) is not None:
            style = AssConverterConfig.ass_style[prefix]["ass_style_name"]   # 填字幕的名字
        else:
            # 如果找不到样式 就把prefix加到最前面 避免出现大批量default还找不到同传目标的问题
            text = f"{prefix} {text}"
        return f"Dialogue: 0,{time_str_start},{time_str_end},{style},,0,0,0,,{text}\n".encode("utf-8")

    @classmethod
    def __get_ass_time_str(cls, time_ms):
        ms = int(time_ms * 100 % 100)
        minute, sec = divmod(time_ms, 60)
        hour, minute = divmod(minute, 60)
        return "%d:%02d:%02d.%02d" % (hour, minute, sec, ms)

    writer_danmu_data: dict
