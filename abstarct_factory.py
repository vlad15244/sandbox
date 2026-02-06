from abc import ABC, abstractmethod
import pymysql
from join_ import Column, Table

class Database(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod    
    def connect(self):
        pass

    @abstractmethod    
    def dissconnect(self):
        pass

    @abstractmethod
    def insert_many(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def select_all(self):
        pass

    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def count(self):
        pass


class Mysql(Database):
    def __init__(self):

        self.connection = None
       

    def connect(self, user:str,password:str,host:str,database:str,charset = 'utf8mb4'):

        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.charset = charset
        self.is_connected : bool 


        try:
            self.connection = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,          
            charset=self.charset
        )
            print(f"Соединение с сервером установлено: {self.host}") 
            self.is_connected = True            
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    def dissconnect(self):
        try:
            self.connection.close()

            if self.is_connected:
                self.is_connected = False

            print(f"Завершено соединение с сервером: {self.host}")             
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    def create(self,table):

        aQuery = ' CREATE TABLE IF NOT EXISTS ' + str(table) + ' ('
        aQuery += table.getcolumns()
        aQuery += ','            
        aQuery += ' PRIMARY KEY (' + table.Columns[0].name +')'
        aQuery += ')' 
        try:
            cursor = self.connection.cursor()
            cursor.execute(aQuery)
            self.connection.commit() 
            cursor.close()
        except Exception as e:
            print(aQuery)
            print(f"Ошибка работы с БД {e}")   

    def select_all(self, table) -> dict:

        aQuery = 'SELECT * FROM ' + str(table) + ';'
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(aQuery)
            self.connection.commit() 

            cursor.close()
            return cursor.fetchall()

        except Exception as e:
            print(aQuery)
            print(f"Ошибка работы с БД {e}") 

    def insert_many(self,table, value : dict) -> str:

        aQuery = 'INSERT INTO ' + str(table) + ' ('
        if not value:
            pass 
            """Дбавить обработку ошибки"""
          
        aCol = ''
        aVal = ''

        #подготовка запроса
        for col in table.Columns:
            if 'ID' in col.name and 'AUTO_INCREMENT' in col.additional_params:
                continue
            else:
                aCol += str(col.name) + ','
                aVal += '%s,'

        aCol = aCol[:-1]
        aVal = aVal[:-1]        

        aQuery += aCol + ') VALUES ('
        aQuery += aVal +');'

        cursor = self.connection.cursor()
        cursor.executemany(aQuery,value)
        self.connection.commit() 
        cursor.close()
        return aQuery

    def delete(self, table, id = 0):
        aQuery = 'DELETE FROM ' + str(table)
        if id != 0:
            aQuery  += ' WHERE ID =' + str(id)

        try:
            cursor = self.connection.cursor()
            cursor.execute(aQuery)
            self.connection.commit() 

            cursor.close()
            return cursor.fetchall()

        except Exception as e:
            print(aQuery)
            print(f"Ошибка работы с БД {e}") 


    def count(self, table):
        aQuery = 'SELECT COUNT(*) FROM' + str(table)

        try:
            cursor = self.connection.cursor()
            cursor.execute(aQuery)
            self.connection.commit() 

            cursor.close()
            return cursor.fetchall()

        except Exception as e:
            print(aQuery)
            print(f"Ошибка работы с БД {e}")              


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

    Table_Order = Table('orders')

    Table_Order.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    Table_Order.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))

    """do something"""
    factory = Mysql_Factory()

    db = factory.create_db()
    db.connect('root', '1234','localhost', 'test')
    db.create(Table_Order)
    db.insert_many(Table_Order, ("sfgdfg","sdfgdgdfg", "fsadfwef" ))    
    print(db.select_all(Table_Order))
    db.dissconnect()

