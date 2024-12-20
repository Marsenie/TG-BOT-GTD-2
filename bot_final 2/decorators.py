from bot_logics import *

#создаём бота
bot = tg_bot()


@bot.bot_.message_handler(commands=['start'])
def start(message):
    """Добавление новых пользователей и приветственное сообщение"""
    #добавляем пользователя в словари tasks и names, если его ещё там нет
    if message.chat.id not in tasks:
        tasks[message.chat.id] = {"tasks for the day": [], "tasks for the week": [], "projects": [], "basket": [], "done": [], "later": [], "TODO":[], "save":"", "counter of completed tasks for this week" : 0, "counter of completed tasks for the past week" : 0}
        names[message.chat.id] = message.from_user.username, message.from_user.first_name, message.from_user.last_name
    #отправляем приветственное сообщение
    bot.bot_.send_message(message.chat.id, text="Привет, {0.first_name}! Я - GTD бот. Буду помогать тебе с составлением расписания.".format(message.from_user), reply_markup=markup_start)

    
@bot.bot_.message_handler(content_types=['photo', 'sticker'])
def otv_na_sticker_(message):
    """отправляет стикер в ответ на фото или стикер"""
    #отправляем стиекер 
    bot.bot_.otv_na_sticker(message)

    
@bot.bot_.message_handler(content_types=['text'])
def communication_bot(message):
    """принимает сообщение пользователя и вызывает соответстующие функции"""
    if message.text == "Мотивация":#стикер
        bot.bot_.send_sticker(message.chat.id, sticker = ls_stickers_motv[random.randint(0, len_ls_stickers_motv)])
    elif message.text == "Показать GTD":#вывод задач
        bot.bot_.send_message(message.chat.id, text = 'Выберите коробку', reply_markup = markup_key_tasks)
        bot.bot_.register_next_step_handler(message, bot.print_tasks)
    elif message.text == "Пройти полный цикл GTD":#помощь с тем, что делать с задачей
         bot.bot_.send_message(message.chat.id, text='Введите задачу:', reply_markup = markup_yes_no)
         bot.bot_.register_next_step_handler(message, bot.cycle_gtd_step_one)
    elif message.text == "Планирование":#добавление/удаление/перемещение задачи
        bot.bot_.send_message(message.chat.id, text = "Планирую", reply_markup = markup_tasks)
    elif message.text == "Вернуться":#выйти на главный экран
        bot.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
    elif message.text == "Добавить задачу":
        bot.bot_.send_message(message.chat.id, text = 'Выберите коробку', reply_markup = markup_key_tasks)
        bot.bot_.register_next_step_handler(message, bot.add_task_step_one)
    elif message.text == "Переместить задачу":
        bot.bot_.send_message(message.chat.id, text = 'Выберите коробку в которую хотите переместить', reply_markup = markup_key_tasks)
        bot.bot_.register_next_step_handler(message, bot.replace_task_step_one)
    elif message.text == "Удалить задачу":
        msg = bot.bot_.send_message(message.chat.id, 'Введите первы слова задачи:')
        bot.bot_.register_next_step_handler(msg, bot.del_task)
    elif message.text == "Стоп бот":#Сохранить данные и остановить выполнение программы(можно использовать если нужно обновить бота и не потерять данные пользователей)
        save_data_in_txt("tasks.txt", tasks)
        save_data_in_txt("names.txt", names)
        bot.bot_.send_message(message.chat.id, "Бот остановлен")
        exit()
    else:
        bot.bot_.send_message(message.chat.id, text = 'Попробуй ещё')
