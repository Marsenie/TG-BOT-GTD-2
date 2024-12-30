"""создание графиков для оценки эффективности"""
import numpy as np
from matplotlib import pyplot as plt
from decorators import *


#создаем график, на котором показанно сколько задач пользователь сделал за последние две недели
class Graph:
    def __init__(self, task_week_last, task_week_past):
        """создание графика"""
        self.task_week_last = task_week_last
        self.task_week_past = task_week_past
        self.create_graph()


    @validate_value(lambda x: isinstance(x, int), "Аргумент должен быть целым числом")
    def create_graph(self):
        """Сохраняет таблицу в файл graphic.png"""
        plt.figure(figsize=(8, 4))
        x = ['Last Week', 'This Week']
        y = [self.task_week_last, self.task_week_past]
        plt.bar(x, y)
        plt.title('График выполненных задач за последние две недели')
        plt.savefig('graphic.png', bbox_inches='tight') 

