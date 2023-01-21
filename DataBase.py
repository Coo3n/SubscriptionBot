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
        return bool(self.cursor.execute("SELECT * FROM `users_bot` WHERE `user_id` = " + str(user_id)))

    #Добавляем пользователя в базу данных      
    async def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users_bot` (user_id) VALUES(\"" + str(user_id) + "\")")
        self.connection.commit()    
    
    #Возвращает количество денег пользователя
    async def get_user_money(self, user_id):
        self.cursor.execute("SELECT `cnt_money` FROM `users_bot` WHERE `user_id` = " + str(user_id))
        return self.cursor.fetchmany(1)

    #Устанавливаем количество денег пользователю
    async def set_money_to_user(self, user_id, money):
        self.cursor.execute("UPDATE `users_bot` SET `cnt_money` = " + str(money) + ", `date_of_payment` = now() WHERE user_id = " + str(user_id))
        self.connection.commit()        
        
