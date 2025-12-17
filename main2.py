import os

from playwright.sync_api import sync_playwright
from loguru import logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
LOGIN1 = os.getenv('LOGIN1')
PASSWORD1 = os.getenv('PASSWORD1')
logger.info("Запуск браузера...")

with sync_playwright() as p:
    logger.add('file.log',
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days")

    brower = p.chromium.launch(headless=False)

    page2 = brower.new_page()
    namestudent = input("Введите имя на github: ")
    page2.goto('https://github.com/' + namestudent)
    logger.info('Открыли github')

    page2.wait_for_selector('a[data-tab-item="repositories"]') # a -ссылка, [] - ключ, " " - значение. 
    # Playwright найди все элементы с типом <a>, среди них найди тот, в котором [data-tab-item="repositories"]
    page2.click('a[data-tab-item="repositories"]') #найди ссылку <a> у которой есть атрибут data-tab-item и значение этого атрибуа repositories
    logger.info("Перешли к выбору репозитория")

    input("Нажмите Enter для закрытия...")
    brower.close()