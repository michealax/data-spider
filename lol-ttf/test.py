from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.common import URL
from selenium import webdriver

from domain.common import URL


def main():
    url = URL.TFT_NORMAL_HEX_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        items = browser.find_elements(By.CLASS_NAME, 'synergy-item')
        for item in items:
            img = item.find_element(By.XPATH, './descendant::img').get_attribute('src')
            hex_name = item.find_element(By.XPATH, './descendant::span[@class="hex-name"]').text
            synergy_text = item.find_element(By.XPATH, './descendant::p[@class="txt-p"]').text

            print(hex_name)
            print(img)
            print(synergy_text)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
