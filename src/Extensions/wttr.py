import aiohttp

WTTR_HELP = '<b>Выводит краткую информацию о погоде в введённом месте.</b>\nИспользование: /wttr [место]\nПример: /wttr Moscow'
WFULL_HELP = '<b>Выводит подробную информацию о погоде в введённом месте.</b>\nИспользование: /wfull [место]\nПример: /wttr Moscow'

LANG_CODE = 'ru'

@dp.message_handler(commands='wttr')
async def wttr_in(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        if message.text[6:].isalpha():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://wttr.in/{message.text[6:]}?m0&T&lang={LANG_CODE}') as wttr_resp:
                    await message.reply(f'<code>{await wttr_resp.text()}</code>', parse_mode='HTML')
    else:
        await message.reply(WTTR_HELP, parse_mode='HTML')
        
@dp.message_handler(commands='wfull')
async def wttr_in_full(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        if message.text[7:].isalpha():
            wttr_media = types.MediaGroup()
            wttr_media.attach_photo(f'https://wttr.in/{message.text[7:]}.png?lang={LANG_CODE}')
            await message.reply_media_group(media=wttr_media)
    else:
        await message.reply(WFULL_HELP, parse_mode='HTML')
