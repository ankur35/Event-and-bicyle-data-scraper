import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from os import path, mkdir

def ensure_data_folder_exists(data_folder):
    if not path.isdir(data_folder):
        mkdir(data_folder)

def get_excel_sheets(url, data_folder):

    driver = webdriver.Firefox()
    driver.get(url)
    sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a')

    for link in links:

        if link.text.endswith('.xls') or link.text.endswith('.csv'):
            filename = link.text.replace(',', '').replace(' ', '-')
            full_path = data_folder + '/' + filename
            
            print('working on {}'.format(full_path))

            if path.isfile(full_path):
                print('file already exists')
                continue
         
            data = requests.get(link['href']).text
            
            with open(full_path, 'w') as f:
                f.write(data)
                f.close()
                print('saved {}'.format(full_path))

    driver.close()


if __name__ == '__main__':
    url = 'https://cycling.data.tfl.gov.uk/'
    data_folder = 'cycling-gov-data'

    ensure_data_folder_exists(data_folder)
    get_excel_sheets(url, data_folder)

