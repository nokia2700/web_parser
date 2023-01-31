import csv
import os.path
import time

from selenium import webdriver

driver = webdriver.Chrome('/Users/dmitrii/PycharmProjects/pythonProject1/chromedriver')

driver.get(f'https://www.regard.ru/catalog/1001/protsessory')

lastPage = driver.find_element_by_xpath('//ul[contains(@class,"Pagination_container")]/li[last()]/a').get_attribute("innerHTML")

for page in range(1, int(lastPage) + 1):
    driver.get(f'https://www.regard.ru/catalog/1001/protsessory?page={page}')

    links = []

    for i in driver.find_elements_by_xpath('//div[contains(@class,"Card_left")]//h6/..'):
        links.append(i.get_attribute("href"))

    for item in links:
        driver.get(item)

        try:
            model = driver.find_element_by_xpath(
                "//span[contains(text(), 'Модель')]/ancestor::li/p/span").get_attribute("innerHTML")
        except:
            continue

        cores = driver.find_element_by_xpath(
            "//span[contains(text(), 'Количество ядер')]/ancestor::li/p/span").get_attribute("innerHTML")
        frequence = driver.find_element_by_xpath(
            "//span[contains(text(), 'Тактовая частота')]/ancestor::li/p/span").get_attribute("innerHTML")

        file = os.path.join(os.getcwd(), 'data.csv')
        file_exists = os.path.isfile(file)
        fields = ["model", "cores", "frequence"]

        with open(file, 'a', encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')

            if not file_exists:
                writer.writeheader()

            writer.writerow({"model": model, "cores": cores, "frequence": frequence})

        time.sleep(1)

    print(f'Распарсили {page} страницу')
    time.sleep(1)

driver.close()
