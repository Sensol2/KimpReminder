# -*- coding: utf-8 -*-
import logging

from telegram.ext.callbackcontext import CallbackContext

from KimpRateAPI import *
from db import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, Job
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

#UI Menu 만들기
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

#10초마다 검사하는 함수
def callback_minute(context):
    currPrice = getKimpRate(0)
    _chat_id=context.job.context
    print(_chat_id)
    
    print(priceCheckerData)
    if currPrice > priceCheckerData[_chat_id]:
        context.bot.send_message(chat_id=_chat_id, text="[비트뱅크->업비트] : {:.3f}% \n ".format(currPrice))


# 버튼이 실행되었을때 콜백 기능 실행
def callback_get(update, context) :
    data_selected = update.callback_query.data
    print("callback : ", data_selected)

    _chat_id = update.callback_query.message.chat_id
    _message_id = update.callback_query.message.message_id

    # 김프 알림간격 설정
    if data_selected.find("10s") != -1 :
        if not _chat_id in priceCheckerJobqueue:
            context.bot.edit_message_text(text="김프를 10초 간격으로 검사합니다", chat_id=_chat_id, message_id=_message_id)
            job = context.job_queue.run_repeating(callback_minute, interval=10, first=3, context=_chat_id)
            priceCheckerJobqueue[_chat_id] = job
        else:
            context.bot.edit_message_text(text="이미 검사중입니다.", chat_id=_chat_id, message_id=_message_id)
        return
    if data_selected.find("3m") != -1 :
        if not _chat_id in priceCheckerJobqueue:
            context.bot.edit_message_text(text="김프를 3분 간격으로 검사합니다", chat_id=_chat_id, message_id=_message_id)
            job = context.job_queue.run_repeating(callback_minute, interval=180, first=3, context=_chat_id)
            priceCheckerJobqueue[_chat_id] = job
        else:
            context.bot.edit_message_text(text="이미 검사중입니다.", chat_id=_chat_id, message_id=_message_id)
        return
    if data_selected.find("30m") != -1 :
        if not _chat_id in priceCheckerJobqueue:
            context.bot.edit_message_text(text="김프를 30분 간격으로 검사합니다", chat_id=_chat_id, message_id=_message_id)
            job = context.job_queue.run_repeating(callback_minute, interval=1800, first=3, context=_chat_id)
            priceCheckerJobqueue[_chat_id] = job        
        else:
            context.bot.edit_message_text(text="이미 검사중입니다.", chat_id=_chat_id, message_id=_message_id)
        return
    if data_selected.find("1h") != -1 :
        if not _chat_id in priceCheckerJobqueue:
            context.bot.edit_message_text(text="김프를 1시간 간격으로 검사합니다", chat_id=_chat_id, message_id=_message_id)
            job = context.job_queue.run_repeating(callback_minute, interval=3600, first=3, context=_chat_id)
            priceCheckerJobqueue[_chat_id] = job        
        else:
            context.bot.edit_message_text(text="이미 검사중입니다.", chat_id=_chat_id, message_id=_message_id)
        return
    if data_selected.find("3h") != -1 :
        if not _chat_id in priceCheckerJobqueue:
            context.bot.edit_message_text(text="김프를 3시간 간격으로 검사합니다", chat_id=_chat_id, message_id=_message_id)
            job = context.job_queue.run_repeating(callback_minute, interval=10800, first=3, context=_chat_id)
            priceCheckerJobqueue[_chat_id] = job
        else:
            context.bot.edit_message_text(text="이미 검사중입니다.", chat_id=_chat_id, message_id=_message_id)
        return

    # 김프 목표가 설정
    if data_selected.find("minusKP-1%") != -1 :
        id = update.callback_query.message.chat.id
        priceCheckerData[id] -= 1
        context.bot.edit_message_text(text="김프가 {:.1f}% 이상일 때 알림을 받습니다.".format(priceCheckerData[id]), 
        chat_id=_chat_id, message_id=_message_id)
        return

    elif data_selected.find("plusKP+1%") != -1 :
        id = update.callback_query.message.chat.id
        priceCheckerData[id] += 1
        context.bot.edit_message_text(text="김프가 {:.1f}% 이상일 때 알림을 받습니다.".format(priceCheckerData[id]), 
        chat_id=_chat_id, message_id=_message_id)
        return

    elif data_selected.find("plusKP-0.1%") != -1 :
        id = update.callback_query.message.chat.id
        priceCheckerData[id] -= 0.1
        context.bot.edit_message_text(text="김프가 {:.1f}% 이상일 때 알림을 받습니다.".format(priceCheckerData[id]), 
        chat_id=_chat_id, message_id=_message_id)
        return

    elif data_selected.find("plusKP+0.1%") != -1 :
        id = update.callback_query.message.chat.id
        priceCheckerData[id] += 0.1
        context.bot.edit_message_text(text="김프가 {:.1f}% 이상일 때 알림을 받습니다.".format(priceCheckerData[id]), 
        chat_id=_chat_id, message_id=_message_id)
        return

    if data_selected.find("bitbank_upbit") != -1 :
        context.bot.edit_message_text(text="비트뱅크->업비트", chat_id=_chat_id, message_id=_message_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="[비트뱅크->업비트] : {:.3f}%".format(getKimpRate(0)))
        return

    elif data_selected.find("bitbank_bithumb") != -1 :
        context.bot.edit_message_text(text="비트뱅크->빗썸", chat_id=_chat_id, message_id=_message_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="[비트뱅크->업비트] : {:.3f}%".format(getKimpRate(1)))
        return

    elif data_selected.find("binance_upbit") != -1 :
        context.bot.edit_message_text(text="바이낸스->업비트", chat_id=_chat_id, message_id=_message_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="[바이낸스->업비트] : {:.3f}%".format(getKimpRate(2)))
        return

    elif data_selected.find("binance_bithumb") != -1 :
        context.bot.edit_message_text(text="바이낸스->빗썸", chat_id=_chat_id, message_id=_message_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="[바이낸스->빗썸] : {:.3f}%".format(getKimpRate(3)))
        return

    elif data_selected.find("cancel") != -1 :
        context.bot.edit_message_text(text="취소하였습니다.",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)                    
        return

