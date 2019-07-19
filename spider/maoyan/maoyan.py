import json
import time

import requests
from bs4 import BeautifulSoup


def get_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.100 Safari/537.36 '}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    for dd in soup.select('#app > div > div > div.main > dl > dd'):
        result = {
            'index': dd.i.string,
            'image': dd.select_one('img[data-src]')['data-src'],
            'title': dd.select_one('p[class=name]').a.string,
            'actor': dd.select_one('p[class=star]').text.strip()[3:],
            'time': dd.select_one('p[class=releasetime]').string[5:],
            'score': dd.select_one('p[class=score]').text
        }
        yield result


def write_to_file(content, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def classic_top_100():
    url = 'https://maoyan.com/board/4?offset='
    for i in range(10):
        html = get_one_page(url + str(i * 10))
        time.sleep(0.2)
        for item in parse_one_page(html):
            print(item)
            write_to_file(item, 'top100.txt')


if __name__ == '__main__':
    classic_top_100()
