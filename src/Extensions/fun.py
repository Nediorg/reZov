# Locals
bricker_warning = 'ни качай эта вирус!!!!1!!!11!1'
ban_warning = 'Под чем ты был, пока писал это? Удаляй при мне.'
# photos = [<telegram media id>]

@dp.message_handler(commands='wtf')
async def wtf_report(message: types.Message):
    if message.chat.id != message.from_user.id:
        await message.reply_to_message.reply(ban_warning)

@dp.message_handler(content_types='file')
async def bricker_warn(message: types.Message):
    await message.reply(bricker_warning)

@dp.message_handler(commands='dice') # Бросает кубик
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
    
@dp.message_handler(commands='casino') # Отправляет стикер с рандомными слотами
async def cmd_cas(message: types.Message):
    await message.answer_dice(emoji="🎰")
    
@dp.message_handler(commands='reward') # Рандомное фото, "выдача награды"
async def rewards(message: types.Message): 
    await message.reply_photo(random.choice(photos))

@dp.message_handler(commands="fun")
async def cmd_fun(message: types.Message):
	your_id = message.from_id
	your_name = message.from_user.username
	args = message.text.split(' ', maxsplit=2)
	com = args[1]
	if com == 'поцеловать':
		act = 'поцеловал(а)'
	if com == 'обосрать':
		act = 'обосрал(а)'
	if com == 'ударить':
		act = 'ударил(а)'
	if com == 'обоссать':
		act = 'обоссал(а)'
	if com == 'обнять':
		act = 'обнял(а)'
	if com == 'сьесть' or com == 'съесть':
		act = 'съел(а)'
	if com == 'забанить' or com == 'заблокировать' or com == 'бан':
		act = 'заблокировал(а)'	
	try:
		friend_name = message.reply_to_message.from_user.username
		friend_id = message.reply_to_message.from_user.id
		await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) {act} [@{friend_name}](tg://user?id={str(friend_id)}).', parse_mode="Markdown")
	except:
		await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) всех {act}.', parse_mode="Markdown")

@dp.message_handler(commands=["zablokirovat","blok"])
async def send_handshake(message: types.Message):
    your_id = message.from_id
    your_name = message.from_user.username
    try:
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) заблокировал пользователя [@{friend_name}](tg://user?id={str(friend_id)}).', parse_mode="Markdown")
    except:
        await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) всех забанил.', parse_mode="Markdown")
