import os
import smtplib
import re

from email_login import email_login, email_password



#  создает новую папку по указанному пути, при условии, что все указанные промежуточные (вложенные) директории уже существуют.
def make_dir_my(driver_fio):
    # cwd need to change after finished
    cwd = r'D:\test'
    path = os.path.join(cwd, driver_fio)
    isdir_my = os.path.isdir(path)
    if isdir_my is False:
        os.mkdir(path)
        return path + '\\'
    # возвращает путь до каталога уже существующего
    if isdir_my is True:
        return path + '\\'


# smtp
letter = """текст сообщения привет это пробное письмо смтп"""
letter = letter.encode("UTF-8")
def send_email():
    server = smtplib.SMTP_SSL('smtp.yandex.kz:465')
    server.login(email_login, email_password)
    server.sendmail(email_login, 'jordialba1995@gmail.com', letter)
    server.quit()


# fio
def validate_fio(string_fio: str):
    fio_regex = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', string_fio)
    if len(fio_regex) > 0:
        return True
    else:
        return False


# ответ на выбранное страхование
def service_choosen():
    pass

