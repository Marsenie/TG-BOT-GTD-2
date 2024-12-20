from telebot import types

class create_markap():
    def __init__(self, list_name_btn, markap_row_width):
        """компактное создание маркапов"""
        #создаём маркап
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = markap_row_width)
        #добавляем в него кнопки
        for i in range(0, len(list_name_btn), markap_row_width):
            self.markup.add(*[types.KeyboardButton(list_name_btn[j]) for j in range(i, min( i + markap_row_width, len(list_name_btn) ))])

    
#создание маркапов
markup_start = create_markap(["Планирование", "Пройти полный цикл GTD", "Показать GTD", "Мотивация", "Показать прогресс"], 2).markup
markup_tasks = create_markap(["Добавить задачу", "Удалить задачу", "Переместить задачу", "Вернуться"], 1).markup
markup_key_tasks = create_markap(["Задачи на сегодня", "Задачи на неделю", "Проекты", "Корзина", "Готово", "Потом", "TODO"], 2).markup
markup_yes_no = create_markap(["Да", "Нет", "Назад", "Вернуться"], 2).markup

