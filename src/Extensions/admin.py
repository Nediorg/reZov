import os, signal
# Broadcast
test_message = "<b>⚠ Внимание!</b>\n<b>Это тестовое сообщение.</b> Если вы видите его, это нормально."
broadcasting = '<i>Отправка...</i>'
broadcasting_test_message = '<i>Отправка тестового сообщения...</i>'
broadcast_warn = '<b>⚠ Внимание!</b>\n'

# Silentcast
silentcasting = '<i>Отправка...</i>'
silentcasting_test_message = '<i>Отправка скрытого объявления......</i>'
silentcast_warn = ''
silent_test_message = "<b>Это тестовое сообщение.</b> Если вы видите его, это нормально."
error_txt = "⛔<b>У вас недостаточно прав для выполнения данной команды.</b>"

# BLACKLIST
blk_success = 'Пользователь успешно добавлен в черный список.'
unblk_success = 'Пользователь успешно удалён из черного списка.'
blk_error = '⛔<b>Не удалось добавить в черный список:</b>'
unblk_error = '⛔<b>Не удалось удалить из черного списка:</b>'
wrnguid = '<b>Неверные данные.<b/>\nПопробуйте ввести в виде "@username" или "-***********" (user id).'
@dp.message_handler(commands='broadcast')
async def broadcast(message: types.Message):
    if message.from_user.id in config.admins and message.text != '/broadcast' and message.text != '/broadcast test':
        await message.answer(broadcasting, parse_mode='HTML')
        chats_list = os.listdir('Bases/')
        chats_list.remove('botbase.txt')
        for chat in chats_list:
            try:
                await bot.send_message(int(chat[:-4]), f'{broadcast_warn}{message.text[message.entities[0].length:]}', parse_mode=types.ParseMode.HTML)
            except:
                pass
    else:
     await message.reply(error_txt, parse_mode='HTML')
    if message.from_user.id in config.admins and message.text == '/broadcast test':
        await message.answer(broadcasting_test_message, parse_mode='HTML')
        chats_list = os.listdir('Bases/')
        chats_list.remove('botbase.txt')
        for chat in chats_list:
            try:
                await bot.send_message(int(chat[:-4]), test_message, parse_mode='HTML')
            except:
                pass
                

@dp.message_handler(commands='silentcast')
async def silentcast(message: types.Message):
    if message.from_user.id in config.admins and message.text != '/silentcast' and message.text != '/silentcast test':
        await message.answer(broadcasting, parse_mode='HTML')
        chats_list = os.listdir('Bases/')
        chats_list.remove('botbase.txt')
        for chat in chats_list:
            try:
                await bot.send_message(int(chat[:-4]), f'{message.text[message.entities[0].length:]}', parse_mode=types.ParseMode.HTML)
            except:
                pass
    if message.from_user.id in config.admins and message.text == '/silentcast test':
        await message.answer(silentcasting_test_message, parse_mode='HTML')
        chats_list = os.listdir('Bases/')
        chats_list.remove('botbase.txt')
        for chat in chats_list:
            try:
                await bot.send_message(int(chat[:-4]), silent_test_message, parse_mode='HTML')
            except:
                pass
