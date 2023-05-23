import os
from config import AssConverterConfig
from log.logger import Logger

class DanmuFileReaderData:
    src_file_name: str
    src_file_data: str


class DanmuFileReader:
    def __init__(self):
        self.data = []

    def load_all_file(self):
        root_dir = AssConverterConfig.input_dir
        for dir_path, dir_name, file_name_array in os.walk(root_dir):
            # 不遍历子文件夹
            for file_name in file_name_array:
                file_data = DanmuFileReaderData()
                file_data.src_file_name = file_name
                f = open(os.path.join(AssConverterConfig.input_dir, file_data.src_file_name), "r", encoding="utf-8")
                file_data.src_file_data = f.read()
                self.data.append(file_data)
                f.close()
                Logger.info(f"添加待解析文件： {file_name}")
            break

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        ret = self.data[self.index]
        self.index += 1
        return ret

    data: [DanmuFileReaderData]
    index: int
