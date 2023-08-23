import json
import os
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parser(area_id, vacancy, url):
    # url = f'https://spb.hh.ru/search/vacancy?area={area_id}&search_field=name&search_field=company_name&search_field=description&text={vacancy}&enable_snippets=false&only_with_salary=true&L_save_area=true'
    url = "https://api.hh.ru/vacancies"

    for counter in range(10):
        # Параметры запроса
        params = {
            "area": 2,  # Код региона (Санкт-Петербург)
            "text": "системный администратор",  # Ключевое слово для поиска
            "page": counter
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            vacancies = data.get("items", [])

            workbook = Workbook()
            sheet = workbook.active
            data = json.loads(response.text)
            sheet.append(['Вакансия', 'Адрес', 'Сотрудник', 'Контакт', 'Зарплата'])

            vacancies = data.get("items", [])
            data_for_vacancy = []
            for vacancy in vacancies:
                # data_for_vacancy.append([vacancy['salary'], vacancy['name'], vacancy['address'], vacancy['employer'], vacancy['contacts']])  # Выводит каждую вакансию в виде словаря

                try:
                    try:
                        chromedriver_path = '/usr/local/bin/chromedriver'

                        chrome_options = Options()
                        chrome_options.add_argument('--headless')
                        chrome_options.add_argument('--disable-gpu')
                        chrome_options.add_argument('--no-sandbox')
                        driver = webdriver.Chrome(executable_path=chromedriver_path,
                                                  chrome_options=chrome_options)  # Используйте соответствующий WebDriver
                        print(url)
                        driver.get(url)
                        wait = WebDriverWait(driver, 10)
                        contact_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-qa='show-employer-contacts']")))

                        contact_button.click()
                        phone_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href^='tel:']")))
                        phone_number = phone_element.text
                        print(phone_number)
                        driver.quit()

                        return 200
                    except requests.exceptions.RequestException as e:
                        print(f"Ошибка: {e}")

                    print(vacancy['alternate_url'])
                except TypeError:
                    continue
                print("-" * 40)

            else:
                print("Failed to retrieve data. Status code:", response.status_code)


def parse_vacancies(url):
    # chromedriver_path = '/usr/local/bin/chromedriver'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Firefox(options=chrome_options)  # Используйте соответствующий WebDriver   executable_path=chromedriver_path, chrome_options=chrome_options

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Запуск браузера без UI
    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    all_vacancies = []

    while True:
        vacancies = driver.find_elements(By.CSS_SELECTOR, "div.vacancy-serp-item")

        for vacancy in vacancies:
            title_element = vacancy.find_element(By.CSS_SELECTOR, "a[data-qa='vacancy-serp__vacancy-title']")
            title = title_element.text

            salary_element = vacancy.find_element(By.CSS_SELECTOR, "span[data-qa='vacancy-serp__vacancy-compensation']")
            salary = salary_element.text if salary_element.text else "Зарплата не указана"

            phone_element = vacancy.find_element(By.CSS_SELECTOR, "a[data-qa='vacancy-serp__vacancy-employer-phone']")
            phone_number = phone_element.get_attribute("href").replace("tel:", "") if phone_element.get_attribute("href") else "Номер не указан"

            all_vacancies.append({"title": title, "salary": salary, "phone": phone_number})

        next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-qa='pager-next']")
        if next_page_button.is_enabled():
            next_page_button.click()
            wait.until(EC.staleness_of(vacancies[0]))  # Ждем, пока обновится список вакансий
        else:
            break

    driver.quit()
    return all_vacancies
