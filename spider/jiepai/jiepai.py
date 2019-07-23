import os
import time
from hashlib import md5
from multiprocessing.pool import Pool
from urllib.parse import urlencode

import requests

headers = {
    'Cookie': 'tt_webid=6716849148794488328; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=h0eacgnym1563888320962; '
              'tt_webid=6716849148794488328; csrftoken=ef68166e64b5446bbffe4e564490f484; SL_GWPT_Show_Hide_tmp=1; '
              'SL_wptGlobTipTmp=1; s_v_web_id=65c440f83c57465f1ea9330fe82cb72f',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(offset):
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time() * 1000)
    }
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json['data']:
        data = json['data']
        for item in data:
            if item.get('title') is None:
                continue
            title = item['title']
            images = item['image_list']
            for image in images:
                yield {
                    'url': image.get('url'),
                    'title': title
                }


def save_image(image_info):
    image_dir = os.path.join('images', image_info['title'])
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    try:
        response = requests.get(image_info['url'])
        if response.status_code == 200:
            file_path = os.path.join(image_dir, md5(response.content).hexdigest() + '.jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as file:
                    file.write(response.content)
    except requests.ConnectionError:
        print("save image failed")


def main(offset):
    json = get_page(offset)
    for image in get_images(json):
        print(image)
        save_image(image)


# 起始/结束页
GROUP_START = 0
GROUP_END = 2

if __name__ == '__main__':
    pool = Pool()
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    pool.map(main, groups)
    pool.close()
    pool.join()
