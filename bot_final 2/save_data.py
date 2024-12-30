"""чтение и сохранение фалов"""
import ast
import os
from exceptions import *


class data():
    def get_data_from_txt(name):
        """извлечение сохранённых дынных"""
        try:    
            with open(name) as f:
                return ast.literal_eval(f.read())
        except:
            print("ошибка чтения данных, попытка создания ", name)
            try:
                with open(name, 'w') as f:
                    if name != "token.txt":
                        f.write("{}")
                    else:
                        f.write("{\"token\" : \"ВАШ ТОКЕН\"}")
                        raise ReadErr("ошибка чтения токена", f"создайте {name} в {os.getcwd()}, с содержимым: " + "{\"token\" : \"ВАШ ТОКЕН\"}")
                print("создан:", name, " в ", os.getcwd())
            except:
                raise CreateFileErr("не получилось создать файл", name)
            return dict()

        
    def save_data_in_txt(name, data):
        """сохранение данных"""
        try:
            with open(name, "w") as f:    
                f.write(str(data))
        except:
            print("ошибка сохранения данных", name)
            return dict()
