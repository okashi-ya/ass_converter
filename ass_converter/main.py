from loader.loader_factory import LoaderFactory
from ass_io.danmu_file_reader import DanmuFileReader
from ass_io.ass_writer import AssWriter
from log.logger import Logger
from config import AssConverterConfig


def main():
    Logger.info("ass_converter Designed by 古守のお菓子屋")
    Logger.info("https://space.bilibili.com/253052708")
    Logger.info("ass_converter 转换开始.")
    danmu_reader = DanmuFileReader()  # 弹幕文件的reader
    danmu_reader.load_all_file()
    ass_writer = AssWriter()  # ass的writer
    for all_file in iter(danmu_reader):
        record_loader = LoaderFactory.create_loader(all_file.src_file_name, all_file.src_file_data)
        ass_writer.add_danmu_data(record_loader.get_danmu_data())
    ass_writer.write()
    Logger.info("ass_converter 转换已成功完成.")
    Logger.info(f"输出文件目录：{AssConverterConfig.OutputDir}")


if __name__ == "__main__":
    main()
