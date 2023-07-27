import aiohttp

whelp_txt = '<b>Выводит краткую информацию о погоде в введённом месте.</b>\nИспользование: /wttr [место]\nПример: /wttr Moscow'
wfhelp_txt = '<b>Выводит подробную информацию о погоде в введённом месте.</b>\nИспользование: /wfull [место]\nПример: /wttr Moscow'

@dp.message_handler(commands='wttr')
async def wttr_in(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        if message.text[6:].isalpha():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://wttr.in/{message.text[6:]}?m0&T') as wttr_resp:
                    await message.reply(f'<code>{await wttr_resp.text()}</code>', parse_mode='HTML')
    else:
        await message.reply(whelp_txt, parse_mode='HTML')
        
@dp.message_handler(commands='wfull')
async def wttr_in_full(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        if message.text[7:].isalpha():
            wttr_media = types.MediaGroup()
            wttr_media.attach_photo(f'https://wttr.in/{message.text[7:]}.png')
            await message.reply_media_group(media=wttr_media)
    else:
        await message.reply(wfhelp_txt, parse_mode='HTML')