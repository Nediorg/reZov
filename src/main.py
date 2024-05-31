import os, random, config, mc, requests
from local import *
from aiogram import Bot, Dispatcher, executor, types
from platform import system, release
from sys import version
from mc import PhraseGenerator
from loguru import logger
from itertools import groupby
from datetime import timedelta
import time
import base64

bot = Bot(token=config.token)
dp = Dispatcher(bot)

logger.add(config.path_to_log, level='DEBUG')

build_code = 'voZer by lunee and nekondrashov, reZov by nediorg'

print(f'{splash}{build_code}\n')

logger.info('Initialization...')

start_time = time.time()

def read_ff(file): # Read from file
    try:
        module_file = open(file, 'r', encoding='UTF-8')
        Contents = module_file.read()
        module_file.close()
        return Contents
    except:
        return None

async def check_bl_wl(message): # Check black/whitelist
    if config.blacklist == 0 and str(message.chat.id) in whitelist and str(message.from_user.id) in whitelist or config.blacklist == 1 and str(message.chat.id) not in blacklist and str(message.from_user.id) not in blacklist:
        return True
    else:
        await message.reply(not_allowed_msg, parse_mode='HTML', reply_markup=contact_with_admin_menu)
        return False

async def check_change_info_permission(message):
    member_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if member_info.status != "member" and member_info.can_change_info == True or message.chat.id == message.from_user.id:
        return True
    else:
        return False
        await message.reply(change_info_error)

async def update_stats(message):
    with open(config.path_to_num_of_all_gen_msgs, 'r', encoding='utf8') as gen_msgs_num_file:
        new_num = str(int(gen_msgs_num_file.read()) + 1)
    with open(config.path_to_num_of_all_gen_msgs, 'w', encoding='utf8') as gen_msgs_num_file:
        gen_msgs_num_file.write(new_num)
    if not os.path.exists(f'{config.stats_dir}{message.chat.id}.txt'):
        open(f'{config.stats_dir}{message.chat.id}.txt', 'w').write('0')
    if message.chat.id != message.from_user.id:
        with open(f'{config.stats_dir}{message.chat.id}.txt', 'r', encoding='utf8') as gen_msgs_num_file:
            new_num = str(int(gen_msgs_num_file.read()) + 1)
        with open(f'{config.stats_dir}{message.chat.id}.txt', 'w', encoding='utf8') as gen_msgs_num_file:
            gen_msgs_num_file.write(new_num)
        if int(new_num) in config.levels:
            await message.reply(f'Now, you are on <b>level {config.levels.index(msg_num) + 1} - {config.level_names[config.levels.index(msg_num)]}!</b>', parse_mode='HTML')
    if not os.path.exists(f'{config.stats_dir}{message.from_user.id}.txt'):
        open(f'{config.stats_dir}{message.from_user.id}.txt', 'w').write('0')
    with open(f'{config.stats_dir}{message.from_user.id}.txt', 'r', encoding='utf8') as gen_msgs_num_file:
        new_num = str(int(gen_msgs_num_file.read()) + 1)
    with open(f'{config.stats_dir}{message.from_user.id}.txt', 'w', encoding='utf8') as gen_msgs_num_file:
        gen_msgs_num_file.write(new_num)
    if int(new_num) in config.levels:
        new_lvl = config.levels.index(int(new_num)) + 1
        new_lvl_name = config.level_names[new_lvl - 1]
        await message.reply(f'<b>Поздравляем, {message.from_user.full_name}! Теперь, твой уровень {new_lvl} - {new_lvl_name}</b>', parse_mode='HTML')

logger.info('Loading files and directories...')
if not os.path.exists(config.lists_dir):
    os.mkdir(config.lists_dir)

for i in range(len(config.lists_files)):
    if not os.path.exists(f'{config.lists_dir}{config.lists_files[i]}'):
        f = open(f'{config.lists_dir}{config.lists_files[i]}', 'w', encoding='utf8')
        f.write('')
        f.close()

if not os.path.exists(config.bases_dir):
    os.mkdir(config.bases_dir)

if not os.path.exists(config.path_to_base):
    f = open(config.path_to_base, 'w', encoding='utf8')
    f.write('Hello World!·')
    f.close()

if not os.path.exists('Logs'):
    os.mkdir('Logs')

if not os.path.exists(config.extensions_dir):
    os.mkdir(config.extensions_dir)

if not os.path.exists(config.stats_dir):
    os.mkdir(config.stats_dir)

if not os.path.exists('NotRepliedPhrases'):
    os.mkdir('NotRepliedPhrases')

if not os.path.exists(config.path_to_num_of_all_gen_msgs):
    f = open(config.path_to_num_of_all_gen_msgs, 'w', encoding='utf8')
    f.write('0')
    f.close()

logger.info('Loading extensions...')
command_handlers = {}
extensions = os.listdir(config.extensions_dir)
for extension in extensions:
    if os.path.isfile(os.path.join(config.extensions_dir, extension)):
        if extension.endswith('.py'):
            if os.stat(os.path.join(config.extensions_dir, extension)).st_size != 0:
                try:
                    logger.info(f'Starting extension "{extension}"...')
                    exec(read_ff(os.path.join(config.extensions_dir, extension)))
                except Exception as e:
                    logger.exception(f'Error initializing extension "{extension}", ignoring')
            else:
                logger.warning(f'Extension "{extension}" is blank, ignoring')
        else:
            logger.warning(f'Extension "{extension}" does not end with .py, ignoring')

logger.info('Loading lists...')
logs_disabled_chats_list = open(f'{config.lists_dir}logsdisabledchats.txt', encoding='utf8').read().split('\n')
chats_list = [x for x in [i for i, _ in groupby(open(f'{config.lists_dir}chatslist', 'r').read().split('\n'))] if x]

