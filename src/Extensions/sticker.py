import magic, tarfile
mime = magic.Magic(mime=True)

stickers_cache_dir = f"{config.extensions_dir}StickersCache/"

if not os.path.exists(stickers_cache_dir):
    os.mkdir(stickers_cache_dir)

STICKER_HELP_TEXT = '<b>Данная команда скачивает стикер в tgs, webm или webp и отправляет его ID.</b>\n\nИспользование:\n- <code>[ответ на стикер] /sticker</code>\n- <code>/sticker [ID стикера]</code>'
STICKER_ID_TEXT = '<b>🏞 ID стикера:</b> '

async def dl_sticker(sid, message):
    sticker_path = f"{stickers_cache_dir}{sid}"
    if not sid in [os.path.splitext(filename)[0].split('.')[0] for filename in os.listdir(stickers_cache_dir)]:
        await bot.download_file_by_id(sid, sticker_path)
        file_type = '.' + mime.from_file(sticker_path).split('/')[1]
        match file_type:
            case ".gzip":
                os.rename(os.path.join(stickers_cache_dir, sid), os.path.join(stickers_cache_dir, sid + ".tgs"))
            case _:
                os.rename(os.path.join(stickers_cache_dir, sid), os.path.join(stickers_cache_dir, sid + file_type))
    for sticker_filename in os.listdir(stickers_cache_dir):
        if sticker_filename.startswith(sid):
            sticker_file_path = stickers_cache_dir + sticker_filename
    file_type = '.' + mime.from_file(sticker_file_path).split('/')[1]
    if file_type == '.webm':
        with open(sticker_file_path, 'rb') as sticker_file:
            await message.reply_document(document=sticker_file, caption=STICKER_ID_TEXT + f'<code>{sid}</code>', parse_mode='HTML')
    else:
        if sticker_file_path.endswith('.tar'):
            with open(sticker_file_path, 'rb') as sticker_file:
                await message.reply_document(document=sticker_file, caption=STICKER_ID_TEXT + f'<code>{sid}</code>', parse_mode='HTML')
        else:
            with tarfile.open(f"{sticker_file_path}.tar", "w") as sticker_tar:
                sticker_tar.add(sticker_file_path, arcname=sticker_file_path.split('/')[-1])
            os.remove(sticker_file_path)
            with open(f"{sticker_file_path}.tar", "rb") as sticker_file:
                await message.reply_document(document=sticker_file, caption=STICKER_ID_TEXT + f'<code>{sid}</code>', parse_mode='HTML')

@dp.message_handler(commands='sticker')
async def get_sticker_info(message: types.Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker_id = message.reply_to_message.sticker.file_id
        await dl_sticker(sticker_id, message)
    elif len(message.text[message.entities[0].length:]) != 0:
        sticker_id = message.text[message.entities[0].length + 1:]
        await dl_sticker(sticker_id, message)
    else:
        await message.reply(STICKER_HELP_TEXT, parse_mode='HTML')