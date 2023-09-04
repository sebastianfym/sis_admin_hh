import json
import os
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import openpyxl
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

def parse_vacancies(url):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['Название вакансии', 'Компания', 'Адрес', 'Опыт', 'контакты'])

    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://spb.hh.ru/account/login?backurl=%2Femployer')
    time.sleep(40)
    all_vacancies = []
    for page_number in range(1, 11):
        driver.get(f'https://spb.hh.ru/vacancies/sistemnyy_administrator?page={page_number}')
        buttons = driver.find_elements(By.CSS_SELECTOR, 'div.serp-item-controls')

        # time.sleep(30)
        for btn in buttons:
            time.sleep(5)
            try:

                if btn.text == "Показать контакты":
                    div = btn.find_element(By.XPATH, '..')

                    print()#get_attribute("class"))
                    vacancy_data = div.text.split('\n')
                    button = btn.find_element(By.TAG_NAME, "button")

                    button.click()
                    time.sleep(2)
                    try:
                        try:
                            f_e = driver.find_element(By.CSS_SELECTOR, 'div.vacancy-contacts-call-tracking__phones')
                            # contact_div = driver.find_element(By.CSS_SELECTOR, "div.vacancy-contacts_search")
                            # print(contact_div)
                            print(f_e.text)
                        except NoSuchElementException:
                            f_e = driver.find_element(By.CSS_SELECTOR, 'div.bloko-drop')
                            print(f_e.text)
                    except NoSuchElementException:
                        f_e = None

            except ElementNotInteractableException:
                print(f'NET: {btn}')
            print()
            try:
                if len(vacancy_data) <= 5:
                    try:
                        sheet.append([vacancy_data[0], vacancy_data[1], vacancy_data[2], vacancy_data[3], f_e.text])
                    except selenium.common.exceptions.StaleElementReferenceException:
                        continue
                else:
                    try:
                        sheet.append([vacancy_data[0], vacancy_data[2], vacancy_data[3], vacancy_data[4], f_e.text])
                    except selenium.common.exceptions.StaleElementReferenceException:
                        continue
            except UnboundLocalError:
                continue


        next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-qa='pager-next']")
        if next_page_button.is_enabled():
            next_page_button.click()
            # wait.until(EC.staleness_of(vacancies[0]))  # Ждем, пока обновится список вакансий
        else:
            break
    file_path = "company_who_search_sys_admin.xlsx"
    workbook.save(file_path)
    driver.quit()
    return workbook


def parse_sys_admin_who_work_in_real_time(vacancy, area_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['Название вакансии', 'ссылка на анкету', 'Название компании', 'Город'])
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
                    if resume_dict['experience'][0]['end'] is None and resume_dict['title'] == vacancy or resume_dict['title'].lower() == vacancy.lower():
                        sheet.append([resume_dict['title'], resume_dict.get('alternate_url'), resume_dict['experience'][0]['company'], resume_dict['area']['name']])


                        # Questionnaire.objects.create(  # update_or_create
                        #     # photo_link=resume_dict['photo']['500'] if resume_dict['photo'] else None,
                        #     link=resume_dict.get('alternate_url'),
                        #     company_name=resume_dict['experience'][0]['company'] if resume_dict['experience'][0][
                        #         'company'] else None,
                        #     work_in_real_time=resume_dict['experience'][0]['start'] + ' — по настоящее время',
                        #     work_experience=str(resume_dict['total_experience'][
                        #                             'months']) + f' месяца или {int(resume_dict["total_experience"]["months"]) / 12} лет' if
                        #     resume_dict['total_experience']['months'] is not None else None,
                        #     gender=resume_dict['gender']['name'] if resume_dict['gender'] else None,
                        #     age=resume_dict['age'] if resume_dict['age'] else None,
                        #     vacancy=resume_dict['title'] if resume_dict['title'] else None,
                        #     salary=resume_dict['salary']['amount'] if resume_dict['salary'] else None,
                        #     education=resume_dict['education']['primary'][0]['name'] if len(
                        #         resume_dict['education']['primary']) != 0 else None,
                        #     updated_at=datetime.strptime(resume_dict['updated_at'], '%Y-%m-%dT%H:%M:%S%z').strftime(
                        #         '%Y-%m-%d %H:%M:%S')
                        #     if resume_dict['updated_at'] else None,
                        #     city=resume_dict['area']['name'] if resume_dict['area']['name'] else None,
                        # )
                except IndexError as e:
                    print(e)
                    continue
            # counter += 1
        except KeyError as e:
            print(e)
            break
    file_path = "result_admin.xlsx"
    workbook.save(file_path)
    return workbook


def parse_vacancies_sys_admin(vacancy, area_id, access_token, page_number):
    url = "https://api.hh.ru/vacancies"

    params = {
        "text": "Системный администратор",
        "area": "2",  # Код региона для Санкт-Петербурга
        "page": page_number
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        vacancies = response.json()
        for vacancy in vacancies["items"]:
            print(vacancy["name"], vacancy['area']['name'], vacancy['alternate_url'], vacancy['contacts'])
            # print(vacancy, end='\n\n')
    else:
        print("Ошибка при запросе:", response.status_code)


