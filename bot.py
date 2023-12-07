from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackContext

import sheet
import schedule
import pytz
import gspread
import datetime
import time
sa = gspread.service_account("service_account.json")
she = sa.open("Доступ в К006")
sh = sheet.Sheet
new_slot = {}
del_slot = {}

key = "6258824392:AAEE_I40M8E908SUNoHttH-pLM3E6Kh6Qf4"
timezone = pytz.timezone('Asia/Almaty')
NAME, DAY, TIME, FIN = range(4)
NAME1, DAY1, TIME1, FIN1 = range(4)

# START


def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.name
    update.message.reply_text(
        "Hello, {}!\nUse the following commands to:\n1./add the rehearsal\n2./delete the rehearsal\n3./list to view the empty slots\n/cancel to cancel add and delete commands".format(user_name))

# LIST


def get_list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(sh.get_all_list())
    return ConversationHandler.END


# ADD
def add(update: Update, context: CallbackContext) -> None:
    if sh.isListed(update.message.from_user.username) == False:
        update.message.reply_text("You don't have an access or you are banned")
        return ConversationHandler.END

    new_slot['username'] = update.message.from_user.username

    reply_keyboard = [['Mon'], ['Tue'], ['Wed'],
                      ['Thu'], ['Fri'], ['Sat'], ['Sun']]
    update.message.reply_text('Day?', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,  input_field_placeholder='Day?'
    ))
    return TIME


def time1(update: Update, context: CallbackContext) -> None:
    current_datetime = datetime.datetime.now()
    current_day_of_week = current_datetime.weekday()
    new_slot['day'] = update.message.text
    if (sh.days_int[f'{update.message.text}'] < current_day_of_week+1):
        update.message.reply_text(
            'You cannot add reservations to the previous days of the week', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    update.message.reply_text(sh.get_list_day(update.message.text))
    reply_keyboard = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
                      ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    update.message.reply_text('Select the time slot', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Time?'
    ))
    return FIN


def fin(update: Update, context: CallbackContext) -> None:
    current_datetime = datetime.datetime.now()
    current_day_of_week = current_datetime.weekday()
    current_datetime = datetime.datetime.now()
    time_string = current_datetime.strftime('%H:%M')
    time = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
            ['15:00 - 16:00'], ['1   6:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    for i in time:
        if i[-1] == update.message.text:
            if i[-1][0]*10+i[-1][1] < time_string[0]*10+time_string[1] and (current_day_of_week == sh.days_int[f"{new_slot['day']}"]-1):
                update.message.reply_text(
                    'You cannot add outdated slots', reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            update.message.reply_text(sh.add(new_slot['username'], new_slot['day'], time.index(
                i) + 9), reply_markup=ReplyKeyboardRemove())
    new_slot.clear()
    return ConversationHandler.END


def cancel_add(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Reservation canceled',
                              reply_markup=ReplyKeyboardRemove())
    new_slot.clear()
    return ConversationHandler.END

# DELETE


def delete(update: Update, context: CallbackContext) -> None:
    if sh.isListed(update.message.from_user.username) == False:
        update.message.reply_text(
            "You don't have an access or you are banned", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    del_slot['username'] = update.message.from_user.username

    reply_keyboard = [['Mon'], ['Tue'], ['Wed'],
                      ['Thu'], ['Fri'], ['Sat'], ['Sun']]
    update.message.reply_text('Day?', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,  input_field_placeholder='Day?'
    ))
    return TIME1


def delete_time(update: Update, context: CallbackContext) -> None:
    current_datetime = datetime.datetime.now()
    current_day_of_week = current_datetime.weekday()
    if (sh.days_int[f'{update.message.text}'] < current_day_of_week+1):
        update.message.reply_text(
            'You cannot cancel outdated reservations', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    update.message.reply_text(sh.get_list_day(update.message.text))
    del_slot['day'] = update.message.text

    reply_keyboard = [['09:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
                      ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    update.message.reply_text('Select the time slot', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Time?'
    ))
    return FIN


def delete_fin(update: Update, context: CallbackContext) -> None:
    current_datetime = datetime.datetime.now()
    current_day_of_week = current_datetime.weekday()
    current_datetime = datetime.datetime.now()
    time_string = current_datetime.strftime('%H:%M')
    time = [['09:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
            ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    time_index = 0
    for i in time:
        if i[-1] == update.message.text:
            time_index = i
            if i[-1][0]*10+i[-1][1] <= time_string[0]*10+time_string[1] and (current_day_of_week == sh.days_int[f"{del_slot['day']}"]-1):
                update.message.reply_text(
                    'You cannot cancel outdated reservations', reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            update.message.reply_text(sh.delete(context, del_slot['username'], del_slot['day'], time.index(
                i) + 9), reply_markup=ReplyKeyboardRemove())
    del_slot.clear()
    return ConversationHandler.END


def cancel_delete(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Deletion canceled', reply_markup=ReplyKeyboardRemove())
    del_slot.clear()
    return ConversationHandler.END


def main():
    scheduled_time = datetime.time(14, 2)  # 10:00 AM

# Schedule the task to run every day at the specified time
    schedule.every().saturday.at(str(scheduled_time)).do(sh.reset_list)
    updater = Updater(key)
    dispatcher = updater.dispatcher

    add_conv = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            TIME: [MessageHandler(Filters.regex('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)$'), time1)],
            FIN: [MessageHandler(Filters.all, fin)]
        },
        fallbacks=[CommandHandler('cancel', cancel_add)],
        conversation_timeout=300
    )
    del_conv = ConversationHandler(
        entry_points=[CommandHandler("delete", delete)],
        states={
            TIME1: [MessageHandler(Filters.regex('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)$'), delete_time)],
            FIN1: [MessageHandler(Filters.all, delete_fin)]
        },
        fallbacks=[CommandHandler('cancel', cancel_delete)],
        conversation_timeout=300
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", get_list))
    dispatcher.add_handler(add_conv)
    dispatcher.add_handler(del_conv)

    updater.start_polling()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
