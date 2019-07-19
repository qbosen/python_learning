import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36 '
}
url = 'https://www.zhihu.com/explore'
response = requests.get(url, headers=headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.DOTALL)
titles = pattern.findall(response.text)
print(titles)
