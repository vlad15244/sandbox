from functools import wraps
import pymysql

"""OBSOLETE"""
class Run_Database():

    def __init__(self, user:str,password:str,host:str,database:str,charset = 'utf8mb4'):
        """Параметры подключения к БД"""
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.charset = charset



        self.connection = None


    def connect(self):

        self.connection = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,          
            charset=self.charset
        )

class Column():
    def __init__(self, name, type, additional_params, block_insert_update = True):
        self.name = name
        self.type = type
        self.additional_params = additional_params
        self.block_insert_update = block_insert_update

    def __str__(self):
        return self.name + ' ' + self.type + ' ' + self.additional_params
    
    def ToString(self, WithSQL : bool, Separator : str):

        result = self.name
        if WithSQL:
            result = result + ' ' + self.type + ' ' + self.additional_params
        result = result + Separator
        return result
    
   
class Table():
    
    def __init__(self, name):
        self.name = name
        self.Columns = []
        self.parent_table = None        


    def __str__(self):
        return self.name
    
    def getcolumns(self):
        return ','.join(str(col) for col in self.Columns)

    def AddColumn(self, column):
        self.Columns.append(column) 

    def Initialization(self) -> str:

        aQuery = ' CREATE TABLE IF NOT EXISTS ' + self.name + ' ('
        aQuery += ','.join(str(col) for col in self.Columns)

        if 'ID' not in self.Columns[0].name:
            pass

        if self.parent_table:
            aQuery += ','
            aQuery += ' PRIMARY KEY (`' + self.Columns[0].name +'`,`' + self.Columns[1].name + '`),'
            aQuery += ' KEY `idx`' + '( ' + self.Columns[1].name + ' ),'
            aQuery += ' CONSTRAINT ' + '`' + self.Columns[1].name + '`' + ' FOREIGN KEY (`' +self.Columns[1].name+'`) REFERENCES `' + self.parent_table.name +  '` (`ID`) ON DELETE CASCADE'
            aQuery += ')' 
        else:
            aQuery += ','            
            aQuery += ' PRIMARY KEY (' + self.Columns[0].name +')'
            aQuery += ')' 
        if self.parent_table:
            self.foreign_key = self.Columns[1].name

        return aQuery


    def insert_one(self, value : dict) -> bool:

        aQuery = 'INSERT INTO ' + self.name + ' ('
        if not value:
            pass 
            """Дбавить обработку ошибки"""
          
        aCol = ''
        aVal = ''

        #подготовка запроса
        for col in self.Columns:
            if 'ID' in col.name and 'AUTO_INCREMENT' in col.additional_params:
                continue
            else:
                aCol += col.name + ','
                aVal += '%s,'

        aCol = aCol[:-1]
        aVal = aVal[:-1]        

        aQuery += aCol + ') VALUES ('
        aQuery += aVal +');'



        cursor = self.database_obj.connection.cursor()
        cursor.execute(aQuery, (value,))
        self.database_obj.connection.commit()

    def insert_many(self, value : dict) -> str:

        aQuery = 'INSERT INTO ' + self.name + ' ('
        if not value:
            pass 
            """Дбавить обработку ошибки"""
          
        aCol = ''
        aVal = ''

        #подготовка запроса
        for col in self.Columns:
            if 'ID' in col.name and 'AUTO_INCREMENT' in col.additional_params:
                continue
            else:
                aCol += col.name + ','
                aVal += '%s,'

        aCol = aCol[:-1]
        aVal = aVal[:-1]        

        aQuery += aCol + ') VALUES ('
        aQuery += aVal +');'

        return aQuery





    def select_all(self) -> dict:

        aQuery = 'SELECT * FROM ' + self.name + ';'
        self.database_obj.connect()

        cursor = self.database_obj.connection.cursor()
        cursor.execute(aQuery)

        return cursor.fetchall()
    
    def select_filter(self, filter: dict) -> dict:

        aQuery = 'SELECT * FROM ' + self.name + ' WHERE '
        where_parts = []

        for flt in filter:

            before, sep, after = flt.partition('_')
            before1, sep1, after1 = flt.partition('=')            
            if '__eq' in flt:
                where_parts.append(f"{before} = '{after1}'")
            if '__lt' in flt:
                where_parts.append(f"{before} > '{after1}'")
            if '__gt' in flt:
                where_parts.append(f"{before} < '{after1}'")
            if '__le' in flt:
                where_parts.append(f"{before} >= '{after1}'")
            if '__ge' in flt:
                where_parts.append(f"{before} <= '{after1}'")

        aQuery += ' , '.join(where_parts)

        cursor = self.database_obj.connection.cursor()
        cursor.execute(aQuery)

        return cursor.fetchall()
    

    def join_table(self, filter = None, order_by = None):
        query = 'SELECT * FROM ' + str(self.parent_table) + ' JOIN ' + self.name + ' ON ' + self.name +'.'

        if  self.parent_table:
            query += self.foreign_key

        query += ' = ' + str(self.parent_table) +'.'  

        for col in self.Columns:
            if 'ID' in col.name and 'AUTO_INCREMENT' in col.additional_params: 
                query += col.name
                break 

        where_parts = []

        if filter:
            query += ' WHERE '

            for col in self.Columns:
                for flt in filter:
                    if col.name in flt:
                        before, sep, after = flt.partition('=')
                        if '__eq' in flt:
                            where_parts.append(f"{self.name}.{col.name} = {after}")
                        if '__lt' in flt:
                            where_parts.append(f"{self.name}.{col.name} > {after}")
                        if '__gt' in flt:
                            where_parts.append(f"{self.name}.{col.name} < {after}")               
                        if '__le' in flt:
                            where_parts.append(f"{self.name}.{col.name} >= {after}")
                        if '__ge' in flt:
                            where_parts.append(f"{self.name}.{col.name} <= {after}")
                            
        query += ' AND '.join(where_parts)

        order_parts = []

        if order_by:

            query += ' ORDER BY '
            for col in self.parent_table.Columns:
                for ord in order_by:
                    if col.name in ord:
                        if '__asc' in ord:
                            order_parts.append(f"{col.name} ASC")
                        if '__dsc' in ord:
                            order_parts.append(f"{col.name} DSC")

        query += ' , '.join(order_parts) 

        cursor = self.database_obj.connection.cursor()
        cursor.execute(query)

        return cursor.fetchall()        
 


if __name__ == "__main__":
    pass
""" Table_Order = Table('orders')

    Table_Order.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    Table_Order.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))

    factory = abstarct_factory.Mysql_Factory()

    db = factory.create_db()

    db.connect('root', '1234','localhost', 'test', Table_Order)
    db.create()

    db.insert(('fdgdfgdfg',))
    
    db.dissconnect()

    Table_Order.select_filter(('ID__le=2',))
    Table_Order1 = Table('items',MySQL, Table_Order)

    Table_Order1.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    Table_Order1.AddColumn(Column('ID_key', 'BIGINT', 'UNSIGNED NOT NULL'))    
    Table_Order1.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))


    Table_Order1.Initialization()
    print(Table_Order1.join_table(('ID__eq=2',)))"""
