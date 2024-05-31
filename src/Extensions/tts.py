from gtts import gTTS
import langid
from aiogram.types import FSInputFile
import tempfile

HELP_TEXT = '<b>Данная команда озвучивает ваш текст.</b>\nИспользование: /tts [текст]'
ERROR_TEXT = '⛔️<b>Не удалось озвучить текст.</b>\n'
LangDetectException_TEXT = 'В тексте нет поддерживаемых символов.'

@dp.message(Command(commands='tts'))
async def tts_handler(message: types.Message):
    if len(message.text.split(maxsplit=1)) > 1:
        input_tts = message.text.split(maxsplit=1)[1]
        lang = langid.classify(input_tts)[0]
        try:
            tts = gTTS(input_tts, lang=lang)
        except ValueError:
            tts = gTTS(input_tts, lang='en')
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tts.save(tmp.name)
            voice_file = FSInputFile(tmp.name)
        await bot.send_voice(message.chat.id, voice_file)
    else:
        await message.reply(HELP_TEXT, parse_mode='HTML')
