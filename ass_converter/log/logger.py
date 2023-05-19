import datetime
import os.path

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
        raise

    @classmethod
    def __out_log(cls, log_level, log):
        if not os.path.exists(AssConverterConfig.LogDir):
            os.makedirs(AssConverterConfig.LogDir)
        log_str = f"[{log_level}]{log}"
        f = open(f"{AssConverterConfig.LogDir}{g_log_file_name}", "ab+")
        f.write((log_str + "\n").encode("utf-8"))
        f.close()
        print(log_str)

    @classmethod
    def get_log_file_name(cls):
        return g_log_file_name
