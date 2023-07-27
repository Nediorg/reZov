from random import randint
from mc import PhraseGenerator
# Configs
bessrom_words = ['bess', 'rom', 'for', 'pabji', 'batteri', 'af', 'smooth', 'kernal', 'gamin', 'twrp', 'oranjfoks', 'ximi', 'sapdagon', 'miatool', 'mido', 'begonia', 'lavander', 'tissot', 'turbo', 'alo', 'vayu', 'surya', 'bocq', 'x', 'pru', 'iphun', '720g', '855', '860', '625', '660', '5s', 'se', '14', '3', '7', 'max', 'perfomance', 'nusuntara', 'linagOS', 'evox', 'pixzal experzence', 'aosp', 'muiu', 'posp', 'crdoid', 'havok', 'plus', 'derpfez', 'radml', 'wen']

@dp.message_handler(commands='bessrom')
async def bessrom(message: types.Message):
    generated_bessrom = ''
    for i in range(randint(4, 7)):
        generated_bessrom += PhraseGenerator(samples=bessrom_words).generate_phrase() + ' '
    await message.reply(generated_bessrom)
