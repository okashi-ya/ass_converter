import traceback

from loader.loader_factory import LoaderFactory
from ass_io.danmu_file_reader import DanmuFileReader
from ass_io.ass_writer import AssWriter
from log.logger import Logger
from config import AssConverterConfig
from utils.utils import Utils


def main():
    try:
        Logger.info(f"ass_converter {Utils.get_version()}")
        Logger.info("Designed by 古守のお菓子屋")
        Logger.info("个人主页 https://space.bilibili.com/253052708")
        Logger.info("ass_converter 转换开始.")
        danmu_reader = DanmuFileReader()  # 弹幕文件的reader
        danmu_reader.load_all_file()
        ass_writer = AssWriter()  # ass的writer
        for all_file in iter(danmu_reader):
            record_loader = LoaderFactory.create_loader(all_file.src_file_name, all_file.src_file_data)
            if record_loader is not None:
                ass_writer.add_danmu_data(record_loader.get_danmu_data())
        ass_writer.write()
        Logger.info("ass_converter 转换已完成.")
        Logger.info(f"输出文件目录：{AssConverterConfig.OutputDir}")
    except ...:
        # 抛出异常，打印fatal
        Logger.fatal(traceback.format_exc())
        Logger.info("ass_converter 转换失败.详细信息请查看日志.")


if __name__ == "__main__":
    main()
