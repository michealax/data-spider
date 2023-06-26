import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.CustomerEncoder import CustomerEncoder
from domain.common import URL
from domain.hex import Hex, HexComponent, ChampionHex, ChampionHexStage, ChampionHexStageItem
from domain.utils import download_photo


def main():
    hexes = []
    url = URL.TFT_CHAMPION_HEX_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)
        version_el = browser.find_element(By.CLASS_NAME, 'season-link').find_elements(By.TAG_NAME, 'span')[
            1].get_attribute('innerText')
        version_txt = version_el.replace(' ', '_')

        buttons = browser.find_elements(By.CLASS_NAME, 'play-bookby-item')

        for i in range(len(buttons)):
            btn = browser.find_elements(By.CLASS_NAME, 'play-bookby-item')[i]
            btn.find_element(By.CLASS_NAME, 'go-buff-details').click()

            hex_item = ChampionHex()
            hex_item.champion_hex_img = browser.find_element(By.CLASS_NAME, 'galaxy-head-image').find_element(
                By.TAG_NAME,
                'img').get_attribute(
                'src')
            hex_item.champion_hex_name = browser.find_element(By.CLASS_NAME, 'galaxy-name').get_attribute('innerText')
            hex_item.champion_hex_desc = browser.find_element(By.CLASS_NAME, 'galaxy-desc').get_attribute('innerText')

            stages = browser.find_elements(By.CLASS_NAME, 'galaxy-stage-item')
            for stage in stages:
                stage_item = ChampionHexStage()
                stage_item.galaxy_stage_con = stage.find_element(By.CLASS_NAME, 'galaxy-stage-con').get_attribute(
                    'innerText')

                galaxy_hex_list = stage.find_elements(By.CLASS_NAME, 'galaxy-hex-list')
                for item in galaxy_hex_list:
                    champion_hex_stage_item = ChampionHexStageItem()
                    champion_hex_stage_item.galaxy_hex_img = item.find_element(By.CLASS_NAME,
                                                                               'galaxy-hex-image').find_element(
                        By.TAG_NAME, 'img').get_attribute('src')
                    champion_hex_stage_item.galaxy_hex_name = item.find_element(By.CLASS_NAME,
                                                                                'galaxy-hex-name').get_attribute(
                        'innerText')
                    champion_hex_stage_item.galaxy_hex_desc = item.find_element(By.CLASS_NAME,
                                                                                'galaxy-hex-desc').get_attribute(
                        'innerText')
                    stage_item.galaxy_hex_list.append(champion_hex_stage_item)

                hex_item.champion_hex_stages.append(stage_item)
            hexes.append(hex_item)
            browser.back()

        with open('resources/json/champion_hex_' + version_txt + '.json', 'w', encoding='utf8') as f1:
            json.dump(hexes, f1, cls=CustomerEncoder, indent=4, ensure_ascii=False)
        image_path = 'resources/images/champion_hex/' + version_txt
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        for hex_item in hexes:
            index = hex_item.champion_hex_img.rfind('/')
            name = hex_item.champion_hex_img[index + 1:]
            download_photo(hex_item.champion_hex_img, image_path + '/' + name)
            for temp in hex_item.champion_hex_stages:
                for item in temp.galaxy_hex_list:
                    index = item.galaxy_hex_img.rfind('/')
                    name = item.galaxy_hex_img[index + 1:]
                    download_photo(item.galaxy_hex_img, image_path + '/' + name)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
