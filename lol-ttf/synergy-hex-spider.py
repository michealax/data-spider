import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.CustomerEncoder import CustomerEncoder
from domain.common import URL
from domain.hex import Hex, HexComponent
from domain.utils import download_photo


def main():
    hexes = []
    url = URL.TFT_NORMAL_HEX_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)
        version_el = browser.find_element(By.CLASS_NAME, 'season-link').find_elements(By.TAG_NAME, 'span')[
            1].get_attribute('innerText')
        version_txt = version_el.replace(' ', '_')

        buttons = browser.find_element(By.CLASS_NAME, 'secondary-filter-box').find_elements(By.CLASS_NAME, 'btn-type')

        for btn in buttons:
            # btn = browser.find_elements(By.CLASS_NAME, 'secondary-filter-box')[i]
            btn.click()
            items = browser.find_elements(By.CLASS_NAME, 'synergy-item')
            hex_item = Hex()
            hex_item.hex_level = btn.get_attribute('innerText')
            for item in items:
                component = HexComponent()
                component.hex_component_img = item.find_element(By.CLASS_NAME, 'hex-img').get_attribute('src')
                component.hex_component_name = item.find_element(By.CLASS_NAME, 'hex-name').get_attribute('innerText')
                component.hex_component_desc = item.find_element(By.CLASS_NAME, 'txt-p').get_attribute('innerText')
                hex_item.hex_components.append(component)
            hexes.append(hex_item)

        with open('resources/json/normal_hex_' + version_txt + '.json', 'w', encoding='utf8') as f1:
            json.dump(hexes, f1, cls=CustomerEncoder, indent=4, ensure_ascii=False)
        image_path = 'resources/images/normal_hex/' + version_txt
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        for hex_item in hexes:
            for item in hex_item.hex_components:
                index = item.hex_component_img.rfind('/')
                name = item.hex_component_img[index + 1:]
                download_photo(item.hex_component_img, image_path + '/' + name)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
