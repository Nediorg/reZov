
# Locals
bot_base_warn = "\n\n<b>ВНИМАНИЕ:</b> Мы не несем ответственности за информацию, хранящуюся в базе бота, так как она заполняется пользователями."
use_bot_base = 'Теперь, чат использует <b>базу бота.</b>' + bot_base_warn
use_chat_base = 'Теперь, бот использует <b>локальную</b> базу.'
bot_is_silent = 'Теперь, для этого чата, бот <b>неактивен</b>.'
bot_is_active = 'Теперь, для этого чата, бот <b>активен</b>.'
logs_disabled = 'Теперь, для этого чата, логи <b>отключены</b>. Но имейте в виду, что информация о сообщениях все равно собирается внутри бота и отключить ее <b>нельзя.</b> '
logs_enabled = 'Теперь, для этого чата, логи <b>включены</b>.'
reset_warning = '<b>!!! ВЫ НЕ МОЖЕТЕ ОТМЕНИТЬ ЭТО ДЕЙСТВИЕ !!!</b>\n\nВы хотите продолжить??'
reset_msg = 'Сброс...'
base_backup = 'Резервная копия базы перед сбросом:'
reset_ok = 'Сброс завершён.'
disable_phrase_usage = 'Использование:\n\n/enable (или /disable)\n[phrase]'
already_disabled = 'Уже отключено.'
already_enabled = 'Уже включено.'
dplist_caption = 'Файл с отклонёнными фразами:'
no_disabled_phrases = 'Нет отклонённых фраз.'

reset_menu = types.InlineKeyboardMarkup()
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=no, callback_data='cancel_delete_base'))
reset_menu.row(types.InlineKeyboardButton(text=yes, callback_data='delete_base'))

@dp.callback_query_handler(text='delete_base')
async def del_base(call: types.CallbackQuery):
    await call.message.reply(reset_msg)
    if os.path.exists(f'Bases/{call.message.chat.id}.txt'):
        base_file = open(f'Bases/{call.message.chat.id}.txt', 'r', encoding='utf8')
        await call.message.reply_document(base_file, caption=base_backup)
        base_file.close()
        os.remove(f'Bases/{call.message.chat.id}.txt')
    else:
        bf = open(f'Bases/{call.message.chat.id}.txt', 'w', encoding='utf8')
        bf.write('Hello, world!')
        bf.close()
    await call.message.reply(reset_ok)
    await call.message.delete()

@dp.callback_query_handler(text='cancel_delete_base')
async def bot_functionality(call: types.CallbackQuery):
    await call.message.reply(okay_msg)
    await call.message.delete()

@dp.message_handler(commands='botonoff')
async def toggle_bot_for_chat(message: types.Message):
    if await check_change_info_permission(message):
        if str(message.chat.id) in disabled_chats_list:
            disabled_chats_list.remove(str(message.chat.id))
            dc_list = open(f'{config.lists_dir}disabledchats.txt', 'w', encoding='utf8')
            for ids in disabled_chats_list:
                dc_list.write('%s\n' %ids)
            await message.reply(bot_is_active, parse_mode='HTML')
        else:
            disabled_chats_list.append(str(message.chat.id))
            dc_list = open(f'{config.lists_dir}disabledchats.txt', 'w', encoding='utf8')
            for ids in disabled_chats_list:
                dc_list.write('%s\n' %ids)
            await message.reply(bot_is_silent, parse_mode='HTML')
    else:
        await message.reply(change_info_error, parse_mode='HTML')

@dp.message_handler(commands='basemode')
async def toggle_global_and_local_base(message: types.Message):
    if await check_change_info_permission(message):
        if str(message.chat.id) in bot_base_chats_list:
            if not os.path.exists('Bases/' + str(message.chat.id) + '.txt'):
                bf = open('Bases/' + str(message.chat.id) + '.txt', 'w', encoding='utf8')
                bf.write('Hello World!·')
            bot_base_chats_list.remove(str(message.chat.id))
            bbc_list = open(f'{config.lists_dir}botbasechats.txt', 'w', encoding='utf8')
            for ids in bot_base_chats_list:
                bbc_list.write('%s\n' %ids)
            await message.reply(use_chat_base, parse_mode='HTML')
        else:
            bot_base_chats_list.append(str(message.chat.id))
            bbc_list = open(f'{config.lists_dir}botbasechats.txt', 'w', encoding='utf8')
            for ids in bot_base_chats_list:
                bbc_list.write('%s\n' %ids)
            await message.reply(use_bot_base, parse_mode='HTML')
    else:
        await message.reply(change_info_error, parse_mode='HTML')

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

@dp.message_handler(commands='reset')
async def reset_base(message: types.Message):
    if await check_change_info_permission(message) == True:
        await message.reply(reset_warning, parse_mode='HTML', reply_markup=reset_menu)
    else:
        await message.reply(change_info_error, parse_mode='HTML')

@dp.message_handler(commands='disable')
async def disable_reply_to_phrase(message: types.Message):
    if not os.path.exists(f'NotRepliedPhrases/{message.chat.id}.txt'):
        open(f'NotRepliedPhrases/{message.chat.id}.txt', 'w').write('.')
    args_list = message.text.split('\n')
    if len(args_list) != 2 or args_list[1] == '':
        await message.reply(disable_phrase_usage)
    else:
        if await check_change_info_permission(message) == True:
            if args_list[1] not in open(f'NotRepliedPhrases/{message.chat.id}.txt', 'r').read().split('\n'):
                disabled_phrases = open(f'NotRepliedPhrases/{message.chat.id}.txt', 'a', encoding='utf8')
                disabled_phrases.write(args_list[1] + '\n')
                disabled_phrases.close()
                await message.reply(okay_msg)
            else:
                await message.reply(already_disabled)

@dp.message_handler(commands='enable')
async def enable_reply_to_phrase(message: types.Message):
    if not os.path.exists(f'NotRepliedPhrases/{message.chat.id}.txt'):
        open(f'NotRepliedPhrases/{message.chat.id}.txt', 'w').write('.')
    args_list = message.text.split('\n')
    if len(args_list) != 2 or args_list[1] == '':
        await message.reply(disable_phrase_usage)
    else:
        if await check_change_info_permission(message) == True:
            disabled_phrases_list = open(f'NotRepliedPhrases/{message.chat.id}.txt', 'r').read().split('\n')
            if args_list[1] in disabled_phrases_list:
                disabled_phrases_list.remove(args_list[1])
                disabled_phrases_list = [x for x in disabled_phrases_list if x]
                disabled_phrases_file = open(f'NotRepliedPhrases/{message.chat.id}.txt', 'w')
                for phrase in disabled_phrases_list:
                    disabled_phrases_file.write("%s\n" % phrase)
                await message.reply(okay_msg)
            else:
                await message.reply(already_enabled)

@dp.message_handler(commands='dplist')
async def show_disabled_phrases(message: types.Message):
    if not os.path.exists(f'NotRepliedPhrases/{message.chat.id}.txt'):
        open(f'NotRepliedPhrases/{message.chat.id}.txt', 'w').write('.')
    try:
        await message.reply_document(open(f'NotRepliedPhrases/{message.chat.id}.txt', 'r'), caption=dplist_caption)
    except:
        await message.reply(no_disabled_phrases)


