# Locals
man_not_found = 'Информация о команде не найдена.'
lhelp_txt = '<b>Выводит полный список справок команд.</b>\nИспользование: /listman'
mhelp_txt = '<b>Выводит справочную информацию о команде.</b>\nИспользование: /man [команда]'

import os

if not os.path.exists(f'{config.extensions_dir}/man/'):
    os.mkdir(f'{config.extensions_dir}/man/')

@dp.message_handler(commands='man')
async def get_manual(message: types.Message):
    try:
        if not os.path.exists(f'{config.extensions_dir}/man/{message.text[5:]}') or '..' in message.text:
            await message.reply(man_not_found)
        if os.path.exists(f'{config.extensions_dir}/man/{message.text[5:]}') and '..' not in message.text:
            await message.reply(open(f'{config.extensions_dir}/man/{message.text[5:]}').read())
    except IsADirectoryError:
        await message.reply(mhelp_txt, parse_mode='HTML')    
@dp.message_handler(commands='listman')
async def get_manuals_list(message: types.Message):
    try:
        man_list = ''
        for man in os.listdir(f'{config.extensions_dir}/man/'):
            man_list += f'- {man}\n'
        await message.reply(f'{man_list}\n/man [man_name]')
    except IsADirectoryError:
        await message.reply(mhelp_txt, parse_mode='HTML')  