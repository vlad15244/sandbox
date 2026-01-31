from functools import wraps
import pymysql



class Run_Database():
    def __init__(self, user,password,host,database,charset = 'utf8mb4'):
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
    
    def __init__(self, name, database_obj : Run_Database, parent_table = None):
        self.name = name
        self.Columns = []
        self.parent_table = parent_table
        self.database_obj = database_obj

    def AddColumn(self, column):
        self.Columns.append(column) 

    def Initialization(self):

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

        self.database_obj.connect()

        cursor = self.database_obj.connection.cursor()
        cursor.execute(aQuery)
        cursor.close()
        self.database_obj.connection.close()


    

def join_table(table1, table2, filter = None, order_by = None):
    query = 'SELECT * FROM ' + table1.name + ' JOIN ' + table2.name + ' ON ' + table1.name +'.' 

    for col in table1.Columns:
        if 'ID' in col.name and 'AUTO_INCREMENT' in col.additional_params: 
            query += col.name
            break 

    query += ' = ' + table2.name +'.'

    if table2.parent_table:
        query += table2.foreign_key

    where_parts = []

    if filter:
        query += ' WHERE '

        for col in table2.Columns:
            for flt in filter:
                if col.name in flt:
                    before, sep, after = flt.partition('=')
                    if '__eq' in flt:
                        where_parts.append(f"{table2.name}.{col.name} = {after}")
                    if '__lt' in flt:
                        where_parts.append(f"{table2.name}.{col.name} > {after}")
                    if '__gt' in flt:
                        where_parts.append(f"{table2.name}.{col.name} < {after}")
                    if '__lte' in flt:
                        where_parts.append(f"{table2.name}.{col.name} >= {after}")
                    if '__gte' in flt:
                        where_parts.append(f"{table2.name}.{col.name} <= {after}")
                    if '__btw' in flt:
                        val1, sep1, val2 = after.partition('^')
                        where_parts.append(f"({table2.name}.{col.name} BETWEEN {val1} AND {val2})")                        

    query += ' AND '.join(where_parts)

    order_parts = []

    if order_by:

        query += ' ORDER BY '
        for col in table2.Columns:
            for ord in order_by:
                if col.name in ord:
                    if '__asc' in ord:
                        order_parts.append(f"{col.name} ASC")
                    if '__dsc' in ord:
                        order_parts.append(f"{col.name} DSC")

    query += ' , '.join(order_parts)            
    return query

if __name__ == "__main__":

    MySQL = Run_Database('root', '1234','localhost', 'test')


    Table_Order = Table('orders', MySQL)

    Table_Order.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    Table_Order.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))


    Table_Order.Initialization()

    Table_Order1 = Table('items',MySQL, Table_Order)

    Table_Order1.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
    Table_Order1.AddColumn(Column('ID_key', 'BIGINT', 'UNSIGNED NOT NULL'))    
    Table_Order1.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))


    Table_Order1.Initialization()


    
