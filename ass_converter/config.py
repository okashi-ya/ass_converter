import os


class AssConverterConfig:
    InputDir = f"{os.getcwd()}\\danmu\\"
    OutputDir = f"{os.getcwd()}\\out\\"
    MatsuriICUFullDanmu = True  # MatsuriICU完整弹幕 如果只是同传弹幕需要把这里改成False再运行
    LogDir = f"{os.getcwd()}\\out\\Log\\"
