import urllib
import json

# Configs
LIBREY_INSTANCE = 'https://librex.antopie.org/'
LIBREY_INSTANCE_API = urllib.parse.urljoin(LIBREY_INSTANCE, 'api.php?q=%')
# Locales
ERROR_TEXT = "<b>⛔️ Не удалось выполнить поисковой запрос.</b>\n"
ERROR_URLError_TEXT = f"Невозможно подключиться к <a href='{LIBREY_INSTANCE}'>серверу.</a>"
ERROR_JSONDecodeError_TEXT = "Ошибка при обработке JSON-ответа от API."
UNKNOWN_ERROR_REASON = "Неизвестная ошибка. Код ошибки: "

@dp.message(Command(commands='s'))
async def search(message: types.Message):
    msg = await message.reply(LOADING_TEXT, parse_mode="HTML")
    try:
        results_json = json.loads(urllib.request.urlopen(f'{LIBREY_INSTANCE_API}{urllib.parse.quote(message.text.split(" ",1)[1])}').read())
        result_text = ''
        for result in results_json:
            if 'special_response' not in result:
                result_text += f'\n\n<b><a href="{result["url"]}">{result["title"]}</a></b>\n{result["description"]}'
            else:
                result_text += f'\n\n<i><a href="{result["special_response"]["source"]}">{result["special_response"]["response"]}</a></i>'
        await msg.edit_text(result_text, parse_mode='HTML')
    except urllib.error.URLError:
        await msg.edit_text(f"{ERROR_TEXT}{ERROR_URLError_TEXT}", parse_mode="HTML")
    except json.JSONDecodeError:
        await msg.edit_text(f"{ERROR_TEXT}{ERROR_JSONDecodeError_TEXT}", parse_mode="HTML")
    except Exception as error:
        error_name = error.__class__.__name__
        error_context = error.args[0]
        await msg.edit_text(f"{ERROR_TEXT}{UNKNOWN_ERROR_REASON}{error_name}: {error_context}", parse_mode="HTML")
