from save_data import *
from markups import *
import telebot
from telebot import types
import random
from apscheduler.schedulers.background import BackgroundScheduler

#читаем данные из файлов
token = data.get_data_from_txt("token.txt")["token"]
tasks = data.get_data_from_txt("tasks.txt")
names = data.get_data_from_txt("names.txt")
#списки назавний коробок и их назаниий в списке tasks
dict_from_markap_to_key_task = {"Задачи на сегодня":"tasks for the day","Задачи на неделю":"tasks for the week","Проекты":"projects","Корзина":"basket","Готово":"done","Потом":"later", "TODO":"TODO"}
dict_key_task_to_markap = {"tasks for the day":"Задачи на сегодня","tasks for the week":"Задачи на неделю","projects":"Проекты","basket":"Корзина","done":"Готово","later":"Потом", "TODO":"TODO"}
#списки стикеров и их длины
ls_stickers_motv = ["CAACAgIAAxkBAAENFFtnKya-Ol73bU-e6FeFvHR_2fXsNwACKlQAAni74Ukz4YY0Fcgi7zYE", "CAACAgIAAxkBAAENFVNnLLQ9kj3LnHiXwjdE2_e4WSPrUAAC9U4AAoYjgEh_p9O9NH2kUTYE"]
len_ls_stickers_motv = len(ls_stickers_motv) - 1
ls_stickers = ["CAACAgIAAxkBAAENJIhnOiJ--BMj3HebjhzZZ9FcuKS_OQACWUIAAjfs6Uh_HZZzeWE60TYE", "CAACAgIAAxkBAAENJIZnOiJ2dyY9mUlCg2ZXCAW3j-CvvgACv0QAAiC4UEu7TjASIXBQyTYE", "CAACAgIAAxkBAAENJIRnOiJu5jq9p8gM8oVNfdHBCj5aUAACLDQAAtB4WEuNzxS2xQABY7w2BA", "CAACAgIAAxkBAAENJIBnOh-xYB_gmayc5K9VgqbVAAGbuuoAAkFZAAJxCLlJBhcQZoXbDvQ2BA", "CAACAgIAAxkBAAENJHFnOh3kgPgqWca-cfyAqwd6LsG95QACjRgAAgQOUUmoCZil16lX3DYE", "CAACAgIAAxkBAAENJG1nOh2rlZmbMbsWmKOjwy2p4jgUXQACtBUAAtIFyEvEgZTnl4Z7azYE", "CAACAgIAAxkBAAENJGtnOh2pFWJZyqevZDzlP5RttHl0WAACXxYAAgq6yUsjtyMt_mlHPjYE", "CAACAgIAAxkBAAENJGlnOh2BcMZU6iFlwatPxw6bz5VTVAACL0UAAlodQUhg9_z4F5aFHTYE", "CAACAgIAAxkBAAENJGdnOh15tzAkr91ahIJEKp-q_JLDrQACpzwAAjULyUv9CJLnbFrcljYE", "CAACAgIAAxkBAAENJGVnOh1iJQO7vVGNvBvHVsvB_kbdGwAC5DkAAhe_yUtoklwSU0XmKzYE", "CAACAgIAAxkBAAENJGNnOh1dqUSb58foIDw3-gdIjdaLFgACsj0AAkotwEvwKHztiZMfXjYE", "CAACAgIAAxkBAAENJGFnOh1P3QYD1CXES3suSpkYp9IDpQACZj4AAmWpKEjLdU768OjDFjYE"]
len_ls_stickers = len(ls_stickers) - 1

