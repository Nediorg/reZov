# Locals
chat_base_desc = 'База чата:'
bot_base_desc = 'База бота:'
news_msg = 'Выберите канал'
blog_btn = 'Наш блог'
news_btn = 'Наши логи (недоступно)'

# Config
news_btn_menu = types.InlineKeyboardMarkup(row_width=1)
news_btns = [types.InlineKeyboardButton(text=blog_btn, url='https://t.me/' + config.news_channel), types.InlineKeyboardButton(text=news_btn, url='https://t.me/' + config.logs_channel)]
news_btn_menu.add(*news_btns)

@dp.message_handler(commands=['getlogs', 'news'])
async def get_news(message: types.Message):
    await message.reply(news_msg, reply_markup=news_btn_menu)

@dp.message_handler(commands='getbotbase')
async def get_bot_base(message: types.Message):
    base_file = open(config.path_to_base, 'r', encoding='utf8')
    await message.reply_document(base_file, caption=bot_base_desc)
    base_file.close()

@dp.message_handler(commands='getchatbase')
async def get_local_base(message: types.Message):
    try:
        base_file = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
        await message.reply_document(base_file, caption=chat_base_desc)
        base_file.close()
    except:
        bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
        bf.write('Hello World!·')
        bf.close()
        base_file = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
        await message.reply_document(base_file, caption=chat_base_desc)
        base_file.close()
