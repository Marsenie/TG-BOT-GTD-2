# TG-BOT-GTD-2

Медведев Арсений 466676 и Бунковская Анна 465304

Телеграмм бот планировщик, в котором реализован метод GTD. Он поможет повысить личную эффективность, посредством организации и контроля задач. Раз в неделю он присылает задачи из коробки "проекты", чтобы пользователь мог не забывал составлять план выполнения задач на неделе. Бот размещён на собственном сервере(rasberry pi 3B+). Функционал бота можно опробовать в тг @GTDplannerOfLife_bot.

Пользователь записывает задачи в нашего бота, а потом смотрит в нём, что ему нужно сделать. По мере выполнения задач он перемещает их в ящик "Готово" или удаляет их.

По просьбам бета-тестеров была добавлена функция реакции на стикеры(присылает стикер в ответ).

# Новизна:

1) построение графиков выполненных задач(прогресс считается по удалённым заданиям)
2) добавлены стикеры мотивации
3) еженедельное сохранение данных пользовательей
4) программа сильно изменена(раньше не было ни одного класса), добавлены: самописные исключения, валидация при создании графика...
5) попытка создания текстовых файлов при запуске, если они отсутствуют(без names.txt и tasks.txt программа запустится, но пользователи утратят все данные. Если будет отсутствоать token.txt, создастся файл, в который необходимо будет вставить токен, а программа завершится с ошибкой. Отсутсвие остальных текстовых файлов урежет фунуционал программы, а также будут вылезать некритические ошибки)

# вопрос зачем его запускать

Его можно открыть в тг @GTDplannerOfLife_bot

# Использование:
2) скачать модули из requirements.txt

3) вставьте токен своего бота в token.txt(если его нет, то создайте в @BotFather)

4) запустить main.py 





