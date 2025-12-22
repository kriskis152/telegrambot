import os

from playwright.sync_api import sync_playwright
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from dotenv import set_key

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
    page = brower.new_page()

    page.goto("https://journal.top-academy.ru/ru/auth/login")
    logger.info("Страница загружена")

    page.wait_for_selector('input[name="username"]', timeout=10000)
    page.fill('input[name="username"]', LOGIN)
    page.fill('input[name="password"]', PASSWORD)
    logger.info("Данные для входа введены")

    page.click('button[type="submit"]')
    logger.info("Кнопка ввода нажата")

    page.wait_for_timeout(5000)
    logger.success(f"Вход выполнен. {page.url}")

    page.goto('https://journal.top-academy.ru/ru/main/homework/page/index')
    logger.info("Зашли на страницу с домашним заданием")

    page.mouse.click(100,100)
    for i in range (5):
        page.keyboard.press("PageDown")
        page.wait_for_timeout(300)
    logger.info("Долистали до конца")
    page.locator("div.item-image").last.hover()
    page.locator("upload-file").last.click()
    #page.wait_for_timeout(300)
    logger.info("Навели курсор")


    input("Нажмите Enter для закрытия...")
    brower.close()




