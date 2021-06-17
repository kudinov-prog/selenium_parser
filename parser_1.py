from selenium import webdriver
import time
import csv


class FsspParser(object):
    """ Создает объект для парсинга (одна строка исходной таблицы)
        и парсит его
    """

    def __init__(self, driver, last_name, first_name, patronymic, date):
        self.driver = driver
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.date = date

    def parse(self):
        # закрываем всплывающее окно
        btn_close = self.driver.find_element_by_class_name("tingle-modal__closeIcon")
        btn_close.click()

        # открываем расширенный поиск
        btn_elem = self.driver.find_element_by_class_name("main-form__toggle-open")
        btn_elem.click()

        # вводим данные в форму
        last_name_form = self.driver.find_element_by_name("is[last_name]")
        last_name_form.send_keys(self.last_name)

        first_name_form = self.driver.find_element_by_name("is[first_name]")
        first_name_form.send_keys(self.first_name)

        patronymic_form = self.driver.find_element_by_name("is[patronymic]")
        patronymic_form.send_keys(self.patronymic)

        date_form = self.driver.find_element_by_name("is[date]")
        date_form.send_keys(self.date)

        # нажимаем кнопку найти
        btn_elem_1 = self.driver.find_element_by_xpath("//button[@class='btn btn-primary']")
        btn_elem_1.click()

        # cell s-2
        btn_elem_2 = self.driver.find_element_by_class_name("cell s-2")
        btn_elem_2.click()


def main():

    driver = webdriver.Chrome()
    driver.get("http://fssprus.ru/")
    time.sleep(1)

    with open("input_list.csv", encoding='utf-8-sig') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")

        for elem in file_reader:
            parser = FsspParser(
                driver, elem[0], elem[1], elem[2], elem[3]
            )
            parser.parse()


if __name__ == "__main__":
    main()
