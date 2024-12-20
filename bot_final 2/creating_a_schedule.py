import numpy as np
from matplotlib import pyplot as plt

#этот класс создает график показывающий количество выполненных задач за прощедщие две недели, чтобы сравнить продуктивность
class Graph:
  def __init__(self, task_week_last, task_week_past):
    self.task_week_past = task_week_past
    self.task_week_last = task_week_last
    create_graph()

  #создаем график и сохраняем его картинкой png
  def create_graph():
    plt.figure(figsize=(10, 4))
    x = ['last week', 'this week']
    y = [self.task_week_last, self.task_week_past]
    plt.scatter(x, y)
    plt.title('График выполненных задач за прощедшие две недели')
    plt.grid(True)
    plt.show()
    plt.savefig('graphic.png', bbox_inches='tight')
