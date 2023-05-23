import datetime
import os.path
import sys

from config import AssConverterConfig

g_log_file_name = datetime.datetime.now().strftime("LOG %Y-%m-%d %H-%M-%S.log")


class Logger:
    @classmethod
    def debug(cls, log):
        return cls.__out_log("Debug", log)

    @classmethod
    def info(cls, log):
        return cls.__out_log("Info", log)

    @classmethod
    def warning(cls, log):
        return cls.__out_log("Warning", log)

    @classmethod
    def error(cls, log):
        return cls.__out_log("Error", log)

    @classmethod
    def fatal(cls, log):
        cls.__out_log("Fatal", log)

    @classmethod
    def __out_log(cls, log_level, log):
        if not os.path.exists(AssConverterConfig.log_dir):
            os.makedirs(AssConverterConfig.log_dir)
        log_str = f"[{log_level}]{log}"
        f = open(f"{AssConverterConfig.log_dir}{g_log_file_name}", "ab+")
        f.write((log_str + "\n").encode("utf-8"))
        f.close()
        match log_level:
            case "Debug":
                pass
            case "Error" | "Fatal":
                print(log_str, file=sys.stderr)
            case _:
                print(log_str)

    @classmethod
    def get_log_file_name(cls):
        return g_log_file_name
