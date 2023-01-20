from Config import host, username, password, db_name
import pymysql

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect (
            host = host,
            user = username,
            password = password,
            database = db_name
        )
        self.cursor = self.connection.cursor()
        
    #Проверка существует ли пользователь    
    async def user_exists(self, user_id): 
        command = "SELECT * FROM `users_bot` WHERE `user_id` = " + str(user_id)
        return bool(self.cursor.execute(command))

    #Добавляем пользователя в базу данных      
    async def add_user(self, user_id):
        command = "INSERT INTO `users_bot` (user_id) VALUES(\"" + str(user_id) + "\")"
        result = self.cursor.execute(command)
        return self.connection.commit()    
    
    #Возвращает количество денег пользователя
    async def show_user_money(self, user_id):
        command = "SELECT `cnt_money` FROM `users_bot` WHERE `user_id` = " + str(user_id)
        self.cursor.execute(command)
        self.cursor.fetchmany(1)

    #Устанавливаем количество денег пользователю
    async def set_money_to_user(self, user_id, money):
        command = "UPDATE `users_bot` SET `cnt_money` = " + str(money) + ", `date_of_payment` = now() WHERE user_id = " + str(user_id)
        result = self.cursor.execute(command)
        self.connection.commit()      
        
