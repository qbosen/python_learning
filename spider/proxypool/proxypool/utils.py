import requests
from requests.exceptions import RequestException

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}, try_times=3):
    """
    抓取代理
    :param url: 目标url
    :param options: 额外头部信息
    :param try_times: 尝试次数
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    result = None
    for i in range(try_times):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            print('抓取成功', url, response.status_code)
            if response.status_code == 200:
                result = response.text
                break
        except RequestException:
            print('第 %s 次抓取失败' % (i + 1), url)
    return result
