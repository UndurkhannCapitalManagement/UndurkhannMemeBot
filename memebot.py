import random
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InputMediaPhoto, MessageEntity
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes
import os
from dotenv import load_dotenv
# Replace 'YOUR_API_TOKEN' with your actual bot token from BotFather
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("SG小助手启动!")
    await show_option_buttons(update, context)

async def show_option_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("广播SG爷爷的故事", callback_data='button_0')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)


async def button_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    op = query.data.split("_")[1]
    match op:
        case '0':
            await broadcast_crime(update, context)
        case '1':
            await reply_with_random_quote(update, context)
        case '_':
            await query.edit_message_text('你不相信我的判断？.jpg')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to the following commands:\n/start - Start the bot\n/help - Get help information\n' +
        '/sgmadness - Get a random SG 爷爷故事\n'
    )

async def reply_with_random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    boism = os.listdir('asset')
    image_name = 'asset/' + random.Random().choice(boism)
    with open(image_name, 'rb') as image:
        #await update.message.reply_photo(photo=InputFile(image))
        await context.bot.send_photo(update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                             photo=InputFile(image))

async def sg_meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sg = os.listdir('asset')
    image_name = 'asset/' + random.Random().choice(sg)
    with open(image_name, 'rb') as image:
        await update.message.reply_photo(photo=InputFile(image))

async def broadcast_crime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    chapters：
    0 序章
    1 云顶
    2 栽赃陷害建群
    3 简介SG爷爷的大记忆恢复术
    4 Liberation day次日提倡不止损
    5 03/19 FOMC迷惑行为大赏
    6-1 I have high conviction tomorrow is the day
    7 The Day之后反咬一口大赏
    Appendix： SG爷爷话术大全

    :param update:
    :param context:
    :return:
    '''
    chapters = ['broadcast/chapter0',
                'broadcast/chapter1',
                'broadcast/chapter4',
                'broadcast/chapter5',
                'broadcast/chapter6',
                'broadcast/chapter7',
                'broadcast/chapter2',
                'broadcast/chapter3',
                'broadcast/appendix']
    def get_text_from_file(directory: str)->str:
        res = []
        with open(directory, 'r') as fh:
            for line in fh:
                res.append(line)
        return "\n".join(res)+"\n"

    for idx, chapter in enumerate(chapters):
        media_group = []
        file_names = os.listdir(chapter)
        caption = ""
        for file in file_names:
            if file == 'caption':
                caption = get_text_from_file(chapter+'/caption')
                continue
            image_name=chapter+'/'+file
            media_group.append(InputMediaPhoto(media=open(image_name,'rb')))

        try:
            for i in range(0, len(media_group), 4):
                await context.bot.send_media_group(update.callback_query.message.chat_id,
                                                   message_thread_id=update.callback_query._get_message().message_thread_id,
                                                   media=media_group[i:i + 4], caption=caption if i == 0 else None,
                                                   write_timeout=500, read_timeout=500)
        except:
            await context.bot.send_message(update.callback_query.message.chat_id,
                                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                           text=caption)
            await context.bot.send_message(update.callback_query.message.chat_id,
                                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                           text="卧槽没图说个锤子")
        time.sleep(1)



def main():
    # Create the Application instance
    application = Application.builder().token(API_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('sgmadness', sg_meme_command))

    # Register a CallbackQueryHandler to handle button selections
    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^button_'))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()