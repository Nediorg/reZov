# Locals
bricker_warning = 'ни качай эта вирус!!!!1!!!11!1'
ban_warning = 'Под чем ты был, пока писал это? Удаляй при мне.'

@dp.message(Command(commands='wtf'))
async def wtf_report(message: types.Message):
    if message.chat.id != message.from_user.id:
        await message.reply_to_message.reply(ban_warning)

@dp.message(Command(commands=["zablokirovat","blok"]))
async def send_handshake(message: types.Message):
    your_id = message.from_user.id
    your_name = message.from_user.username
    try:
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) заблокировал пользователя [@{friend_name}](tg://user?id={str(friend_id)}).', parse_mode="Markdown")
    except:
        await message.answer(f'[@{your_name}](tg://user?id={str(your_id)}) всех забанил.', parse_mode="Markdown")
