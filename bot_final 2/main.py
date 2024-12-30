from bot_logics import *


if __name__ == '__main__':
    #запускаем еженедельные напоминания
    bot.weekly_activities()
    #запускаем бота
    bot.bot_.infinity_polling()
