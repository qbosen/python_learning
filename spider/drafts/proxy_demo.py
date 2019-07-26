from urllib.request import ProxyHandler, build_opener, urlopen
from urllib.error import URLError
import socket
import socks
import requests
from multiprocessing import Process


def http_proxy_test():
    proxy = '127.0.0.1:1087'
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)


def socket5_proxy_test():
    # 需要socks模块
    socks.set_default_proxy(socks.SOCKS5, addr='127.0.0.1', port=1086)
    socket.socket = socks.socksocket
    try:
        response = urlopen('http://httpbin.org/get')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)


def requests_proxy_test():
    proxy = '127.0.0.1:1087'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


if __name__ == '__main__':
    Process(target=http_proxy_test).start()
    Process(target=socket5_proxy_test).start()
    Process(target=requests_proxy_test).start()
