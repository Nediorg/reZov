import psutil, cpuinfo
from psutil._common import bytes2human

cpu_name = cpuinfo.get_cpu_info()['brand_raw']

# Locals
bot_ver_title = 'Версия бота:'
platform_title = 'Платформа:'
python_ver_title = 'Версия Python:'
pong_msg = 'Понг!'
all_gen_msgs_title = 'Сообщений сгенерировано:'
chat_gen_msgs_title = 'Сообщений сгенерировано в этом чате:'
user_gen_msgs_title = 'Сообщений сгенерировано в чате с пользователем:'
cpu_use_title = 'Нагрузка на ЦП:'
cores_title = 'ядер:'
threads_title = 'потоков:'
ram_use_title = 'Использование ОЗУ:'
cpu_info = '<b>ЦП:</b>'
total_ram_title = 'всего:'
modules_title = 'Расширений:'
uptime_title = 'Поднят:'
chat_level_title = 'Уровень чата:'
user_level_title = 'Уровень пользователя:'
gen_msgs_info = '<b>*</b> - включает в себя цитаты, шутки и простые сгенерированные сообщения.'

async def get_chat_level(message):
    chat_gen_msgs_num = open(f'{config.stats_dir}{message.chat.id}.txt', 'r', encoding='utf8').read()
    chat_num_compare = config.levels.copy()
    chat_num_compare.append(int(chat_gen_msgs_num) + 1)
    chat_num_compare.sort()
    return chat_num_compare.index(int(chat_gen_msgs_num) + 1)
    chat_gen_msgs_num.close()

async def get_user_level(message):
    user_gen_msgs_num = open(f'{config.stats_dir}{message.from_user.id}.txt', 'r', encoding='utf8').read()
    user_num_compare = config.levels.copy()
    user_num_compare.append(int(user_gen_msgs_num) + 1)
    user_num_compare.sort()
    return user_num_compare.index(int(user_gen_msgs_num) + 1)
    user_gen_msgs_num.close()

@dp.message_handler(commands='ping')
async def bot_ping(message: types.Message):
    await message.reply(pong_msg)

@dp.message_handler(commands='stats')
async def get_stats(message: types.Message):
    if await check_bl_wl(message):
        if not os.path.exists(f'{config.stats_dir}{message.chat.id}.txt'):
            open(f'{config.stats_dir}{message.chat.id}.txt', 'w').write('0')
        if not os.path.exists(f'{config.stats_dir}{message.from_user.id}.txt'):
            open(f'{config.stats_dir}{message.from_user.id}.txt', 'w').write('0')
        all_gen_msgs_num = open(config.path_to_num_of_all_gen_msgs, 'r', encoding='utf8').read()
        chat_gen_msgs_num = open(f'{config.stats_dir}{message.chat.id}.txt', 'r', encoding='utf8').read()
        user_gen_msgs_num = open(f'{config.stats_dir}{message.from_user.id}.txt', 'r', encoding='utf8').read()
        user_level = await get_user_level(message)
        chat_level = await get_chat_level(message)
        if message.chat.id == message.from_user.id:
            bot_info = f'<b>{all_gen_msgs_title}</b> {all_gen_msgs_num}*\n<b>{user_gen_msgs_title}</b> {user_gen_msgs_num}*\n<b>{user_level_title}</b> {user_level} - {config.level_names[user_level - 1]}\n\n{gen_msgs_info}'
        else:
            bot_info = f'<b>{all_gen_msgs_title}</b> {all_gen_msgs_num}*\n<b>{chat_gen_msgs_title}</b> {chat_gen_msgs_num}*\n<b>{user_gen_msgs_title}</b> {user_gen_msgs_num}*\n<b>{chat_level_title}</b> {chat_level} - {config.level_names[chat_level - 1]}\n<b>{user_level_title}</b> {user_level} - {config.level_names[user_level - 1]}\n\n{gen_msgs_info}'
        await message.reply(bot_info, parse_mode='HTML')
    else:
        await message.reply(not_allowed_msg, parse_mode='HTML', reply_markup=contact_with_admin_menu)

@dp.message_handler(commands='info')
async def get_bot_info(message: types.Message):
    if await check_bl_wl(message):
        bot_info = f'<b>{bot_ver_title}</b> {bot_ver}\n<b>{platform_title}</b> {system()} {release()}\n<b>{python_ver_title}</b> {version}\n<b>{cpu_use_title}</b> {psutil.cpu_percent()}%\n<i>{cpu_info} {cpu_name} ({cores_title} {psutil.cpu_count(logical=False)}, {threads_title} {psutil.cpu_count(logical=True)})</i>\n<b>{ram_use_title}</b> {psutil.virtual_memory()[2]}% <i>({total_ram_title} {bytes2human(psutil.virtual_memory().total)})</i>\n<b>{uptime_title}</b> {timedelta(seconds=int(time.time() - start_time))}\n<b>{modules_title}</b> {len(list(config.extensions_dir))}'
        await message.reply(bot_info, parse_mode='HTML')
    else:
        await message.reply(not_allowed_msg, parse_mode='HTML', reply_markup=contact_with_admin_menu)
