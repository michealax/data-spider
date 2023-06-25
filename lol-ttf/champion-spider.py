import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from domain.Champion import Champion, Skill, ChampionStat
from domain.CustomerEncoder import CustomerEncoder
from domain.common import URL
from domain.utils import download_photo


def main():
    champions = []
    url = URL.TFT_CHAMPION_URL
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)

        version_el = browser.find_element(By.CLASS_NAME, 'season-link').find_elements(By.TAG_NAME, 'span')[
            1].get_attribute('innerText')
        version_txt = version_el.replace(' ', '_')

        champion_list = browser.find_elements(By.CLASS_NAME, 'champion-item-big')
        for i in range(len(champion_list)):
            item = browser.find_elements(By.CLASS_NAME, 'champion-item-big')[i]
            champion = Champion()
            # set roles
            champion.roles = []
            role_els = item.find_elements(By.CLASS_NAME, 'race-job-name')
            for role in role_els:
                champion.roles.append(role.get_attribute('innerText'))

            item.click()
            champion.name = browser.find_element(By.CLASS_NAME, 'champion-name').get_attribute('innerText')
            champion.price = browser.find_element(By.CLASS_NAME, 'champion-price').get_attribute('innerText')
            champion.pic = browser.find_element(By.CLASS_NAME, 'champion-pic').find_element(By.TAG_NAME,
                                                                                            'img').get_attribute('src')

            # set skill
            skill = Skill()
            skill.skill_pic = browser.find_element(By.CLASS_NAME, 'skill-pic').find_element(By.TAG_NAME,
                                                                                            'img').get_attribute('src')
            skill.skill_name = browser.find_element(By.CLASS_NAME, 'skill-name').get_attribute('innerText')
            skill.skill_type = browser.find_element(By.CLASS_NAME, 'skill-type').get_attribute('innerText')
            skill.skill_desc = browser.find_element(By.CLASS_NAME, 'skill-desc').get_attribute('innerText')
            champion.skill = skill

            # set champion stat
            champion_stat = ChampionStat()
            text = browser.find_element(By.CLASS_NAME, 'detail-info-2').find_element(By.CLASS_NAME,
                                                                                     'detail-info-desc').get_attribute(
                'innerText')
            infos = text.split('\n')
            champion_stat.set(infos)
            champion.champion_stat = champion_stat

            champions.append(champion)
            browser.back()
        with open('resources/json/champion_' + version_txt + '.json', 'w', encoding='utf8') as f1:
            json.dump(champions, f1, cls=CustomerEncoder, indent=4, ensure_ascii=False)
        image_path = 'resources/images/champion/' + version_txt
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        for champion in champions:
            index = champion.pic.rfind('/')
            name = champion.pic[index + 1:]
            download_photo(champion.pic, image_path + '/' + name)

            index = champion.skill.skill_pic.rfind('/')
            name = champion.skill.skill_pic[index + 1:]
            download_photo(champion.skill.skill_pic, image_path + '/' + name)

    finally:
        browser.close()


if __name__ == '__main__':
    main()
