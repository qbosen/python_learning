from urllib.parse import urlencode
import requests
from pyquery import PyQuery
from pymongo import MongoClient

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Referer': 'https://m.weibo.cn/u/2803301701',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page_num):
    params = {
        'type': 'uid',
        # userId 这里是人民日报微博
        'value': '2803301701',
        # 107603+userId
        'containerid': '1076032803301701',
        'page': page_num,
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json_data):
    if json_data:
        items = json_data.get('data').get('cards')
        for item in items:
            blog = item.get('mblog')
            weibo = {
                'id': blog['id'],
                'text': PyQuery(blog['text']).text(),
                'attitudes': blog['attitudes_count'],
                'comments': blog['comments_count'],
                'reposts': blog['reposts_count']
            }
            yield weibo


if __name__ == '__main__':
    client = MongoClient(port=27018)
    db = client['weibo']
    collection = db['weibo']

    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            # 有则更新，没有则插入
            collection.update_one({'id': result['id']}, {'$set': result}, upsert=True)
