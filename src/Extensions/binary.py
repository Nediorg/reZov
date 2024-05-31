import re

thelp_txt = '<b>Переводит текст в двоичный код.</b>\nИспользование: /tobin [текст]'
fhelp_txt = '<b>Переводит двоичный код в текст.</b>\nИспользование: /frombin [двоичный код]'

async def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return ' '.join(re.findall('.{%s}' % 8, str(bits.zfill(8 * ((len(bits) + 7) // 8)))))

async def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits.replace(' ', ''), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

@dp.message(Command(commands='tobin'))
async def convert_to_binary(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        await message.reply(await text_to_bits(message.text[message.entities[0].length:]))
    else:
        await message.reply(thelp_txt, parse_mode='HTML')
        
@dp.message(Command(commands='frombin'))
async def convert_from_binary(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        text = await text_from_bits(message.text[message.entities[0].length:])
        if 't.me/+42777' not in text:
            await message.reply(text)
        else:
            await message.reply('IДI НАХУЙ\n\n- с уважением, админ')
    else:
        await message.reply(fhelp_txt, parse_mode='HTML')
