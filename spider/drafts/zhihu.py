import requests
from pyquery import PyQuery

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36 '
}
url = 'https://www.zhihu.com/explore'
response = requests.get(url, headers=headers)
html = response.text
doc = PyQuery(html)
file = open('explore.txt', 'w', encoding='utf-8')
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer_html = item.find('.content').html()
    answer = PyQuery(answer_html).text()
    file.write('\n'.join([question, author, answer]))
    file.write('\n' + '=' * 50 + '\n')
file.close()
