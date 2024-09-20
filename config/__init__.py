import logging
import os
from datetime import datetime

import pytz

from config.settings import LOG_DIR

shanghai_tz = pytz.timezone('Asia/Shanghai')


class ShanghaiFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, shanghai_tz)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            s = dt.strftime('%Y-%m-%d %H:%M:%S')
        return s


Format = ("%(asctime)s - %(filename)s - line:%(lineno)d - %(funcName)s - %("
          "levelname)s - %(message)s")


class Log:
    def __init__(self, name):
        self.name = name
        if self.name != 'tmp' and self.name is None:
            self.name = 'tmp'
        # 获取logger实例
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        # 设置存储目录, 用于写入日志文件
        log_dir_path = LOG_DIR
        print(log_dir_path)
        if not os.path.exists(log_dir_path):
            os.makedirs(log_dir_path)

        log_file_path = log_dir_path + "/" + self.name + ".log"
        print(log_file_path)
        log_path = logging.FileHandler(log_file_path, encoding='utf-8')
        # 设置终端打印的日志, 用于打印到控制台
        console = logging.StreamHandler()
        # 设置终端打印的级别
        console.setLevel(logging.INFO)

        # 设置打印的格式
        formatter = ShanghaiFormatter(Format)

        # 为终端打印以及日志打印中加上格式
        console.setFormatter(formatter)
        log_path.setFormatter(formatter)

        # 将文件日志加入日志集中
        self.logger.addHandler(console)
        self.logger.addHandler(log_path)

    def log(self):
        # 设置文件中存储的日志级别
        return self.logger
