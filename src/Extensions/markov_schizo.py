from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageTextIsEmpty
from typing import Optional, List

# Locals
RESET_WARNING = 'Внимание: <b>вы не можете обратить это действие!</b>\nУдалить базу?'
RESET_TEXT = 'Сброс...'
BASE_BACKUP_TEXT = 'Резервная копия базы перед сбросом:'
RESET_SUCCESS = 'Сброс завершён.'
CHAT_BASE_DESC = 'База чата:'
I_JUST_SAID_TITLE = 'Я просто сказал:\n\n'
I_SAID_MUCH_TITLE = 'Я много сказал:\n\n'
EMPTY_BASE_ERROR = '⛔️<b>База пока не готова.</b> Повторите попытку позже.'
BOT_IS_SILENT = 'Теперь, для этого чата, бот <b>неактивен</b>.'
BOT_IS_ACTIVE = 'Теперь, для этого чата, бот <b>активен</b>.'

# Config
say_much_cycles = 7
disabled_chats_list = open(f'{config.lists_dir}markov_disabledchats.txt', encoding='utf8').read().split('\n')

reset_menu = types.InlineKeyboardMarkup()
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=yes, callback_data='delete_base'))

@dp.callback_query_handler(lambda c: c.data =='delete_base')
async def del_base(call: types.CallbackQuery, **kwargs):
    await call.message.reply(RESET_TEXT)
    if os.path.exists(f'Bases/{chat_id}.txt'):
        base_file = open(f'Bases/{chat_id}.txt', 'r', encoding='utf8')
        await call.message.reply_document(base_file, caption=BASE_BACKUP_TEXT)
        base_file.close()
        os.remove(f'Bases/{chat_id}.txt')
    else:
        bf = open(f'Bases/{chat_id}.txt', 'w', encoding='utf8')
        bf.write('Hello, world!')
        bf.close()
    await call.message.reply(RESET_SUCCESS)
    await call.message.delete()

@dp.callback_query_handler(text='cancel_delete_base')
async def bot_functionality(call: types.CallbackQuery):
    await call.message.reply(okay_msg)
    await call.message.delete()

@dp.message_handler(commands='reset')
async def reset_base(message: types.Message):
    if message.chat.id != message.from_user.id:
        parameters = f"reset_{message.chat.id}"
        await rights_check(message, parameters)
    else:
        global chat_id
        chat_id = message.chat.id
        await message.reply(RESET_WARNING, parse_mode='HTML', reply_markup=reset_menu)

async def reset_link(message: types.Message, parameters: Optional[List[str]] = None):
        member = await bot.get_chat_member(int(parameters[1]), message.from_user.id)
        if member.status == types.ChatMemberStatus.CREATOR:
            global chat_id
            chat_id = parameters[1]
            await message.reply(RESET_WARNING, parse_mode='HTML', reply_markup=reset_menu)
        else:
            await message.reply(change_info_error, parse_mode='HTML')
command_handlers["reset"] = reset_link

@dp.message_handler(commands='getchatbase')
async def get_local_base(message: types.Message):
    if message.chat.id != message.from_user.id:
        parameters = f"get-chat-base_{message.chat.id}"
        await rights_check(message, parameters)
    else:
        try:
            base_file = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(base_file, caption=CHAT_BASE_DESC)
            base_file.close()
        except:
            bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
            bf.write('Hello World!·')
            bf.close()
            base_file = open('Bases/' + str(message.chat.id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(base_file, caption=CHAT_BASE_DESC)
            base_file.close()

async def get_local_base(message: types.Message, parameters: Optional[List[str]] = None):
    chat_id = parameters[1]
    member = await bot.get_chat_member(int(parameters[1]), message.from_user.id)
    if member.status == types.ChatMemberStatus.CREATOR:
        try:
            base_file = open('Bases/' + str(chat_id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(base_file, caption=CHAT_BASE_DESC)
            base_file.close()
        except:
            bf = open('Bases/' + str(chat_id) + '.txt', 'w', encoding='utf8')
            bf.write('Hello World!·')
            bf.close()
            base_file = open('Bases/' + str(chat_id) + '.txt', 'r', encoding='utf8')
            await message.reply_document(base_file, caption=CHAT_BASE_DESC)
            base_file.close()
    else:
        await message.reply(change_info_error, parse_mode="HTML")
command_handlers["get-chat-base"] = get_local_base

@dp.message_handler(commands='saymuch')
async def say_much(message: types.Message):
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
        await bot.send_message(config.logs_channel_id, I_SAID_MUCH_TITLE + generated_text)

@dp.message_handler(commands=['justsay','say'])
async def just_say(message: types.Message):
    try:
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
            await bot.send_message(config.logs_channel_id, I_JUST_SAID_TITLE + generated_text)
    except MessageTextIsEmpty:
        await message.reply(EMPTY_BASE_ERROR, parse_mode='HTML')

@dp.message_handler(commands='botonoff')
async def toggle_bot_for_chat(message: types.Message):
    if await check_change_info_permission(message):
        if str(message.chat.id) in disabled_chats_list:
            disabled_chats_list.remove(str(message.chat.id))
            dc_list = open(f'{config.lists_dir}markov_disabledchats.txt', 'w', encoding='utf8')
            for ids in disabled_chats_list:
                dc_list.write('%s\n' %ids)
            await message.reply(BOT_IS_ACTIVE, parse_mode='HTML')
        else:
            disabled_chats_list.append(str(message.chat.id))
            dc_list = open(f'{config.lists_dir}markov_disabledchats.txt', 'w', encoding='utf8')
            for ids in disabled_chats_list:
                dc_list.write('%s\n' %ids)
            await message.reply(BOT_IS_SILENT, parse_mode='HTML')
    else:
        await message.reply(change_info_error, parse_mode='HTML')
