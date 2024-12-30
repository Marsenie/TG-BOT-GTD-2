"""функции бота и сценарий ответов на сообщения"""
from save_data import *
from markups import *
import telebot
from telebot import types
from creating_a_schedule import *
import random
from apscheduler.schedulers.background import BackgroundScheduler 


#списки назавний коробок и их назаниий в списке tasks
dict_from_markap_to_key_task = {"Задачи на сегодня":"tasks for the day","Задачи на неделю":"tasks for the week","Проекты":"projects","Корзина":"basket","Готово":"done","Потом":"later", "TODO":"TODO"}
dict_key_task_to_markap = {"tasks for the day":"Задачи на сегодня","tasks for the week":"Задачи на неделю","projects":"Проекты","basket":"Корзина","done":"Готово","later":"Потом", "TODO":"TODO"}
#списки стикеров и их длины
ls_stickers_motv = data.get_data_from_txt("stickers_motv.txt")
ls_stickers = data.get_data_from_txt("ls_stickers.txt")
len_ls_stickers_motv = len(ls_stickers_motv) - 1
len_ls_stickers = len(ls_stickers) - 1

class tg_bot():
    def __init__(self):
        """создание бота и чтение данных"""
        #читаем данные из файлов
        self.tasks = data.get_data_from_txt("tasks.txt")
        self.names = data.get_data_from_txt("names.txt")
        self.token = data.get_data_from_txt("token.txt")["token"]
        #создаём бота
        self.bot_ = telebot.TeleBot(self.token)
        
        
    def alert(self):
        """напоминание"""
        for i in self.names:
            if len(self.tasks[i]["tasks for the week"]) == 0:
                #если нет задач
                self.bot_.send_message(i, f"У вас ещё нет задач в Задачи на неделю. Стоит их добавить.")
                continue
            msg = "" 
            for i in range(len(self.tasks[i]["tasks for the week"])):
                msg += f"{self.tasks[message.chat.id]['tasks for the week'][i]}\n"
            #отправить напоминание о том, что нужно сделать пользователю
            self.bot_.send_message(i, msg)

    def progress(self):
        """Показывает статистку двух последних недель и обновляет неделю"""
        for i in self.names:
            #создать фото таблицы
            Graph(self.tasks[i]["counter of completed tasks for the past week"], self.tasks[i]["counter of completed tasks for this week"])
            #отправить фото пользователю
            img = open('graphic.png', 'rb')
            self.bot_.send_photo(i, img)
            img.close()
            #обновление недель
            self.tasks[i]["counter of completed tasks for the past week"] = self.tasks[i]["counter of completed tasks for this week"]
            self.tasks[i]["counter of completed tasks for this week"] = 0

    def show_progress(self, message):
        """Показывает статистку двух последних недель"""
        #создать фото таблицы
        Graph(self.tasks[message.chat.id]["counter of completed tasks for the past week"], self.tasks[message.chat.id]["counter of completed tasks for this week"])
        #отправить фото пользователю
        img = open('graphic.png', 'rb')
        self.bot_.send_photo(message.chat.id, img)
        img.close()

    def save_data_week(self):
        """еженедельное сохранение данных"""
        data.save_data_in_txt("tasks.txt", self.tasks)
        data.save_data_in_txt("names.txt", self.names)
    def weekly_activities(self):
        """вызов еженедельных функций"""
        #создаём объект который будет вызывать alert каждую неделю
        sched = BackgroundScheduler()
        #напоминание о том, что нужно сделать
        sched.add_job(self.alert, 'interval', seconds = 604800)
        #показать прогресс
        sched.add_job(self.progress, 'interval', seconds = 604800)#604800 секунд - неделя
        #сохранение данных
        sched.add_job(self.save_data_week, 'interval', seconds = 604800)
        sched.start()


    def del_task(self, message):
        """удалить задачу"""
        #перебираем все коробки
        for i in self.tasks[message.chat.id]:
            #в коробках перебираем задачи
            for j in range(len(self.tasks[message.chat.id][i])):
                #если задача начанается с написанного слова в сообщение, то удаляём её
                if message.text in self.tasks[message.chat.id][i][j]:
                    self.bot_.send_message(message.chat.id, f"Удалена: {self.tasks[message.chat.id][i][j]}", reply_markup = markup_tasks)
                    self.tasks[message.chat.id][i].pop(j)
                    self.tasks[message.chat.id]["counter of completed tasks for this week"] += 1
                    return
        #иначе говорим, что задача не найдена
        self.bot_.send_message(message.chat.id, f"Задача не найдена. Нет такой задачи, которая начинается с {message.text}", reply_markup = markup_tasks)


    def add_task_step_one(self, message):
        """добавить задачу часть 1"""
        try:
            #сохраняем задачу в tasks
            self.tasks[message.chat.id]["save"] = dict_from_markap_to_key_task[message.text]
            #передаём сообщение второй части
            self.bot_.send_message(message.chat.id, 'Введите задачу:', reply_markup = markup_key_tasks)
            self.bot_.register_next_step_handler(message, self.add_task_step_two)
        except:
            #ещё раз выбираем коробку, так как выбрана не корректная
            self.bot_.send_message(message.chat.id, text = 'Выберите коробку', reply_markup = markup_key_tasks)
            self.bot_.register_next_step_handler(message, self.add_task_step_one)

        
    def add_task_step_two(self, message):
        """добавить задачу часть 2"""
        try:
            #добавляем задачу и отправляем сообщение об успешном выполении
            self.tasks[message.chat.id][self.tasks[message.chat.id]["save"]].append(message.text)
            self.bot_.send_message(message.chat.id, text = "Добавил задачу", reply_markup = markup_tasks)
        except:
            #отправляем сообщение об ошибке, если что-то пошло не так
            self.bot_.send_message(message.chat.id, text = "Произошла ошибка((((", reply_markup = markup_tasks)


    def replace_task_step_one(self, message):
        """переместить задачу часть 1"""
        #сохраняем, то куда мы хотим переместить задачу
        try:
            self.tasks[message.chat.id]["save"] = dict_from_markap_to_key_task[message.text]
            self.bot_.send_message(message.chat.id, 'Введите первые слова задачи:')
            self.bot_.register_next_step_handler(message, self.replace_task_step_two)
        except:
            self.bot_.send_message(message.chat.id, text = 'Выберите коробку в которую хотите переместить:', reply_markup = markup_key_tasks)
            self.bot_.register_next_step_handler(message, self.replace_task_step_one)

            
    def replace_task_step_two(self, message):
        """переместить задачу часть 2"""
        #перебираем все коробки
        for i in self.tasks[message.chat.id]:
            #в коробках перебираем задачи
            for j in range(len(self.tasks[message.chat.id][i])):
                #если задача начанается с написанного слова в сообщение, то перемещаем его в сохранённую коробку
                if message.text in self.tasks[message.chat.id][i][j]:
                    try:
                        #сообщение об успешном выполнении 
                        self.bot_.send_message(message.chat.id, f"Перемещена: {self.tasks[message.chat.id][i][j]}", reply_markup = markup_tasks)
                        #перемещение задачи
                        self.tasks[message.chat.id][self.tasks[message.chat.id]["save"]].append(self.tasks[message.chat.id][i][j])
                        self.tasks[message.chat.id][i].pop(j)
                    except:
                        #сообщение ошибки
                        self.bot_.send_message(message.chat.id, "Задача не перемещена😭😭😭😭", reply_markup = markup_tasks)
                    return
        #если мы не нашли такую задачу
        self.bot_.send_message(message.chat.id, "Задача не  найдена, а значит и не перемещена😭😭😭😭", reply_markup = markup_tasks)


    def print_tasks(self, message):
        """показать все задачи в коробке"""
        #если нет задач, то ответим, что коробка пустая
        if len(self.tasks[message.chat.id][dict_from_markap_to_key_task[message.text]]) == 0:
            self.bot_.send_message(message.chat.id, f"У вас ещё нет задач в <<{message.text}>>", reply_markup = markup_start)
            return
        #иначе отправим все здачи
        msg = "" 
        for i in range(len(self.tasks[message.chat.id][dict_from_markap_to_key_task[message.text]])):
            msg += f"{self.tasks[message.chat.id][dict_from_markap_to_key_task[message.text]][i]}\n\n"
        self.bot_.send_message(message.chat.id, msg, reply_markup = markup_start)


    def otv_na_sticker(self, message):
        """отправляет стикер в ответ на фото или стикер"""
        #отправляем стиекер 
        self.bot_.send_sticker(message.chat.id, sticker = ls_stickers[random.randint(0, len_ls_stickers)])
        
    #цикл gtd
    def draft_cycle_gtd(self, message, step):
        """Шаблон вопросов, который принимет сообщение пользователя и номер вопроса, а после присылает ответ пользователю и вызывыет функцию вопроса(сообщение Да/Назад) или добавляет задачу в коробку(сообщение Нет)"""
        #списки, нужные для упрощения вызова шаблона(вместо 6 вргументов у нас 2)
        ls_questions = ['Эта задача предполагает действия?', 'Решаемо за одно действие?', 'Могу сделать только я?', 'Требует более 10 минут на выполнение?']
        ls_key_task = ["later", "projects", "TODO"]
        ls_func = [self.cycle_gtd_step_alt_one, self.cycle_gtd_step_two, self.cycle_gtd_step_three, self.cycle_gtd_step_four]
        if message.text == "Нет":
            #добавляем в список и отпраляем сообщение, что всё прошло успешно
            self.bot_.send_message(message.chat.id, f'Задача добавлена в коробку <<{dict_key_task_to_markap[ls_key_task[step]]}>>', reply_markup = markup_start)
            self.tasks[message.chat.id][ls_key_task[step]].append(self.tasks[message.chat.id]["save"])
        elif message.text == "Да":
            #задаём следующий вопрос и перенаправляем на функцию следующего вопроса
            self.bot_.send_message(message.chat.id, text=ls_questions[step + 1], reply_markup = markup_yes_no)
            self.bot_.register_next_step_handler(message, ls_func[step + 1])
        elif message.text == "Вернуться":
            #Прекращаем цикл и возвращаемся на главный экран
            self.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
        elif message.text == "Назад":
            #Возвращаемся к предыдущему вопросу или на главный экран, если вопрос был первым
            if step >= 1:
                #к предыдущему вопросу
                self.bot_.send_message(message.chat.id, text=ls_questions[step - 1], reply_markup = markup_yes_no)
                self.bot_.register_next_step_handler(message, ls_func[step - 1])
            else:
                #на главный экран
                self.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
        else:
            self.bot_.register_next_step_handler(message, ls_func[step])

    
    def cycle_gtd_step_one(self, message):
        """функция принимающая задачу из сообщения(сохранияет его в tasks) и ожидающая следующего сообщения для вызова следующей функции"""
        #сохраняем задачу
        self.tasks[message.chat.id]["save"] = message.text
        #вызываем шаблон через функцию вопроса
        self.bot_.send_message(message.chat.id, text='Эта задача предполагает действия?', reply_markup = markup_yes_no)
        self.bot_.register_next_step_handler(message, self.cycle_gtd_step_alt_one)

        
    def cycle_gtd_step_alt_one(self, message):
        """промежуточная функция для вызова шаблона вопроса"""
        self.draft_cycle_gtd(message, 0)

        
    def cycle_gtd_step_two(self, message):
        """промежуточная функция для вызова шаблона вопроса"""
        self.draft_cycle_gtd(message, 1)

        
    def cycle_gtd_step_three(self, message):
        """промежуточная функция для вызова шаблона вопроса"""
        self.draft_cycle_gtd(message, 2)

        
    def cycle_gtd_step_four(self, message):
        """принимет сообщение пользователя и номер вопроса, а после присылает ответ пользователю..."""
        if message.text == "Нет":
            self.bot_.send_message(message.chat.id, text = "Делегируй", reply_markup = markup_start)
        elif message.text == "Да":
            self.bot_.send_message(message.chat.id, text = 'Нужно сделать сегодня?', reply_markup = markup_yes_no)
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_five)
        elif message.text == "Вернуться":
            self.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
        elif message.text == "Назад":
            self.bot_.send_message(message.chat.id, text = 'Могу сделать только я?', reply_markup = markup_yes_no)
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_three)
        else:
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_four)

        
    def cycle_gtd_step_five(self, message):
        """принимет сообщение пользователя и номер вопроса, а после присылает ответ пользователю..."""
        if message.text == "Нет":
            key_task = "tasks for the week"
            self.tasks[message.chat.id][key_task].append(self.tasks[message.chat.id]["save"])
            self.bot_.send_message(message.chat.id, f'Задача добавлена в коробку <<{dict_key_task_to_markap[key_task]}>>', reply_markup = markup_start)
        elif message.text == "Да":
            key_task = "tasks for the day"
            self.tasks[message.chat.id][key_task].append(self.tasks[message.chat.id]["save"])
            self.bot_.send_message(message.chat.id, f'Задача добавлена в коробку <<{dict_key_task_to_markap[key_task]}>>', reply_markup = markup_start)
        elif message.text == "Вернуться":
            self.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
        elif message.text == "Назад":
            self.bot_.send_message(message.chat.id, text = 'Требует более 10 минут на выполнение?', reply_markup = markup_yes_no)
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_four)
        else:
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_five)


