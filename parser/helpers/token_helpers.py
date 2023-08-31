import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from parser.additional_config import client_id, redirect_uri, client_secret


def get_authorization_code():
    url = f'https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}'
    try:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome()  # Используйте соответствующий WebDriver

        driver.get(url)
        button = driver.find_element(By.CSS_SELECTOR, '[data-qa="oauth-grant-allow"]')
        button.click()
        time.sleep(10)
        # current_url = driver.current_url
        # code = unquote(current_url).split('code=')[1]
        driver.quit()

        return 200
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")



def get_access_token(authorization_code):
    url = 'https://hh.ru/oauth/token'

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, data=data)
    response_data = response.json()
    access_token = response_data['access_token']
    # boss.refresh_token = None
    # boss.access_token = access_token
    # boss.save()
    return access_token


def refresh_access_token():
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': 'refresh_token',
    }

    response = requests.post('https://hh.ru/oauth/token', data=data)
    result = response.json()
    print(result)
    return result['access_token']