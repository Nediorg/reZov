from aiogram.utils.exceptions import MessageTextIsEmpty

# Config
say_much_cycles = 7

# Locals
i_just_said_title = 'Я просто сказал:\n\n'
i_said_much_title = 'Я много сказал:\n\n'
emptysay = '⛔<b>База пока не готова.</b> Повторите попытку позже.'

@dp.message_handler(commands='saymuch')
async def say_much(message: types.Message):
    if str(message.chat.id) in bot_base_chats_list:
        with open(path_to_base, encoding='utf8') as bfile:
            txt = bfile.read().split('·')
    else:
        if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
            bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
            bf.write('Hello World!·')
        with open('Bases/' + str(message.chat.id) + '.txt', encoding='utf8') as bfile:
            txt = bfile.read().split('·')
    generated_text = ''
    for mgt in range(say_much_cycles):
        generated_now_text = PhraseGenerator(samples=txt).generate_phrase()
        generated_text += ' ' + generated_now_text
        generated_text.replace('@', '[at]')
    await message.reply(generated_text)
    await update_stats(message)
    if str(message.chat.id) not in logs_disabled_chats_list:
        await bot.send_message(config.logs_channel_id, i_said_much_title + generated_text)

@dp.message_handler(commands=['justsay','say'])
async def just_say(message: types.Message):
    try:
        if str(message.chat.id) in bot_base_chats_list:
            with open(path_to_base, encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        else:
            if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                bf.write('Hello World!·')
            with open('Bases/' + str(message.chat.id) + '.txt', encoding='utf8') as bfile:
                txt = bfile.read().split('·')
        generated_text = PhraseGenerator(samples=txt).generate_phrase()
        generated_text.replace('@', '[at]')
        await message.reply(generated_text)
        await update_stats(message)
        if str(message.chat.id) not in logs_disabled_chats_list:
            await bot.send_message(config.logs_channel_id, i_just_said_title + generated_text)
    except MessageTextIsEmpty:
        await message.reply(emptysay, parse_mode='HTML')