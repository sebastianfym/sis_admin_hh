import json
import os
from datetime import datetime

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

from parser.models import Questionnaire


def parse_vacancies(url, cookies):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)  # Перезагрузка страницы с примененными куками
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
            phone_number = phone_element.get_attribute("href").replace("tel:", "") if phone_element.get_attribute(
                "href") else "Номер не указан"

            all_vacancies.append({"title": title, "salary": salary, "phone": phone_number})

        next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-qa='pager-next']")
        if next_page_button.is_enabled():
            next_page_button.click()
            wait.until(EC.staleness_of(vacancies[0]))  # Ждем, пока обновится список вакансий
        else:
            break

    driver.quit()
    return all_vacancies


def parse_sys_admin_who_work_in_real_time(vacancy, area_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    for counter in range(100):

        params = {
            "text": vacancy,
            "area": area_id,  # Код региона для Санкт-Петербурга
            "employment": "full",  # Работает на данный момент
        }

        url = "https://api.hh.ru/resumes"

        response = requests.get(url, headers=headers, params=params)

        resume_list = response.json()

        try:
            for resume_dict in resume_list['items']:
                try:
                    if resume_dict['experience'][0]['end'] is None and resume_dict['title'] == vacancy:
                        Questionnaire.objects.create(  # update_or_create
                            photo_link=resume_dict['photo']['500'] if resume_dict['photo'] else None,
                            link=resume_dict.get('alternate_url'),
                            company_name=resume_dict['experience'][0]['company'] if resume_dict['experience'][0][
                                'company'] else None,
                            work_in_real_time=resume_dict['experience'][0]['start'] + ' — по настоящее время',
                            work_experience=str(resume_dict['total_experience'][
                                                    'months']) + f' месяца или {int(resume_dict["total_experience"]["months"]) / 12} лет' if
                            resume_dict['total_experience']['months'] is not None else None,
                            gender=resume_dict['gender']['name'] if resume_dict['gender'] else None,
                            age=resume_dict['age'] if resume_dict['age'] else None,
                            vacancy=resume_dict['title'] if resume_dict['title'] else None,
                            salary=resume_dict['salary']['amount'] if resume_dict['salary'] else None,
                            education=resume_dict['education']['primary'][0]['name'] if len(
                                resume_dict['education']['primary']) != 0 else None,
                            updated_at=datetime.strptime(resume_dict['updated_at'], '%Y-%m-%dT%H:%M:%S%z').strftime(
                                '%Y-%m-%d %H:%M:%S')
                            if resume_dict['updated_at'] else None,
                            city=resume_dict['area']['name'] if resume_dict['area']['name'] else None,
                        )
                except IndexError as e:
                    continue
            # counter += 1
        except KeyError as e:
            break
    return
