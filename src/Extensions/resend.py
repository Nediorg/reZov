from aiogram.utils.exceptions import ChatNotFound, CantInitiateConversation, BotBlocked

# SEND
WARNING_MESSAGE = "Помните: за отправку неподобающих сообщений вы можете <b>получить блокировку.</b>"
SEND_TXT_ADMIN = f"<b>Сообщение отправлено администратору reZov.</b>\n{WARNING_MESSAGE}"
SEND_HLP_ADMIN = f'<b>Отправляет ваше сообщение администраторам reZov.</b>\n{WARNING_MESSAGE}'
DM_ERROR_MESSAGE = 'Эту команду можно выполнить только из ЛС.'

ADMIN_TEMPLATE = '<b>Пользователь <a href="tg://user?id=%(id)s">%(username)s</a>:</b>\n%(msg)s\n\n<code>/resend %(id)s</code>'
ADMIN_LOGS_TEMPLATE = '<b>Отправлено пользователем <a href="tg://user?id=%(id)s">%(username)s</a>:</b>\n\n%(msg)s'

# RESEND
RECEIVED_MESSAGE = "<b>❗️Сообщение от администраторов reZov:</b>\n\n%(msg)s"
ADMIN_SENT_MESSAGE = 'Отправлено админом'
RESENDED_BY_MESSAGE = 'Отправлено админом %(id)s:\n\n%(msg)s'
SUCCESS_MESSAGE = 'Отправлено!'
# ERRORS: RESEND
NO_RIGHTS_MESSAGE = "⛔️ <b>У вас недостаточно прав для выполнения данной команды.</b>"
WRONG_ID_MESSAGE = '⛔️ <b>Неверно указан ID.</b>'
EMPTY_MESSAGE = '⛔️ <b>Неверное выполнение команды.</b>'
CHAT_NOT_FOUND_MESSAGE = '⛔️ <b>Чат не найден.</b>'
ERROR_MESSAGE = '⛔️ <b>Не удалось отправить сообщение.</b> Код ошибки: %(error)s'

@dp.message_handler(commands='send')
async def send_admin(message: types.Message):
    if message.chat.id != message.from_user.id:
        link = await get_start_link("")
        dm_link = types.InlineKeyboardMarkup()
        dm_link.row(types.InlineKeyboardButton(text="Перейти", url=link))
        await message.reply(DM_ERROR_MESSAGE, parse_mode='HTML', reply_markup=dm_link)
    else:
        try:
            args = message.text.split(' ', 1)
            await bot.send_message(config.admin_id, ADMIN_TEMPLATE % {"id": message.from_id, "username": message.from_user.first_name, "msg": args[1]}, parse_mode='HTML')
            await message.reply(SEND_TXT_ADMIN, parse_mode="HTML")
            await bot.send_message(config.logs_channel_id, ADMIN_LOGS_TEMPLATE % {"id": message.from_id, "username": message.from_user.first_name, "msg": args[1]}, parse_mode='HTML')
        except IndexError:
            await message.reply(SEND_HLP_ADMIN, parse_mode='HTML')

@dp.message_handler(commands='resend')
async def resend_admin(message: types.Message):
    if message.from_user.id in config.admins:
        if not len(message.text.split(' ', 1)[1]) == 0:
            try:
                args = message.text.split(' ', 2)
                await bot.send_message(config.logs_channel_id, RESENDED_BY_MESSAGE % {"id": message.from_id, "msg": args[2]}, parse_mode='HTML')
                await bot.send_message(int(args[1]), RECEIVED_MESSAGE % {"msg": args[2]}, parse_mode='HTML')
                await message.reply(SUCCESS_MESSAGE, parse_mode='HTML')
            except ValueError:
                await message.reply(WRONG_ID_MESSAGE, parse_mode='HTML')
            except ChatNotFound:
                await message.reply(CHAT_NOT_FOUND_MESSAGE, parse_mode='HTML')
            except Exception as error:
                error_name = error.__class__.__name__
                error_context = error.args[0]
                await message.reply(ERROR_MESSAGE % {"error": f'{error_name}: {error_context}'}, parse_mode="HTML")
        else:
            await message.reply(EMPTY_MESSAGE, parse_mode='HTML')
    else:
        await message.reply(NO_RIGHTS_MESSAGE, parse_mode='HTML')
