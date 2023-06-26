import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.CustomerEncoder import CustomerEncoder
from domain.common import URL
from domain.hex import GalaxyHex, GalaxyHexItem
from domain.utils import download_photo


def main():
    hexes = []
    url = URL.TFT_GALAXY_HEX_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)
        version_el = browser.find_element(By.CLASS_NAME, 'season-link').find_elements(By.TAG_NAME, 'span')[
            1].get_attribute('innerText')
        version_txt = version_el.replace(' ', '_')

        items = browser.find_elements(By.CLASS_NAME, 'galaxy-list-item')

        for item in items:
            galaxy_hex = GalaxyHex()
            galaxy_hex.galaxy_hex_img = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
            galaxy_hex.galaxy_hex_name = item.find_element(By.CLASS_NAME, 'badge-name').get_attribute('innerText')

            infos = item.find_element(By.CLASS_NAME, 'galaxy-item-info').find_elements(By.TAG_NAME, 'p')
            for info in infos:
                galaxy_hex_item = GalaxyHexItem()
                galaxy_hex_item.title = info.find_element(By.CLASS_NAME, 'info-title').get_attribute('innerText')
                galaxy_hex_item.desc = info.find_element(By.CLASS_NAME, 'info-desc').get_attribute('innerText')
                galaxy_hex.galaxy_hex_items.append(galaxy_hex_item)

            hexes.append(galaxy_hex)

        with open('resources/json/galaxy_hex_' + version_txt + '.json', 'w', encoding='utf8') as f1:
            json.dump(hexes, f1, cls=CustomerEncoder, indent=4, ensure_ascii=False)
        image_path = 'resources/images/galaxy_hex/' + version_txt
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        for hex_item in hexes:
            index = hex_item.galaxy_hex_img.rfind('/')
            name = hex_item.galaxy_hex_img[index + 1:]
            download_photo(hex_item.galaxy_hex_img, image_path + '/' + name)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