def start(update, context):
    """Send a message when the command /start is issued."""
    # context.job_queue.start()
    show_list = []
    show_list.append(InlineKeyboardButton("10초", callback_data="10s"))
    show_list.append(InlineKeyboardButton("3분", callback_data="3m"))
    show_list.append(InlineKeyboardButton("30분", callback_data="30m"))
    show_list.append(InlineKeyboardButton("1시간", callback_data="1h"))
    show_list.append(InlineKeyboardButton("3시간", callback_data="3h"))
    show_list.append(InlineKeyboardButton("취소", callback_data="cancel"))

    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    update.message.reply_text("김프를 검사할 주기를 설정해주세요. 목표가를 설정하지 않았다면 /set으로 먼저 목표가를 설정해주세요.", reply_markup=show_markup)

# 해당 id의 스케쥴러 제거
def stop(update, context):
    if update.message.chat.id in priceCheckerJobqueue:
        priceCheckerJobqueue[update.message.chat.id].schedule_removal()
        del(priceCheckerJobqueue[update.message.chat.id])
        update.message.reply_text("검사를 정지합니다")
    else:
        update.message.reply_text("현재 실행중인 알림이 없습니다")


# 모든 스케쥴러 제거
def allstop(update, context):
    for job in context.job_queue.jobs():
        job.schedule_removal()

def WaitforInput(message):
    targetPrice = message.text
    print(targetPrice)

# 김프 목표가 불러오기
def setTargetPrice(update, context):

    # update.message.reply_text('목표 김프 가격을 정수단위로 설정해주세요.')
    # 딕셔너리, key는 ID고 value 기본값은 10%로 설정
    if not update.message.chat.id in priceCheckerData:
        priceCheckerData[update.message.chat.id] = 10
    print(update.message.chat.id)

    show_list = []
    show_list.append(InlineKeyboardButton("-1%", callback_data="minusKP-1%"))
    show_list.append(InlineKeyboardButton("+1%", callback_data="plusKP+1%"))
    show_list.append(InlineKeyboardButton("-0.1%", callback_data="plusKP-0.1%"))
    show_list.append(InlineKeyboardButton("+0.1%", callback_data="plusKP+0.1%"))
    show_list.append(InlineKeyboardButton("취소", callback_data="cancel"))
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    update.message.reply_text("김프가 {}% 이상일 때 알림을 받습니다.".format(priceCheckerData[update.message.chat.id]), reply_markup=show_markup)

    # print("함수 진입")
    # print(context)
    # msg = context.bot.send_message(update.message.chat_id, '목표 김프 가격을 정수단위로 설정해주세요')
    # context.bot.register_next_step_handler(msg, WaitforInput)
    
    # priceCheckerData.append
    # print(update.message.chat.id)

# 김프 가격 불러오기
def getPrice(update, context):
    show_list = []
    show_list.append(InlineKeyboardButton("빗뱅->업빗", callback_data="bitbank_upbit"))
    show_list.append(InlineKeyboardButton("빗뱅->빗썸", callback_data="bitbank_bithumb"))
    show_list.append(InlineKeyboardButton("바낸->업빗", callback_data="binance_upbit"))
    show_list.append(InlineKeyboardButton("바낸->빗썸", callback_data="binance_bithumb"))
    show_list.append(InlineKeyboardButton("취소", callback_data="cancel"))
    # 버튼 UI 설정

    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1890731216:AAEUhKtiWAetUMyCbQhKHw9Nwd4cyeY0wLw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
    dp.add_handler(CommandHandler("allstop", allstop, pass_job_queue=True))
    dp.add_handler(CommandHandler("set", setTargetPrice))
    dp.add_handler(CommandHandler("get", getPrice))

    # 스케쥴러
    # Initialize()
    # GetLink()
    # time.sleep(1)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # inline 버튼에 대응하는 콜백
    dp.add_handler(CallbackQueryHandler(callback_get))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
