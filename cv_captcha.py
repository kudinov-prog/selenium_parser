from PIL import Image
import pytesseract
import urllib.request


def captcha_to_text(CAPTCHA_URL):
    """ Получает на вход url картинки, распознает и выдает в виде текста.
    В строке с путем до установленного tesseract указать свой путь
    """
    fname = 'captcha.png'
    pic = urllib.request.urlopen(CAPTCHA_URL).read()

    with open(fname, 'wb') as f:
        f.write(pic)
    img = Image.open(fname)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kudin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    # https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016
    text = pytesseract.image_to_string(img, lang='rus').replace(' ', '')

    return text[:5]