if config.blacklist == 1:
    blacklist = open(f'{config.lists_dir}blacklist.txt', encoding='utf8').read().split('\n')
    whitelist = ['']
    not_allowed_msg = blacklisted_msg
else:
    whitelist = open(f'{config.lists_dir}whitelist.txt', encoding='utf8').read().split('\n')
    blacklist = ['']
    not_allowed_msg = not_whitelisted_msg


logger.info('One moment...')
start_menu = types.InlineKeyboardMarkup()
start_menu.row(types.InlineKeyboardButton(text='Исходный код reZov', url='https://github.com/Nediorg/reZov'))
start_menu.row(types.InlineKeyboardButton(text=contact_with_admin_text, callback_data='send_info'))
start_menu.row(types.InlineKeyboardButton(text=prviacy_policy_title, callback_data='privacy_policy'))
start_menu.row(types.InlineKeyboardButton(text=func_button, callback_data='com'))

cat = types.InlineKeyboardMarkup()
cat.row(types.InlineKeyboardButton(text=func_title, callback_data='func_info'))
cat.row(types.InlineKeyboardButton(text=admin_title, callback_data='admin_info'))
cat.row(types.InlineKeyboardButton(text=fun_title, callback_data='fun_info'))

contact_with_admin_menu = types.InlineKeyboardMarkup()
contact_with_admin_menu.add(types.InlineKeyboardButton(text=contact_with_admin_text, url='t.me/' + config.admin_username))
logger.success('Ready!')

@dp.callback_query_handler(text='com')
async def bot_functionality(call: types.CallbackQuery):
        await call.message.reply(comtext, reply_markup=cat)

@dp.callback_query_handler(text='fun_info')
async def fun_inf(call: types.CallbackQuery):
    await call.message.reply(fun_info)

@dp.callback_query_handler(text='func_info')
async def func_inf(call: types.CallbackQuery):
    await call.message.reply(func_info)

@dp.callback_query_handler(text='send_info')
async def func_inf(call: types.CallbackQuery):
    await call.message.reply(send_hlp, parse_mode='HTML')

@dp.callback_query_handler(text='admin_info')
async def admin_inf(call: types.CallbackQuery):
    await call.message.reply(admin_info)

@dp.callback_query_handler(text='privacy_policy')
async def privacy(call: types.CallbackQuery):
    await call.message.reply(privacy_policy_text)

@dp.message_handler(commands=['start', 'help'])
async def get_started(message: types.Message):
    if await check_bl_wl(message):
        args = message.get_args()
        padding_len = len(args) % 4
        args += '=' * padding_len
        decoded = base64.urlsafe_b64decode(args).decode("utf-8")
        parameters = decoded.split("_")
        if not parameters[0]:
            await message.reply(hello_msg, reply_markup=start_menu)
        else:
            command = parameters[0]
            if command in command_handlers:
                handler = command_handlers[command]
                await handler(message, parameters)

@dp.callback_query_handler(text='cancel_rights_check')
async def bot_functionality(call: types.CallbackQuery):
    await call.message.reply(okay_msg)
    await call.message.delete()

async def rights_check(message: types.Message, parameters):
    link = await get_start_link(parameters, encode=True)
    check_permission = types.InlineKeyboardMarkup()
    check_permission.row(types.InlineKeyboardButton(text="Перейти", url=link))
    check_permission.row(types.InlineKeyboardButton(text="Отмена", callback_data='cancel_rights_check'))
    await message.reply(goto_dm_text, parse_mode='HTML', reply_markup=check_permission)

@dp.message_handler(commands='logsmode')
async def toggle_logs(message: types.Message):
    if await check_change_info_permission(message):
        if str(message.chat.id) in logs_disabled_chats_list:
            logs_disabled_chats_list.remove(str(message.chat.id))
            ldc_list = open(f'{config.lists_dir}logsdisabledchats.txt', 'w', encoding='utf8')
            for ids in logs_disabled_chats_list:
                ldc_list.write('%s\n' %ids)
            await message.reply(logs_enabled, parse_mode='HTML')
        else:
            logs_disabled_chats_list.append(str(message.chat.id))
            ldc_list = open(f'{config.lists_dir}logsdisabledchats.txt', 'w', encoding='utf8')
            for ids in logs_disabled_chats_list:
                ldc_list.write('%s\n' %ids)
            await message.reply(logs_disabled, parse_mode='HTML')
    else:
        await message.reply(change_info_error, parse_mode='HTML')

@dp.message()
async def get_text_messages(message: types.Message):
    my_info = await bot.get_me()
    modified_text = filter_messages(message)
    with open(f'Bases/{message.chat.id}.txt', 'a', encoding='utf8') as bfile:
        bfile.write(modified_text + '·')
    try:
        if len(txt) >= 2 and random.randint(1, config.chance) == 1 or message.reply_to_message.from_user.id == my_info.id or message.chat.id == message.from_user.id:
            if str(message.chat.id) not in disabled_chats_list:
                schizo_text = generate_markov_schizo(message)
                await message.reply(schizo_text)
                await update_stats(message)
                if str(message.chat.id) not in logs_disabled_chats_list and config.activate_logs == True:
                    await bot.send_message(config.logs_channel_id, f'{user_msg_title}{message.text} \n---\n\n{bot_answer_title}{generated_text}\n---')
                    log_str = f'{message.from_user.first_name} (ID {message.from_user.id}) (Chat ID {message.chat.id}): {message.text} | Bot answer: {generated_text}'
                    logger.info(log_str)
    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
