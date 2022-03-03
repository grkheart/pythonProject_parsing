from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pprint import pprint
import requests
from lxml import html
import pymongo
from pymongo.errors import DuplicateKeyError
from lxml import etree


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)  # Подключаемся к базе
    db = client['local']  # База для записи результатов
    goods = db.local

# Сбор данных о акционных продуктах

def get_news(parsInfo):
    goods_list = []
    href = parsInfo.xpath(".//div[@class='product-card item']")
    for url in href:
        r = requests.get(url, headers=HEADERS)
        dom_local = etree.HTML(r.text)
        block_goods = dom_local.xpath(".//div[@class='product-card item]")[0]
        goods_list.append({
            "_id": url.split('/')[-2],
            "source": block_goods.xpath('./text()')[0],
            "title": block_goods.xpath('.//div[@class="item-name"]//text()')[0],
            "expired": block_goods.xpath('.//div[@class="item-date"]]//text()')[0],
            "price": block_goods.xpath('.//div[@class="prices"]/text()')[0]
            }
        )
    return goods_list


s = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://5ka.ru/special_offers')

button = driver.find_element(By.XPATH, "//span[contains(text(),'Принять')]")
button.click()

while True:
    wait = WebDriverWait(driver, 5)
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-more-btn")))
    button = driver.find_element(By.CLASS_NAME, "add-more-btn")
    button.click()

elems = driver.find_elements(By.CLASS_NAME, 'product-card item')
for elem in elems:
    pass



