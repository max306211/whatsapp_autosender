''' Скрипт для отправки сообшений в вацап.
На вход принимает URL который содержит номер абонента и сообщение.
Требутся первичная авторизация. Если скрипт видит заголовок авторизации - делается скриншот и ожидает авторизации WIAT_TIME
Все настройки сохраняются в папку где находится скрипт'''
import datetime
import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--headless') # GUI DISABLED
options.add_argument('--no-sandbox')  # GUI DISABLED
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(f'user-data-dir={os.path.dirname(os.path.abspath(__file__))}') # УКАЗАТЬ ПУТЬ ГДЕ УБДЕТ ЛЕЖАТЬ ФАЙЛЫ БРАУЗЕРА
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--profiling-flush=n')
options.add_argument('--enable-aggressive-domstorage-flushing')
options.add_argument('user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)
WAIT_TIME = 120



def main(url:str):
    driver.get(url)
    sleep(1)
    try:
        x = driver.find_element(By.ID, "initial_startup")
        time.sleep(20)
        driver.save_screenshot(f"auth_screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M-%S')}.png")
        print("Требуется авторизация")
        time.sleep(WAIT_TIME)
        """ МЕСТО ВЫЗОВА ПОСТ ЗАПРОСА НА АВТОРИЗАЦИЮ -- 2 мин ожидание. Авторизаиця выполняется 1 раз."""
    except NoSuchElementException as err:
        print("НЕ Требуется авторизация")
        pass
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
    print("Отправлено")


if __name__ == "__main__":
    url = f"https://web.whatsapp.com/send?phone=+79065467911&text=Привет+мир!"
    main(url)