import os
import smtplib
import re

from config_reader import config
from text import *

#  создает новую папку по указанному пути, при условии, что все указанные промежуточные (вложенные) директории уже существуют.
def make_dir_my(driver_fio):
    # cwd need to change after finished
    cwd = r'D:\test\bot_photos'
    path = os.path.join(cwd, driver_fio)
    isdir_my = os.path.isdir(path)
    if isdir_my is False:
        os.mkdir(path)
        return path + '\\'
    # возвращает путь до каталога уже существующего
    if isdir_my is True:
        return path + '\\'


# send mail
email_login = config.email_login.get_secret_value()
email_password = config.email_password.get_secret_value()
email_send_to = config.email_send_to.get_secret_value()

def send_email(letter):
    letter = letter.encode("UTF-8")
    server = smtplib.SMTP_SSL('smtp.yandex.kz:465')
    server.login(email_login, email_password)
    server.sendmail(email_login, email_send_to, letter)
    server.quit()


# fio
def validate_fio(string_fio: str):
    fio_regex = re.findall(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?', string_fio)
    if len(fio_regex) > 0:
        return True
    else:
        return False


# ответ на выбранное страхование
def service_choosen(service):

    if service == list_services[0]:
        return 'пакет документов для каско'

    elif service == list_services[1]:
        return 'пакет документов осаго'

    elif service == list_services[2]:
        return 'пакет документов для несчастных случаев'

    elif service == list_services[3]:
        return 'пакет документов взр'

    elif service == list_services[4]:
        return 'пакет документов дмс'

    elif service == list_services[5]:
        return 'пакет документов недвижка'

    elif service == list_services[6]:
        return 'пакет документов ипотечное'

    elif service == list_services[7]:
        return 'пакет документов крит заболеваний'


def name_worker(service):
    if service == list_services[0]:
        return 'ssilka na sotrudnika для каско'

    elif service == list_services[1]:
        return 'ssilka осаго'

    elif service == list_services[2]:
        return 'ssilka для несчастных случаев'

    elif service == list_services[3]:
        return 'ssilka взр'

    elif service == list_services[4]:
        return 'ssilka дмс'

    elif service == list_services[5]:
        return 'ssilka недвижка'

    elif service == list_services[6]:
        return 'ssilka ипотечное'

    elif service == list_services[7]:
        return 'silka крит заболеваний'
