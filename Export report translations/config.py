# API配置
BASE_URL = "http://saas.gpsnow.net/saas-pre/web/api"

# 登录配置
LOGIN_CONFIG = {
    "username": "swd",
    "password": "a123456",
    "timezone_second": 28800
}

# 支持的语言列表
LANGUAGE_LIST = [
    'en',    # 英语
    'zh-CN', # 简体中文
    'zh-TW', # 繁体中文
    'fr',    # 法语
    'ar',    # 阿拉伯语
    'vi',    # 越南语
    'es',    # 西班牙语
    'pt',    # 葡萄牙语
    'ru',    # 俄语
    'it',    # 意大利语
    'de',    # 德语
    'id',    # 印度尼西亚语
    'fa',    # 波斯语
    'bn',    # 孟加拉语
    'he',    # 希伯来语
    'nl',    # 荷兰语
    'tr',    # 土耳其语
    'geo',   # 格鲁吉亚语
    'pl',    # 波兰语
    'ro',    # 罗马尼亚语
    'sq',    # 阿尔巴尼亚语
    'lo',    # 老挝语
    'mn'     # 蒙古语
]

# 文件保存路径配置
import os
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
TRANSLATION_DIR = os.path.join(DESKTOP_PATH, "语言翻译")

# 请求头配置
DEFAULT_HEADERS = {
    'User-Agent': 'python-requests/2.31.0'
} 