# Configs
librex_instance = 'https://search.davidovski.xyz/api.php?q='

import urllib
from json import loads

@dp.message_handler(commands='s')
async def search(message: types.Message):
    results_json = loads(urllib.request.urlopen(f'{librex_instance}{urllib.parse.quote(message.text[3:])}').read())
    result_text = ''
    for result in results_json:
        if 'special_response' not in result:
            result_text += f'\n\n<b><a href="{result["url"]}">{result["title"]}</a></b>\n{result["description"]}'
        else:
            result_text += f'\n\n<i><a href="{result["special_response"]["source"]}">{result["special_response"]["response"]}</a></i>'
    await message.reply(result_text, parse_mode='HTML')
