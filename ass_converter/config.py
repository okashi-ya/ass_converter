import os
import yaml

class AssConverterConfig:
    input_dir = f"{os.getcwd()}\\danmu\\"
    output_dir = f"{os.getcwd()}\\out\\"
    matsuriicu_full_danmu = True  # MatsuriICU完整弹幕 如果只是同传弹幕需要把这里改成False再运行
    log_dir = f"{os.getcwd()}\\out\\Log\\"
    ass_style = {}

    @classmethod
    def load_user_config(cls):
        with open(f"{os.getcwd()}\\ass_converter_config.yaml", "r", encoding="utf8") as f:
            user_config = yaml.safe_load(f)

            for prefix, single_style in user_config["ass_style"].items():
                AssConverterConfig.ass_style[str(prefix)] = {   # prefix 如果是纯数字之类的就需要转换一下
                    "ass_style_name": single_style.split(",")[0],
                    "style": single_style}
            cls.matsuriicu_full_danmu = user_config["matsuriicu_full_danmu"]
