import os

from utils import check_dir

HEADERS = {
    'referer': 'https://pixivic.com',
    'origin': 'https://pixivic.com',
    'accept': 'application/json',
    'cookie': '__cfduid=dacbdcb16ae9702ab2810464e338f605d1589024076; _ga=GA1.2.1792509931.1589024077; _gid=GA1.2.1486130353.1589024077',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"
}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

IMAGES_SAVE_DIR = os.path.join(BASE_DIR, 'pics')
PARSE_TASK_DIR = os.path.join(BASE_DIR, 'parse_tasks')
DL_TASK_DIR = os.path.join(BASE_DIR, 'dl_tasks')

ALREADY_SAVED_DATA_DIR = os.path.join(BASE_DIR, 'already_saved_data')

for i in [IMAGES_SAVE_DIR,
          PARSE_TASK_DIR,
          DL_TASK_DIR,
          ALREADY_SAVED_DATA_DIR]:
    check_dir(i)
