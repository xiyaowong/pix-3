import json
import os
from queue import Queue
from threading import Thread
from time import sleep
import random

import config
import utils

queue = Queue(maxsize=1000)


@utils.retry(2, 1)
def dl():
    # 其他仓库已下载，不再下载
    already_saved_data_files = os.listdir(config.ALREADY_SAVED_DATA_DIR)
    already_saved_pics = []
    for file in already_saved_data_files:
        with open(os.path.join(config.ALREADY_SAVED_DATA_DIR, file)) as f:
            data = json.load(f)
        already_saved_pics.extend(data['pics'])

    while not queue.empty():
        i = queue.get(timeout=10)
        url = i['imageUrls'][0]['original'].replace('i.pximg.net', 'original.img.cheerfun.dev')  # type: str
        file_type = url[url.rindex('.') + 1:]
        file_name = str(i['id'])
        if f'{file_name}.{file_type}' in already_saved_pics:
            print('其他仓库已下载，不再下载')
            continue
        sleep(random.randrange(0, 3))
        if not os.path.exists(os.path.join(config.IMAGES_SAVE_DIR, file_name + file_type)):
            utils.download(
                file_url=url,
                file_name=file_name,
                file_type=file_type,
                headers=config.HEADERS,
                save_path=config.IMAGES_SAVE_DIR
            )


def main():
    files = os.listdir(config.DL_TASK_DIR)
    if not files:
        print('没有下载任务文件，请先执行paser')
        return None
    while files:
        file = os.path.join(config.DL_TASK_DIR, files.pop())
        with open(file, 'r') as f:
            items = json.load(f)
        utils.remove_file(file)
        for i in items:
            queue.put(i)
        threads = [Thread(target=dl) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
