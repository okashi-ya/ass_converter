import json
import re
import xml.etree.ElementTree
import xml.dom.minidom
import enum
from loader.base_loader import BaseLoader
from loader.bililive_recorder_xml_loader import BililiveRecorderXMLLoader
from loader.matsuri_icu_json_loader import MatsuriICUJSONLoader
from loader.matsuri_icu_xml_loader import MatsuriICUXmlLoader
from loader.danmakus_json_loader import DanmakusJSONLoader
from loader.danmakus_xml_loader import DanmakusXMLLoader
from loader.blrec_xml_loader import BlrecXMLLoader
from loader.jjdown_xml_loader import JJDownXMLLoader
from loader.oksy_xml_loader import OksyXMLLoader
from log.logger import Logger


class LoaderType(enum.IntEnum):
    LOADER_TYPE_INVALID = 0  # 未知
    LOADER_TYPE_BILILIVE_RECORDER_XML = 1   # 录播姬的xml
    LOADER_TYPE_MATSURI_ICU_JSON = 2        # MatsuriICU的Json
    LOADER_TYPE_MATSURI_ICU_XML = 3         # MatsuriICU的xml
    LOADER_TYPE_DANMAKUS_JSON = 4           # Danmakus的json
    LOADER_TYPE_DANMAKUS_XML = 5            # Danmakus的xml
    LOADER_TYPE_BLREC_XML = 6               # blrec录播工具的xml
    LOADER_TYPE_JJDOWN_XML = 7              # 唧唧Down下载工具的xml
    LOADER_TYPE_OKSY_XML = 8                # 使用oksy录制的xml


class LoaderFactory:
    @classmethod
    def create_loader(cls, src_file: str, danmu_data: str) -> BaseLoader | None:
        loader_data_dict = cls.__get_loader_data_type(src_file, danmu_data)
        Logger.info(f"已创建加载器 类型 : {loader_data_dict['type'].name}")
        match loader_data_dict["type"]:
            case LoaderType.LOADER_TYPE_BILILIVE_RECORDER_XML:
                return BililiveRecorderXMLLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_MATSURI_ICU_JSON:
                return MatsuriICUJSONLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_MATSURI_ICU_XML:
                return MatsuriICUXmlLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_DANMAKUS_JSON:
                return DanmakusJSONLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_DANMAKUS_XML:
                return DanmakusXMLLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_BLREC_XML:
                return BlrecXMLLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_JJDOWN_XML:
                return JJDownXMLLoader(src_file, loader_data_dict["data"])
            case LoaderType.LOADER_TYPE_OKSY_XML:
                return OksyXMLLoader(src_file, loader_data_dict["data"])
        Logger.error(f"无法获取 {src_file} 的加载器类型 !")
        return None

    @classmethod
    def __danmaku_xml_pre_handle(cls, danmu_data: str):
        # Danmakus的xml并不是标准的xml文件格式 需要再最开始预先处理一下
        # Tag中带数字无法正确被解析 后续看有没有其他办法
        is_danmaku_xml = False
        if danmu_data.find("<wordCloud>") != -1 and danmu_data.find("</wordCloud>") != -1:
            danmu_data = \
                danmu_data[:danmu_data.find("<wordCloud>")] + \
                danmu_data[danmu_data.find("</wordCloud>") + len("</wordCloud>"):]
            is_danmaku_xml = True
        if danmu_data.find("<onlineRank>") != -1 and danmu_data.find("</onlineRank>") != -1:
            danmu_data = \
                danmu_data[:danmu_data.find("<onlineRank>")] + \
                danmu_data[danmu_data.find("</onlineRank>") + len("</onlineRank>"):]
            is_danmaku_xml = True
        if is_danmaku_xml:
            danmu_data = f"<danmakus_root>{danmu_data}</danmakus_root>"
            Logger.warning("检测到Danmakus的xml弹幕。该文件不是标准的xml格式。已进行兼容性转换。")
        return danmu_data

    @classmethod
    def __get_loader_data_type(cls, src_file: str, danmu_data: str):
        danmu_data = cls.__danmaku_xml_pre_handle(danmu_data)

        try:
            # 判断是否为xml格式
            dom_tree = xml.dom.minidom.parseString(danmu_data)

            if len(dom_tree.getElementsByTagName("BililiveRecorder")) != 0:
                # 有BililiveRecorder的为录播姬弹幕文件
                return {"type": LoaderType.LOADER_TYPE_BILILIVE_RECORDER_XML, "data": dom_tree}
            elif len(dom_tree.getElementsByTagName("danmakus")) != 0:
                # 有danmakus的为Danmakus弹幕文件
                return {"type": LoaderType.LOADER_TYPE_DANMAKUS_XML, "data": dom_tree}
            elif len(dom_tree.getElementsByTagName("recorder")) != 0 and \
                    str.find(dom_tree.getElementsByTagName("recorder")[0].firstChild.data, "blrec") != -1:
                # 有recorder且对应内容为blrec的弹幕文件
                return {"type": LoaderType.LOADER_TYPE_BLREC_XML, "data": dom_tree}
            elif len(dom_tree.getElementsByTagName("creator_info")) != 0:
                # 有creator_info的为oksy格式弹幕文件
                return {"type": LoaderType.LOADER_TYPE_OKSY_XML, "data": dom_tree}
            else:
                # Matsuri和唧唧Down的弹幕文件几乎没有特征 直接放在else里
                # 它们依赖文件名做判断

                # 唧唧Down的文件名结尾会有(AvXXXX,P?)的字样
                if re.search(r"(\(Av[0-9]*,P[0-9]*\))", src_file) is not None:
                    return {"type": LoaderType.LOADER_TYPE_JJDOWN_XML, "data": dom_tree}
                else:
                    return {"type": LoaderType.LOADER_TYPE_MATSURI_ICU_XML, "data": dom_tree}
        except xml.parsers.expat.ExpatError:
            # 判断是否为json格式
            try:
                json_data = json.loads(danmu_data)

                if len(json_data) == 2 and json_data.get("full_comments") is not None:
                    # 有2个字段 且有一个为full_comments的为MatsuriICU的json弹幕
                    return {"type": LoaderType.LOADER_TYPE_MATSURI_ICU_JSON, "data": json_data}
                elif len(json_data) == 3 and json_data.get("danmakus") is not None:
                    # 有3个字段 且有一个为danmakus的为Danmakus的json弹幕
                    return {"type": LoaderType.LOADER_TYPE_DANMAKUS_JSON, "data": json_data}
                else:
                    # 未知json
                    return {"type": LoaderType.LOADER_TYPE_INVALID, "data": None}
            except json.decoder.JSONDecodeError:
                return {"type": LoaderType.LOADER_TYPE_INVALID, "data": None}
