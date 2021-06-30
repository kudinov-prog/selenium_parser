## Парсер сайта http://fssprus.ru/

Парсер построчно берет данные людей для поиска из файла input_list.csv, делает запрос и при наличии задолженностей сохраняет данные по ним в файл result.csv


## Установка проекта
Для установки на локальной машине потребуется:
* Клонировать репозиторий
* Установить нужные библиотеки из файла requirements.txt
* Установить программу tesseract для своей системы https://github.com/UB-Mannheim/tesseract/wiki
* Скачать и положить пакет для распознавания русского языка в папку /tessdata c установленной программой https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016
* Запустить файл parser_fssp.py
