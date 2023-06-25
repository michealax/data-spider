import json
import os.path

from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.common import URL
from domain.CustomerEncoder import CustomerEncoder
from domain.Synergy import Synergy, Level
from domain.utils import download_photo


def get_items_from_browser(browser, synergies):
    items = browser.find_elements(By.CLASS_NAME, 'synergy-item')
    for item in items:
        synergy_icon = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
        synergy_name = item.find_element(By.CLASS_NAME, 'synergy').get_attribute('innerText')
        synergy_text = item.find_element(By.CLASS_NAME, 'txt-p').get_attribute('innerText')
        synergy = Synergy()
        synergy.synergy_icon = synergy_icon
        synergy.synergy_name = synergy_name
        synergy.synergy_text = synergy_text
        synergy.levels = []

        p_list = item.find_elements(By.CLASS_NAME, 'txt-p2')
        for p in p_list:
            level = Level()
            level.level = p.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
            p_txt = p.get_attribute('innerText')
            level.level_text = p_txt[p_txt.find('\n') + 1:]
            synergy.levels.append(level)
        synergies.append(synergy)


def main():
    synergies = []
    url = URL.TFT_SYNERGY_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)
        version_el = browser.find_element(By.CLASS_NAME, 'season-link').find_elements(By.TAG_NAME, 'span')[
            1].get_attribute('innerText')
        version_txt = version_el.replace(' ', '_')
        get_items_from_browser(browser, synergies)

        buttons = browser.find_elements(By.CLASS_NAME, 'btn-type')
        buttons[1].click()
        get_items_from_browser(browser, synergies)
        with open('resources/json/synergy_' + version_txt + '.json', 'w', encoding='utf8') as f1:
            json.dump(synergies, f1, cls=CustomerEncoder, indent=4, ensure_ascii=False)
        image_path = 'resources/images/synergy/' + version_txt
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        for synergy in synergies:
            index = synergy.synergy_icon.rfind('/')
            name = synergy.synergy_icon[index + 1:]
            download_photo(synergy.synergy_icon, image_path + '/' + name)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
