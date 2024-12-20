import ast


class data():
    def get_data_from_txt(name):
        """извлечение сохранённых дынных"""
        try:    
            with open(name) as f:
                return ast.literal_eval(f.read())
        except:
            print("ошибка чтения данных", name)
            return dict()

        
    def save_data_in_txt(name, data):
        """сохранение данных"""
        try:
            with open(name, "w") as f:    
                f.write(str(data))
        except:
            print("ошибка сохранения данных", name)
            return dict()
