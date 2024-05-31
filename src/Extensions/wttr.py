import aiohttp
from aiogram.types import URLInputFile

whelp_txt = '''<b>Информация о погоде.</b>
/wttr - краткая информация в виде ASCII.
/wfull - подробная информация в виде фото.
<b>Использование:</b>
/wttr Moscow
/wfull New York

<i>Используется API <a href="https://github.com/chubin/wttr.in">wttr.in</a>.</i>'''
ERROR_MESSAGE = '⛔️ <b>Не удалось отправить сообщение.</b> Код ошибки: %(error)s'
        
@dp.message(Command(commands=['wfull','wttr']))
async def wttr_info(message: types.Message):
    place_name = message.text.split(' ', 1)
    if len(place_name) > 1 and place_name[1].isalpha():
        message_loader = await message.reply(LOADING_TEXT, parse_mode='HTML')
        try:
            if place_name[0] == "/wttr":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://wttr.in/{place_name[1]}?m0&T') as wttr_resp:
                        await message_loader.edit_text(f'<code>{await wttr_resp.text()}</code>', parse_mode='HTML')
            if place_name[0] == "/wfull":
                image = URLInputFile(
                    f'https://wttr.in/{place_name}.png',
                    filename="weather-file.png"
                )
                await message.reply_photo(image)
        except Exception as error:
            error_name = error.__class__.__name__
            await message.reply(ERROR_MESSAGE % {"error": f'{error_name}'}, parse_mode="HTML")
            logger.error(f'{error_name}: {error}')
    else:
        await message.reply(whelp_txt, parse_mode='HTML', disable_web_page_preview=True)