#создаём бота
bot = tg_bot()


@bot.bot_.message_handler(commands=['start'])
def start(message):
    """Добавление новых пользователей и приветственное сообщение"""
    #добавляем пользователя в словари tasks и names, если его ещё там нет
    if message.chat.id not in bot.tasks:
        bot.tasks[message.chat.id] = {"tasks for the day": [], "tasks for the week": [], "projects": [], "basket": [], "done": [], "later": [], "TODO":[], "save":"", "counter of completed tasks for this week" : 0, "counter of completed tasks for the past week" : 0}
        bot.names[message.chat.id] = message.from_user.username, message.from_user.first_name, message.from_user.last_name
    #отправляем приветственное сообщение
    bot.bot_.send_message(message.chat.id, text="Привет, {0.first_name}! Я - GTD бот. Буду помогать тебе с составлением расписания.".format(message.from_user), reply_markup=markup_start)

    
@bot.bot_.message_handler(content_types=['photo', 'sticker'])
def otv_na_sticker_(message):
    """отправляет стикер в ответ на фото или стикер"""
    #отправляем стиекер 
    bot.otv_na_sticker(message)

    
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
    elif message.text == "Показать прогресс":
        bot.show_progress(message)
    elif message.text == "Стоп бот":#Сохранить данные и остановить выполнение программы(можно использовать если нужно обновить бота и не потерять данные пользователей)
        data.save_data_in_txt("tasks.txt", bot.tasks)
        data.save_data_in_txt("names.txt", bot.names)
        bot.bot_.send_message(message.chat.id, "Бот остановлен")
        exit()
    else:
        bot.bot_.send_message(message.chat.id, text = 'Попробуй ещё')
