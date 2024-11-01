# input docs kasko
@router.message(Service_Strahovanie.input_docs_kasko,
                F.content_type == 'document'
                )
async def docs_kasko(message: Message, state: FSMContext):
    user_data = await state.get_data()
    path = make_dir_my(user_data['fio'])
    if message.bot.split('.')[-1] in ['zip', 'rar']:
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
