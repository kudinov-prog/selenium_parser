from selenium import webdriver
import time
import csv

from cv_captcha import captcha_to_text


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

    def parse_input(self):
        """ Вводит данные для поиска и переходит до страницы с капчой
        """
        btn_close_window = self.driver.find_element_by_class_name("tingle-modal__closeIcon")
        btn_close_window.click()

        btn_advanced_find = self.driver.find_element_by_class_name("main-form__toggle-open")
        btn_advanced_find.click()

        last_name_form = self.driver.find_element_by_name("is[last_name]")
        last_name_form.send_keys(self.last_name)
        first_name_form = self.driver.find_element_by_name("is[first_name]")
        first_name_form.send_keys(self.first_name)
        patronymic_form = self.driver.find_element_by_name("is[patronymic]")
        patronymic_form.send_keys(self.patronymic)
        date_form = self.driver.find_element_by_name("is[date]")
        date_form.send_keys(self.date)

        btn_find = self.driver.find_element_by_xpath("//button[@class='btn btn-primary']")
        btn_find.click()
        time.sleep(3)

    def insert_code(self):
        """ Распознает изображение капчи и преобразует в текст. Вводит в
            форму и проверяет корректность, если нет - перезапускает функцию.
        """
        find_img = self.driver.find_element_by_class_name("context").find_element_by_css_selector('img')

        CAPTCHA_URL = str(find_img.get_attribute("src"))
        CAPTCHA_TEXT = captcha_to_text(CAPTCHA_URL)

        captcha_form = self.driver.find_element_by_name("code")
        captcha_form.send_keys(CAPTCHA_TEXT)
        time.sleep(1)

        btn_move = self.driver.find_element_by_xpath("//input[@class='input-submit-capcha']")
        btn_move.click()
        time.sleep(2)

        wrong_text = self.driver.find_element_by_tag_name("body").text
        if 'Неверно введен код' in wrong_text:
            self.insert_code()

    def parse_result(self):
        """ При наличии у запрашиваемого человека задолжностей парсит их
        """
        result = self.driver.find_element_by_tag_name("body").text

        if 'По вашему запросу ничего не найдено' not in result:
            find_elements = self.driver.find_elements_by_xpath("//table[@class='list border table alt-p05']/tbody/tr")
            result_list = [elem.text.split('\n') for elem in find_elements[2:]]

            with open("result.csv", mode="w", encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, lineterminator="\r")
                file_writer.writerows(result_list)


def main():
    with open("input_list.csv", encoding='utf-8-sig') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")

        for elem in file_reader:
            driver = webdriver.Chrome()
            driver.get("http://fssprus.ru/")
            time.sleep(1)

            parser = FsspParser(
                driver, elem[0], elem[1], elem[2], elem[3]
            )

            parser.parse_input()
            parser.insert_code()
            parser.parse_result()
            driver.close()


if __name__ == "__main__":
    main()
