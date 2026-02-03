from abc import ABC, abstractmethod
import pymysql

class Database(ABC):
    @abstractmethod

    def __init__(self):
        pass
    def connect(self):
        pass
    def dissconnect(self):
        pass

    def insert(self):
        pass

    def create(self):
        pass


class Mysql(Database):
    def __init__(self):

        self.connection = None
        self.table_obj_1 = None
        self.table_obj_2 = None        

    def connect(self, user:str,password:str,host:str,database:str, table1, table2 = None,charset = 'utf8mb4'):

        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.charset = charset    
        self.table_obj_1 = table1
        self.table_obj_2 = table2        
        try:
            self.connection = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,          
            charset=self.charset
        )
            print(f"Соединение с сервером установлено: {self.host}")             
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def dissconnect(self):
        try:
            self.connection.close()
            print(f"Завершено соединение с сервером: {self.host}")             
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def insert(self, value:dict):

        aQuery = self.table_obj_1.insert_many(value)

        cursor = self.connection.cursor()
        cursor.executemany(aQuery, (value))
        self.connection.commit() 

    def create(self):
        aQuery = self.table_obj_1.Initialization()

        cursor = self.connection.cursor()
        cursor.execute(aQuery)
        cursor.close()   

        
class Mssql(Database):
    def connect(self):
        """need a realization"""
        print('This is driver for Mssql server')  

class Sqlite(Database):
    def connect(self):
        print('This is driver for sqlite')  

class Database_Factory(ABC):
    @abstractmethod
    def create_db(self) -> Database:
        pass

class Mysql_Factory(Database_Factory):
    def create_db(self):
        return Mysql()
    
class Mssql_Factory(Database_Factory):
    def create_db(self):
        return Mssql()
    
if __name__ == "__main__":

    """do something"""
    factory = Mysql_Factory()

    db = factory.create_db()
    db.connect('root', '1234','localhost', 'test')
    db.dissconnect()

