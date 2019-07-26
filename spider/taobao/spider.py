import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from config import *

from urllib.parse import quote

options = webdriver.ChromeOptions()
# 设置为开发者模式，放置被各大网站识别出来使用了Selenium
# 如果不设置 淘宝验证码不通过
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
login_flag = False


def check_login():
    global login_flag
    if not login_flag:
        # 简单的进行手动登陆
        input('等待登陆...')
        login_flag = True


def index_page(page_index):
    """
    抓取索引页
    :param page_index:页码
    """
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        driver.get(url)
        check_login()
        print('正在爬取第%s页' % page_index)
        if page_index > 1:
            # 等待索引页输入框加载完成
            page_input_selector = (By.CSS_SELECTOR, '#mainsrp-pager div.form > input')
            submit_button_selector = (By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')
            page_input = wait.until(EC.presence_of_element_located(page_input_selector))
            submit_button = wait.until(EC.element_to_be_clickable(submit_button_selector))

            page_input.clear()
            page_input.send_keys(page_index)
            submit_button.click()

        # 等待下方当前页码变为目标值，即跳转成功
        current_page_selector = (By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span')
        wait.until(EC.text_to_be_present_in_element(current_page_selector, str(page_index)))
        # 商品列表加载成功
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))

        get_products()
    except TimeoutException:
        # 超时就重新加载
        index_page(page_index)


def get_products():
    """
        提取商品数据
        """
    html = driver.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert_one(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    driver.close()


if __name__ == '__main__':
    main()
