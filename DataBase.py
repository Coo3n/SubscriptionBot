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
    
    #Возвращает тариф пользователя
    async def get_tarif_user(self, user_id):
        self.cursor.execute("SELECT `number_rate` FROM `users_bot` WHERE `user_id` = " + str(user_id))
        return self.cursor.fetchmany(1)

    #Устанавливаем тариф пользователю
    async def set_rate_to_user(self, user_id, number_rate):
        self.cursor.execute("UPDATE `users_bot` SET `number_rate` = " + str(number_rate) + ", `date_of_payment` = now() WHERE user_id = " + str(user_id))
        self.connection.commit()        
        
    #Добавляем чек в базу данных      
    async def add_check(self, user_id, number_rate):
        self.cursor.execute("INSERT INTO `bill_check` (user_id, number_rate) VALUES(" + str(user_id) + ", \"" + str(number_rate)  + "\")")
        self.connection.commit()    

    #Смотрим есть ли такой чек в базе 
    async def exist_bill_сheck(self, user_id):
        self.cursor.execute("SELECT * FROM `bill_check` WHERE `user_id` = " + str(user_id))
        return len(self.cursor.fetchmany(1)) != 0

    #Удаляем чек 
    async def delete_check(self, user_id):
        self.cursor.execute("SET SQL_SAFE_UPDATES = 0")
        self.connection.commit()    
        self.cursor.execute("DELETE FROM `bill_check` WHERE `user_id` = \"" + str(user_id) + "\"")
        self.connection.commit()    

