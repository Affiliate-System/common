from distutils.command.config import config
import logging
from datetime import datetime

from config import config


formatter = logging.Formatter(f'[%(levelname)s] %(pathname)s: %(funcName)s():%(lineno)d \n%(asctime)s : %(message)s')
InfoLogger = logging.getLogger('info logger')
InfoLogger.setLevel(logging.INFO)
info_file_handler = logging.FileHandler(config.INFO_LOGDIR)
info_file_handler.setFormatter(formatter)
InfoLogger.addHandler(info_file_handler)

formatter = logging.Formatter(f'[%(levelname)s] %(pathname)s: %(funcName)s():%(lineno)d \n%(asctime)s : %(message)s')
ErrorLogger = logging.getLogger('error logger')
ErrorLogger.setLevel(logging.ERROR)
error_file_handler = logging.FileHandler(config.ERROR_LOGDIR)
error_file_handler.setFormatter(formatter)
ErrorLogger.addHandler(error_file_handler)