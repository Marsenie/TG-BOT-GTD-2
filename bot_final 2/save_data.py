import ast

class data():
    #извлечение сохранённых дынных
    def get_data_from_txt(name):
        try:    
            with open(name) as f:
                return ast.literal_eval(f.read())
        except:
            print("ошибка чтения данных", name)
            return dict()

        
    #сохранение данных
    def save_data_in_txt(name, data):
        try:
            with open(name, "w") as f:    
                f.write(str(data))
        except:
            print("ошибка сохранения данных", name)
            return dict()
