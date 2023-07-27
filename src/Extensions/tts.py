from gtts import gTTS
from langdetect import detect

help_txt = '<b>Данная команда озвучивает ваш текст.</b>\nИспользование: /tts [текст]'
randomint = random.randint(1000, 9999)
temp_dir = os.path.join(os.getcwd(), config.extensions_dir, 'temp/')
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)
temp_file =  os.path.join(temp_dir, str(randomint) + '.mp3')

@dp.message_handler(commands='tts')
async def tts_handler(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        randomint = random.randint(1000, 9999)
        input_tts = {message.text[message.entities[0].length:]}
        lang = detect(str(input_tts))
        tts = gTTS(str(input_tts), lang=lang)
        tts.save(temp_file)
        with open(temp_file, 'rb') as f:
            voice_message = f.read()
        await bot.send_voice(message.chat.id, voice_message)
        os.remove(temp_file)
    else:
        await message.reply(help_txt, parse_mode='HTML') 
