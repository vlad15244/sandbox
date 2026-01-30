from functools import wraps
         
class Column():
    def __init__(self, name, type, additinal_params, block_insert_update = True):
        self.name = name
        self.type = type
        self.additinal_params = additinal_params
        self.block_insert_update = block_insert_update


    def ToString(self, WithSQL : bool, Separator : str):

        result = self.name
        if WithSQL:
            result = result + ' ' + self.type + ' ' + self.additinal_params
        result = result + Separator
        return result
    

class Table():
    def __init__(self, name):
        self.name = name
        self.Columns = [] 

    def AddColumn(self, column):
        self.Columns.append(column) 


def join_table(table1, table2, filter = None, order_by = None):
    query = 'SELECT * FROM ' + table1.name + ' JOIN ' + table2.name + ' ON ' + table1.name +'.' 

    for col in table1.Columns:
        if 'PRIMARY KEY' in col.additinal_params:
            query += col.name
            break 

    query += ' = ' + table2.name +'.' 

    for col in table2.Columns:
        if 'FOREIGN KEY' in col.additinal_params:
            query += col.name
            break

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

    oreder_parts = []

    if order_by:

        query += ' ORDER BY '
        for col in table2.Columns:
            for ord in order_by:
                if col.name in ord:
                    if '__asc' in ord:
                        oreder_parts.append(f"{col.name} ASC")
                    if '__dsc' in ord:
                        oreder_parts.append(f"{col.name} DSC")

    query += ' , '.join(oreder_parts)            
    return query

if __name__ == "__main__":

    Table_Order = Table('order')
    Table_Order.AddColumn(Column('ID', 'INTEGER', 'NOT NULL PRIMARY KEY AUTOINCREMENT'))
    Table_Order.AddColumn(Column('NAME', 'TEXT', 'NOT NULL'))
    Table_Order.AddColumn(Column('TIMESTAMP', 'TEXT', 'NOT NULL'))
    Table_Order.AddColumn(Column('VALUE', 'REAL', 'NOT NULL'))

    Table_Order1 = Table('order1')
    Table_Order1.AddColumn(Column('ID', 'INTEGER', 'NOT NULL PRIMARY KEY AUTOINCREMENT'))
    Table_Order1.AddColumn(Column('ID_key', 'INTEGER', 'FOREIGN KEY'))    
    Table_Order1.AddColumn(Column('NAME', 'TEXT', 'NOT NULL'))
    Table_Order1.AddColumn(Column('VALUE', 'REAL', 'NOT NULL'))

    #print(join_table(Table_Order, Table_Order1, ('VALUE__btw=2^5','NAME__gts=vlad'),('ID__asc',)))
    print(join_table(Table_Order, Table_Order1))
