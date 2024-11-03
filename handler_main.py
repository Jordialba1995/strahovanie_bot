from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from datetime import *


from keyboards import row_keyboard, services_kb
from bot_functions import make_dir_my, send_email, validate_fio, service_choosen, name_worker
from text import *


# items for keyboars
next_step = ['Далее']
y_n = ['Да', 'Нет']


router = Router()


class Service_Strahovanie(StatesGroup):
    # 0
    zero_state = State()
    # fio
    fio = State()
    save_fio = State()
    successed_fio = State()
    # services
    choose_service = State()
    service_chosen = State()
    # paket dokov
    input_docs = State()
    # name worker
    worker_name = State()
    # ended
    the_end = State()


# start
@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Service_Strahovanie.zero_state)
    await message.answer(
        text=hello_message + '\nНажмите кнопку "Далее" для продолжения работы  с ботом',
        reply_markup=row_keyboard(next_step)
    )
    await state.set_state(Service_Strahovanie.fio)


# fio
@router.message(Service_Strahovanie.fio,
                F.text.in_({'Далее', 'В начало'}))
async def fio(message: Message, state: FSMContext):
    await message.answer(
        text='Введите Фамилию, Имя, Отчество ЧЕРЕЗ ПРОБЕЛ\nПример: Иванов Иван Иванович',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Service_Strahovanie.save_fio)


@router.message(Service_Strahovanie.fio)
async def check_text_fio(message: Message):
    await message.answer(
        text='вы попытались ввести текст, нажмите нужную кнопку'
    )


# save fio
@router.message(Service_Strahovanie.save_fio)
async def save_fio(message: Message, state: FSMContext):
    if validate_fio(message.text):
        await state.update_data(fio=message.text.title())
        await message.answer(
            text=f'Ваше ФИО: {message.text.title()}',
            reply_markup=row_keyboard(y_n)
        )
        await state.set_state(Service_Strahovanie.successed_fio)
    else:
        await message.answer(
            text='Введите КОРРЕКТНУЮ Фамилию, Имя, Отчество через пробел\nПример: Иванов Иван Иванович', parse_mode='HTML')
        await state.set_state(Service_Strahovanie.save_fio)


@router.message(Service_Strahovanie.save_fio)
async def check_text_fio(message: Message):
    await message.answer(
        text='вы попытались ввести текст, нажмите нужную кнопку'
    )


# failed fio
@router.message(Service_Strahovanie.successed_fio,
                F.text == 'Нет')
async def failed_fio(message: Message, state: FSMContext):
    await message.answer(
        text='Введите ФИО еще раз',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Service_Strahovanie.save_fio)


# choose service
@router.message(Service_Strahovanie.successed_fio,
                F.text == 'Да')
async def choosing(message: Message, state: FSMContext):
    user_data = await state.get_data()
    path = make_dir_my(user_data['fio'])
    await state.update_data(path=path)
    await message.answer(
        text='выберите интересующее страхование',
        reply_markup=services_kb()
    )
    await state.set_state(Service_Strahovanie.service_chosen)


@router.message(Service_Strahovanie.successed_fio)
async def check_text_fio(message: Message):
    await message.answer(
        text='вы попытались ввести текст, нажмите нужную кнопку'
    )


# cancel to search services
@router.message(Service_Strahovanie.service_chosen,
    F.text.lower() == 'вернуться')
async def service_cancel(message: Message, state: FSMContext):
    await message.answer(
        text='вернулись к выбору страхования',
        reply_markup=services_kb()
    )
    await state.set_state(Service_Strahovanie.choose_service)


# service already choose
@router.message(Service_Strahovanie.service_chosen,
                F.text.in_(list_services))
async def select_kasko(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    service_need = service_choosen(message.text) # otvet na vibrannoe strahovanie

    await message.answer(
        text=f'отправьте пакет документов для {service_need} одним архивом типа rar и получите условия по услуге',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Service_Strahovanie.input_docs)


@router.message(Service_Strahovanie.service_chosen)
async def check_text_fio(message: Message):
    await message.answer(
        text='выберите страхование'
    )


# input docs
@router.message(Service_Strahovanie.input_docs,
                F.content_type == 'document'
                )
async def docs_kasko(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(user_name_file=message.document.file_name)
    user_filename = message.document.file_name
    path = user_data['path'] # return path dir

    if user_filename.split('.')[-1] in ['zip', 'rar']:
        filename = path + '\\' + datetime.today().strftime('%d%m%Y_%H%M%S') + '_docs1' + '.rar'
        await message.bot.download(file=message.document.file_id, destination=filename)
        await message.answer(
            text='zagruzka docs vipolnena'
        )
        await message.answer(
            text='Нажмите Далее для получения ссылки на сотрудника',
            reply_markup=row_keyboard(next_step)
        )
        await state.set_state(Service_Strahovanie.worker_name)

    else:
        await message.answer(
            text='Загрузите файл с расширением "zip" или "rar"'
        )
        await state.set_state(Service_Strahovanie.input_docs)


# failed input
@router.message(Service_Strahovanie.input_docs)
async def failed_input(message: Message):
    await message.answer(
        text='вы, попытались отправить не документ, попробуйте еще раз'
    )

# name worker + smtp
@router.message(Service_Strahovanie.worker_name,
                F.text.in_(next_step)
                )
async def kasko_worker(message: Message, state: FSMContext):
    user_data = await state.get_data()
    letter = user_data['fio'] + '//' + user_data['service'] + '//' + datetime.today().strftime('%d%m%Y_%H%M%S')
    send_email(letter)

    await message.answer(
        text=f'ssilka na {name_worker(user_data['service'])} sotrudnika',
    )
    await message.answer(
        text='работа с ботом завершена хотите перейти в начало?',
        reply_markup=row_keyboard(['В начало'])
    )
    await state.set_state(Service_Strahovanie.the_end)


# ended
@router.message(Service_Strahovanie.the_end,
                F.text == 'В начало')
async def the_end(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f'{bye_message}\nВведите Фамилию, Имя, Отчество ЧЕРЕЗ ПРОБЕЛ\nПример: Иванов Иван Иванович',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    # await state.set_data({})
    await state.set_state(Service_Strahovanie.save_fio)


