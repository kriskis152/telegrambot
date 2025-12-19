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

    page2 = brower.new_page()
    namestudent = input("Введите имя на github: ")
    page2.goto('https://github.com/' + namestudent)
    logger.info('Открыли github')

    page2.wait_for_selector('a[data-tab-item="repositories"]') # a -ссылка, [] - ключ, " " - значение. 
    # Playwright найди все элементы с типом <a>, среди них найди тот, в котором [data-tab-item="repositories"]
    page2.click('a[data-tab-item="repositories"]') #найди ссылку <a> у которой есть атрибут data-tab-item и значение этого атрибуа repositories
    logger.info("Перешли к выбору репозитория")

    count = page2.locator('a[data-tab-item="repositories"] span.Counter').first.inner_text() #locator -ищет окшко со сщётчиклм "span.Counter"
    #firt - потому что их может быть больше, чем одна
    # inner_text - "вытаскивает текст, который видет человек из кнопки Counter"
    repcount = int(count)
    print(f"Количество репозиториев: {repcount}")
    logger.info(f"Количество репозиториев: {repcount}")


    repslink = 'h3 a[itemprop="name codeRepository"]'
    #h3 - заголовок, ищем заголовок уровня3, потом смотрим, что внутри, потом ищем ссылку a с нужным атрибутом
    # если оставить только a, программа будет искать по всей сранице, где есть a,  р3 уву указатель, что искать надо только среди заголовков
    page2.wait_for_selector(repslink, timeout=10000)

    # Собираем все найденные ссылки
    repos_locator = page2.locator(repslink)
    all_repos = repos_locator.all_inner_texts()

    if all_repos:
    # Очищаем названия от лишних пробелов и переносов строк
        clean_names = [name.strip() for name in all_repos]
        logger.info(f"Последний обновленный репозиторий: {clean_names[0]}")
    
    # Кликаем по самому первому
        repos_locator.first.click()
        logger.info("Зашли в последний обновленный репозиторий")
    else:
        logger.error("Не удалось найти список репозиториев")

    lastrep = page2.locator('h3 a[itemprop="name codeRepository"]').first
    link = lastrep.get_attribute('href') # смотрит в словарь и ищет значение по ключу href
    full_link = f"https://github.com{link}"
    logger.info(f"Ссылка на репозиторий: {full_link}")
    env_file_path = ".env"
    set_key(env_file_path, "REPO_URL", full_link)
    logger.info("Ссылка успешно сохранена в .env")


    input("Нажмите Enter для закрытия...")
    brower.close()
    