class tg_bot():
    def __init__(self):
        #создаём бота
        self.bot_ = telebot.TeleBot(token)
        #запускаем бота
        #self.bot_.infinity_polling()
    
        
    def alert(self):
        """напоминание"""
        for i in names:
            if len(tasks[i]["tasks for the week"]) == 0:
                self.bot_.send_message(i, f"У вас ещё нет задач в Задачи на неделю. Стоит их добавить.")
                continue
            msg = "" 
            for i in range(len(tasks[i]["tasks for the week"])):
                msg += f"{tasks[message.chat.id]['tasks for the week'][i]}\n"
            self.bot_.send_message(i, msg, reply_markup = markup_start)

        
    def сall_alert(self):
        """вызов напоминания"""
        #создаём объект который будет вызывать alert каждую неделю
        sched = BackgroundScheduler()
        sched.add_job(self.alert, 'interval', seconds = 604800)#604800 секунд - неделя
        sched.start()


    def del_task(self, message):
        """удалить задачу"""
        #перебираем все коробки
        for i in tasks[message.chat.id]:
            #в коробках перебираем задачи
            for j in range(len(tasks[message.chat.id][i])):
                #если задача начанается с написанного слова в сообщение, то удаляём её
                if message.text in tasks[message.chat.id][i][j]:
                    self.bot_.send_message(message.chat.id, f"Удалена: {tasks[message.chat.id][i][j]}", reply_markup = markup_tasks)
                    tasks[message.chat.id][i].pop(j)
                    return
        #иначе говорим, что задача не найдена
        self.bot_.send_message(message.chat.id, f"Задача не найдена. Нет такой задачи, которая начинается с {message.text}", reply_markup = markup_tasks)


    def add_task_step_one(self, message):
        """добавить задачу часть 1"""
        try:
            #сохраняем задачу в tasks
            tasks[message.chat.id]["save"] = dict_from_markap_to_key_task[message.text]
            print(tasks[message.chat.id]["save"])
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
            tasks[message.chat.id][tasks[message.chat.id]["save"]].append(message.text)
            self.bot_.send_message(message.chat.id, text = "Добавил задачу", reply_markup = markup_tasks)
        except:
            #отправляем сообщение об ошибке, если что-то пошло не так
            self.bot_.send_message(message.chat.id, text = "Произошла ошибка((((", reply_markup = markup_tasks)


    def replace_task_step_one(self, message):
        """переместить задачу часть 1"""
        #сохраняем, то куда мы хотим переместить задачу
        try:
            tasks[message.chat.id]["save"] = dict_from_markap_to_key_task[message.text]
            self.bot_.send_message(message.chat.id, 'Введите первые слова задачи:')
            self.bot_.register_next_step_handler(message, self.replace_task_step_two)
        except:
            self.bot_.send_message(message.chat.id, text = 'Выберите коробку в которую хотите переместить:', reply_markup = markup_key_tasks)
            self.bot_.register_next_step_handler(message, self.replace_task_step_one)

            
    def replace_task_step_two(self, message):
        """переместить задачу часть 2"""
        #перебираем все коробки
        for i in tasks[message.chat.id]:
            #в коробках перебираем задачи
            for j in range(len(tasks[message.chat.id][i])):
                #если задача начанается с написанного слова в сообщение, то перемещаем его в сохранённую коробку
                if message.text in tasks[message.chat.id][i][j]:
                    try:
                        #перемещение задачи
                        tasks[message.chat.id][tasks[message.chat.id]["save"]].append(tasks[message.chat.id][i][j])
                        tasks[message.chat.id][i].pop(j)
                        #сообщение об успешном выполнении 
                        self.bot_.send_message(message.chat.id, f"Перемещена: {tasks[message.chat.id][i][j]}", reply_markup = markup_tasks)
                    except:
                        #сообщение ошибки
                        self.bot_.send_message(message.chat.id, "Задача не перемещена😭😭😭😭", reply_markup = markup_tasks)
                    return
        #если мы не нашли такую задачу
        self.bot_.send_message(message.chat.id, "Задача не  найдена, а значит и не перемещена😭😭😭😭", reply_markup = markup_tasks)


    def print_tasks(self, message):
        """показать все задачи в коробке"""
        #если нет задач, то ответим, что коробка пустая
        if len(tasks[message.chat.id][dict_from_markap_to_key_task[message.text]]) == 0:
            self.bot_.send_message(message.chat.id, f"У вас ещё нет задач в <<{message.text}>>", reply_markup = markup_start)
            return
        #иначе отправим все здачи
        msg = "" 
        for i in range(len(tasks[message.chat.id][dict_from_markap_to_key_task[message.text]])):
            msg += f"{tasks[message.chat.id][dict_from_markap_to_key_task[message.text]][i]}\n\n"
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
            tasks[message.chat.id][ls_key_task[step]].append(tasks[message.chat.id]["save"])
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
        tasks[message.chat.id]["save"] = message.text
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
            tasks[message.chat.id][key_task].append(tasks[message.chat.id]["save"])
            self.bot_.send_message(message.chat.id, f'Задача добавлена в коробку <<{dict_key_task_to_markap[key_task]}>>', reply_markup = markup_start)
        elif message.text == "Да":
            key_task = "tasks for the day"
            tasks[message.chat.id][key_task].append(tasks[message.chat.id]["save"])
            self.bot_.send_message(message.chat.id, f'Задача добавлена в коробку <<{dict_key_task_to_markap[key_task]}>>', reply_markup = markup_start)
        elif message.text == "Вернуться":
            self.bot_.send_message(message.chat.id, text = "Окей", reply_markup = markup_start)
        elif message.text == "Назад":
            self.bot_.send_message(message.chat.id, text = 'Требует более 10 минут на выполнение?', reply_markup = markup_yes_no)
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_four)
        else:
            self.bot_.register_next_step_handler(message, self.cycle_gtd_step_five)








          


      




