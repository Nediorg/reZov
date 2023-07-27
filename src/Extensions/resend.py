from aiogram.utils.exceptions import ChatNotFound, CantInitiateConversation, BotBlocked

# SEND
send_txt = "<b>Сообщение отправлено администратору reZov.</b>\nПомните: за отправку неподобающих сообщений вы можете <b>получить блокировку.</b>"
sendpm_txt = "Пользователь"
send_title = 'Отправлено админ-ам:\n'
send_hlp = '<b>Отправляет ваше сообщение админ-ам reZov.</b>\nПомните: за отправку неподобающих сообщений вы можете <b>получить блокировку.</b>'
# RESEND
recieved_txt = "<b>❗Сообщение от администраторов reZov:</b>"
logadm_txt = 'Отправлено админом'
success_txt = 'Отправлено!'
# ERRORS: RESEND
norights_txt = "⛔ <b>У вас недостаточно прав для выполнения данной команды.</b>"
wrongid_txt = '⛔ <b>Неверно указан ID.</b> Повторите попытку.'
empty_txt = '⛔ <b>Неверное выполнение команды.</b>'
chatnotfound_txt = '⛔ <b>Чат не найден.</b>'
cic_txt = '⛔ <b>Не удалось отправить сообщение.</b> Возможно, пользователь заблокировал бота.'
blockbot_txt = '⛔ <b>Не удалось отправить сообщение.</b> Пользователь заблокировал бота.'
@dp.message_handler(commands='send')  
async def send_admin(message:types.Message):
    if not len(message.text[6:])==0:
        your_id = message.from_id
        your_name = message.from_user.username
        await message.reply(send_txt, parse_mode='HTML')
        await bot.send_message(config.admin_id, f'<b>{sendpm_txt} <a href="tg://user?id={your_id}">@{your_name}</a> <a href="tg://user?id={your_id}">(ссылка)</a>:</b>\n{message.text[6:]}\n\n<code>/resend {your_id}</code>', parse_mode='HTML')
        logger.info(f'To admins from: {message.from_user.username} (ID: {message.from_id}): {message.text[6:]}')
        await bot.send_message(config.logs_channel_id, f'{send_title}\n<b>{sendpm_txt} <a href="tg://user?id={your_id}">@{your_name}</a> <a href="tg://user?id={your_id}">(ссылка)</a>:</b>\n\n---\n\n{message.text[6:]}', parse_mode='HTML')
    else:
        await message.reply(send_hlp, parse_mode='HTML')         

@dp.message_handler(commands='resend')  
async def resend_admin(message:types.Message):
	if message.from_user.id in config.admins:
		if not len(message.text[8:])==0:
			try:
				args = message.text.split(' ', maxsplit=2)
				sended_id = int(args[1])
				your_id = message.from_id
				await bot.send_message(config.logs_channel_id, f'{logadm_txt} {your_id}:\n\n{args[2]}', parse_mode='HTML')
				logger.info(f'Resended by {your_id}: {args[2]}')
				await bot.send_message(sended_id, f'{recieved_txt}\n\n{args[2]}', parse_mode='HTML')
				await message.reply(success_txt, parse_mode='HTML')
			except ValueError:
				await message.reply(wrongid_txt, parse_mode='HTML')
			except ChatNotFound:
				await message.reply(chatnotfound_txt, parse_mode='HTML')
			except CantInitiateConversation:
				await message.reply(cic_txt, parse_mode='HTML')
			except BotBlocked:
				await message.reply(blockbot_txt, parse_mode='HTML')
		else:
			await message.reply(empty_txt, parse_mode='HTML')         
	else:
		await message.reply(norights_txt, parse_mode='HTML')

@dp.message_handler(commands='sresend')  
async def resend_admin(message:types.Message):
	if message.from_user.id in config.admins:
		if not len(message.text[8:])==0:
			try:
				args = message.text.split(' ', maxsplit=2)
				sended_id = int(args[1])
				your_id = message.from_id
				await bot.send_message(config.logs_channel_id, f'{logadm_txt} {your_id}:\n\n{args[2]}', parse_mode='HTML')
				logger.info(f'Resended by {your_id}: {args[2]}')
				await bot.send_message(sended_id, args[2], parse_mode='HTML')
				await message.reply(success_txt, parse_mode='HTML')
			except ValueError:
				await message.reply(wrongid_txt, parse_mode='HTML')
			except ChatNotFound:
				await message.reply(chatnotfound_txt, parse_mode='HTML')
			except CantInitiateConversation:
				await message.reply(cic_txt, parse_mode='HTML')
			except BotBlocked:
				await message.reply(blockbot_txt, parse_mode='HTML')
		else:
			await message.reply(empty_txt, parse_mode='HTML')         
	else:
		await message.reply(norights_txt, parse_mode='HTML')
