SELECTED_UNIVERSITY = "清华大学_test"

import os
CONFIG = {
    "UNIVERSITY_NAME": SELECTED_UNIVERSITY,
    "SPECIFIED_LETTERS" :[],# 搜索全部：[],搜索特定：['D', 'H']
    "SPECIFIED_COLLEGES": [],  # 搜索全部：[],搜索特定：['生命学院', '农学院']
    "DRIVER_PATH": os.environ.get("DRIVER_PATH", "C:/ProgramData/Anaconda3/chromedriver.exe"),
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "PORT": int(os.environ.get("DB_PORT", 27017)),
    "DATABASE_NAME": os.environ.get("DB_NAME", "faculty_db"),
    "COLLECTION_NAME": SELECTED_UNIVERSITY+"_teacher_info",
    "LETTERS" : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    "USER_AGENT": os.environ.get("USER_AGENT",
                                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
}

from configs.nwafu_university_config import NWAFU_UNIVERSITY
from configs.thu_university_config import THU_UNIVERSITY

UNIVERSITIES = {
    '华中科技大学_test': {
        'module': 'hust_scraper',
        'class': 'HUSTScraper'
    },
    '中南大学': {
        'module': 'csu_scraper',
        'class': 'CSUScraper'
    },
    '中国科学技术大学': {
        'module': 'ustc_scraper',
        'class': 'USTCScraper'
    },
    '西安交通大学': {
        'module': 'xjtu_scraper',
        'class': 'XJTUScraper'
    },
    '大连理工大学': {
        'module': 'dut_scraper',
        'class': 'DUTScraper'
    },
    '电子科技大学': {
        'module': 'uestc_scraper',
        'class': 'UESTCScraper'
    },
    '华东师范大学': {
        'module': 'ecnu_scraper',
        'class': 'ECNUScraper'
    },
    '中国农业大学': {
        'module': 'cau_scraper',
        'class': 'CAUScraper'
    },
    NWAFU_UNIVERSITY['name']: NWAFU_UNIVERSITY,
    THU_UNIVERSITY['name']: THU_UNIVERSITY,
}
#为函数动态添加相应的模块和类名
#例如：当SELECTED_UNIVERSITY = "华中科技大学"时，from hust_scraper import HUSTScraper
import importlib
def get_selected_university_scraper():
    module_name = 'scrapers.' + UNIVERSITIES[SELECTED_UNIVERSITY]['module']  # 注意添加正确的包路径
    class_name = UNIVERSITIES[SELECTED_UNIVERSITY]['class']
    module = importlib.import_module(module_name, package='scrapers')  # 提供 'package' 参数
    scraper_class = getattr(module, class_name)
    return scraper_class

