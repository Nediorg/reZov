LANG_CODE = "ru" # language code for wikipedia (english - "en")

NO_EVENTS_ERROR = "⛔️ <b>Не удалось получить информацию.</b>"
API_ERROR = "⛔️ <b>Ошибка API Wikipedia. Подождите и повторите попытку.</b>"
WIKI_INFO_TEXT = f'\n<i>Данные взяты из <b><a href="{LANG_CODE}.wikipedia.org">Википедии.</a></b></i>'
LOADING_TEXT = "⏳ <b>Подождите...</b>"
AT_THIS_DAY_TEXT = "в этот день"

THEMES_API_LIST = ["births", "events", "holidays"] # for API
THEMES_TEXT_LIST = ["Дни рождения", "События", "Праздники"] # for message

import requests
import datetime
import random
from typing import Optional, List

@dp.message_handler(commands='today')
async def today(message: types.Message):
    THEME_API = random.choice(THEMES_API_LIST)
    await on_this_day(message, THEME_API)

def today_facts(THEME_API, DATA, MONTH, DAY):
    THEME_NAME = THEMES_TEXT_LIST[THEMES_API_LIST.index(THEME_API)]

    try:
        EVENTS = DATA[THEME_API]
    except KeyError:
        return 1

    FACT = f"🗓 <b>{THEME_NAME} {AT_THIS_DAY_TEXT}</b> ({MONTH}/{DAY}):\n\n"
    for i in range(min(5, len(EVENTS))):
        try:
            FACT += f'· <a href="{EVENTS[i]["pages"][0]["content_urls"]["desktop"]["page"]}">{EVENTS[i]["text"]}</a>\n'
        except IndexError:
            FACT += f'· {EVENTS[i]["text"]}\n'
    return FACT

async def on_this_day(message: types.Message, THEME_API: Optional[List[str]] = None):
    THEME_NAME = THEMES_TEXT_LIST[THEMES_API_LIST.index(THEME_API)]
    global msg, MONTH, DAY

    msg = await message.reply(text=LOADING_TEXT, parse_mode="HTML")

    date = datetime.date.today()
    MONTH = str(date.month).zfill(2)
    DAY = str(date.day).zfill(2)

    url = f'https://{LANG_CODE}.wikipedia.org/api/rest_v1/feed/onthisday/{THEME_API}/{MONTH}/{DAY}'

    try:
        response = requests.get(url)
    except ConnectionError:
        await wait_message.edit_text(text=API_ERROR, parse_mode='HTML')

    global DATA
    DATA = response.json()
    facts = today_facts(THEME_API, DATA, MONTH, DAY)

    if facts == 1:
        await msg.edit_text(text=NO_EVENTS_ERROR, parse_mode='HTML')
    else:
        await msg.edit_text(text=today_facts(THEME_API, DATA, MONTH, DAY) + WIKI_INFO_TEXT, parse_mode='HTML', disable_web_page_preview=True)
