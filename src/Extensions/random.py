from random import randint

rhelp_txt = '<b>Выбирает число случайным образом.</b>\nИспользование: /random [min] [max]\nПример: /random 1 10'

@dp.message_handler(commands='random')
async def generate_random_number(message: types.Message):
    if not len(message.text[message.entities[0].length:])==0:
        args = message.text.split(' ')
        if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
            await message.reply(wrong)
        else:
            await message.reply(randint(int(args[1]), int(args[2])))
    else:
        await message.reply(rhelp_txt, parse_mode='HTML')