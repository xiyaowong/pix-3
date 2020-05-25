import json
import os
from datetime import datetime

import requests

import config
import utils


def get_tasks() -> list:
    files = os.listdir(config.PARSE_TASK_DIR)
    if 'example' in files:
        files.remove('example')
    if files:
        return files
    now = datetime.now()
    date = f'{now.year}-{now.month:0>2}-{now.day-5:0>2}'
    return [date]


@utils.retry(1)
def parse(date):
    print(f'[PAESE]{date}')
    api = f"https://api.pixivic.com/ranks?page=1&date={date}&mode=day&pageSize=1000"

    rep = requests.get(api, headers=config.HEADERS, timeout=10)
    data = rep.json().get('data')  # type: list
    if not '获取排行成功' in rep.text or data is None or len(data) == 0:
        print(f'没获取到{date}这天的数据')
        return None
    with open(os.path.join(config.DL_TASK_DIR, f'{date}.json'), 'w') as f:
        json.dump(data, f)
    utils.remove_file(os.path.join(config.PARSE_TASK_DIR, date))
    return None


def main():
    tasks = get_tasks()
    for task in tasks:
        parse(task)


if __name__ == "__main__":
    print(get_tasks())
    main()
