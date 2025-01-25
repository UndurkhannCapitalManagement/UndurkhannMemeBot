
import os
import random

import mplfinance
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, InputMediaPhoto
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes, Updater, MessageHandler, Application
from dotenv import load_dotenv
from tvDatafeed import TvDatafeed, Interval

from com.main.services.stock_chart_service import StockChartService

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome to the Simple Meme Bot!")
    await show_option_buttons(update, context)


async def show_option_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("随机语录", callback_data='button_1')],
        [InlineKeyboardButton("一锅端！", callback_data='button_2')],
        [InlineKeyboardButton("5块钱当爹", callback_data='button_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)


async def button_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    op = query.data.split("_")[1]
    match op:
        case '0':
            await stock_command(update, context)
        case '1':
            await reply_with_random_quote(update, context)
        case '2':
            await query.edit_message_text('勃勃：小心我把你们一锅端！.jpg')
        case '3':
            await query.edit_message_text('勃勃：你以为5块钱想当我爹？.jpg')
        case '_':
            await query.edit_message_text('未知领域')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'I can respond to the following commands:\n/start - Start the bot\n/help - Get help information\n' +
        '/bobomadness - Get a random 勃主席语录\n'
    )

async def reply_with_random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    boism = os.listdir('asset')
    image_name = 'asset/' + random.Random().choice(boism)
    with open(image_name, 'rb') as image:
        await context.bot.send_photo(update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                             photo=InputFile(image))
async def bobo_meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    boism = os.listdir('asset')
    image_name = 'asset/' + random.Random().choice(boism)
    with open(image_name, 'rb') as image:
        await update.message.reply_photo(photo=InputFile(image))

async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        tv = TvDatafeed()
        if not context.args:
            tickers = [["SPX", "SP"], ["NDX", "NASDAQ"], ["IWM", "AMEX"]]
            await context.bot.send_message(update.callback_query.message.chat_id, "Weekly Trend for Major Index")
        else:
            tickers = [[context.args[0].upper(), context.args[1].upper()]]
        for ticker, exchange in tickers:
            data = tv.get_hist(ticker, exchange, interval=Interval.in_15_minute, n_bars=160)
            if data.empty:
                await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                              text= f"No data found for {ticker}. Please check the ticker symbol.")
                return
            macd = StockChartService.MACD(pd.DataFrame(data), 12, 26, 9)

            macd_plot = [
                mplfinance.make_addplot((macd['macd']), color='#606060', panel=2, ylabel='MACD', secondary_y=False),
                mplfinance.make_addplot((macd['signal']), color='#1f77b4', panel=2, secondary_y=False),
                mplfinance.make_addplot((macd['bar_positive']), type='bar', color='#4dc790', panel=2),
                mplfinance.make_addplot((macd['bar_negative']), type='bar', color='#fd6b6c', panel=2),
            ]
            chart_filename = f'{ticker}_chart.png'
            mplfinance.plot(data, type='candle', style='yahoo', mav=(5, 20), volume=True,
                            addplot=macd_plot, savefig=chart_filename)
            with open(chart_filename, 'rb') as chart:
                await context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                             photo=InputFile(chart))
            os.remove(chart_filename)
    except IndexError:
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                       text='Please provide a valid ticker symbol. Usage: /stock [ticker]')
    except Exception as e:
        await context.bot.send_message(update.callback_query.message.chat_id,
                           message_thread_id=update.callback_query._get_message().message_thread_id,
                                       text=f"An error occurred: {str(e)}")

async def downloader(update, context):
    if update.message.document is None:
        await update.message.reply_text('Please attach the photo with /upload command!')
        return
    fileName = update.message.document.file_name
    new_file = await update.message.effective_attachment.get_file()
    await new_file.download_to_drive('./asset/'+fileName)
    await update.message.reply_text(f"{fileName} saved successfully")


def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('bobomadness', bobo_meme_command))
    application.add_handler(CommandHandler('stock', stock_command))
    #application.add_handler(MessageHandler(Filters.UpdateFilter(['upload']), downloader))

    application.add_handler(CallbackQueryHandler(button_selection_handler, pattern='^button_'))
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    while True:
        main()
