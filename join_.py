from functools import wraps
import pg8000

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
    
    def __init__(self, name, parent_table = None):
        self.name = name
        self.Columns = []
        self.parent_table = parent_table

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

        print(aQuery)

        connection = pg8000.connect(
            user='postgres',
            password='1234',
            host='localhost',
            database='postgres',
            port=5432
        )

        cursor = connection.cursor()

        cursor.execute(aQuery)

        cursor.close()
        connection.close()        



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

    Table_Order = Table('orders')

    Table_Order.AddColumn(Column('ID', 'SERIAL', 'NOT NULL'))
    Table_Order.AddColumn(Column('NAME', 'TEXT', 'NOT NULL'))
    Table_Order.AddColumn(Column('TIMESTAMP', 'TEXT', 'NOT NULL'))

    Table_Order.Initialization()

    """Table_Order1 = Table('order1', Table_Order)

    Table_Order1.AddColumn(Column('ID', 'INTEGER', 'NOT NULL'))
    Table_Order1.AddColumn(Column('ID_key', 'INTEGER', 'NOT NULL'))    
    Table_Order1.AddColumn(Column('NAME', 'TEXT', 'NOT NULL'))
    Table_Order1.AddColumn(Column('VALUE', 'REAL', 'NOT NULL'))

    Table_Order1.Initialization()"""

    
