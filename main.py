import json
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException


options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

data = {}
count_page = 0

for page in range(2, 7):
    url = f"https://www.russiadiscovery.ru/tours/page/{page}/"
    driver.get(url)
    block = driver.find_element(By.CLASS_NAME, 'tourListUl')
    posts = block.find_elements(By.TAG_NAME, 'li')
    for post in posts:
        title_link = post.find_element(By.CLASS_NAME, 'tourList__title').find_element(By.TAG_NAME, 'a').get_attribute('href')
        title = post.find_element(By.CLASS_NAME, 'tourList__title').find_element(By.TAG_NAME, 'a').text
        price = post.find_element(By.CLASS_NAME, 'tourList__price').find_element(By.TAG_NAME, 'span').text.replace(" ", ".")
        data[title] = {
            'url': title_link,
            'price': price
        }
        time.sleep(random.randint(1, 3))

    for post_url in data.values():
        driver.get(post_url['url'])
        print(f"Doing: {post_url['url']}")
        print(f"page number: {count_page}")
        time.sleep(random.randint(1, 3))
        count_page += 1

        size = driver.find_element(By.CLASS_NAME, 'size_group').find_element(By.CLASS_NAME, 'right').text
        post_url['group_size'] = size

        photo_count = driver.find_element(By.CLASS_NAME, 'moreMediaGallery').text
        photo_count = int(photo_count.replace("+", "").replace(" ", "")) + 5
        post_url['photos'] = []

        for photo_num in range(1, photo_count):
            photo_url = f"{post_url['url']}#&gid=1&pid={photo_num}"
            post_url['photos'].append(photo_url)

        with open("result3.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    time.sleep(5)
    driver.quit()