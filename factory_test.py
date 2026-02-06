import pytest

from abstarct_factory import Database, Mysql, Database_Factory, Mysql_Factory, Mssql, Mssql_Factory
from join_ import Column, Table

class TestTable:

    def test_table_init(self):
        test = Table('orders')
        assert test.name == 'orders', "Задано имя"
        assert test.Columns == [], "Непустые колонки у созданной таблицы" 
        assert str(test) == 'orders', "Задано имя"   


    def test_eq_table(self, test_table):
        test = Table('orders')

        test.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
        test.AddColumn(Column('NAME', 'VARCHAR(40)', 'NOT NULL'))

        assert test == test_table, "Созданная таблица не соотвествует тестируемой"

        test1 = Table('orders1')

        test1.AddColumn(Column('ID', 'BIGINT', 'UNSIGNED NOT NULL AUTO_INCREMENT'))
        test1.AddColumn(Column('TEXT', 'VARCHAR(40)', 'NOT NULL'))

        assert test1 != test_table, "Созданная таблица соотвествует тестируемой"


    def test_getcolumns(self):

        table = Table('users')
        table.AddColumn(Column('id', 'INT', ''))
        table.AddColumn(Column('name', 'TEXT', ''))
        assert table.getcolumns() == 'id INT ,name TEXT ', 'Не корректная привязка полей'
     
class TestAbstractClass:
    """Проверяем, что это абстрактные классы"""
    def test_cannot_inmplements_db(self):
        with pytest.raises(TypeError) as excinfo:
            Database()

    def test_cannot_inmplements_factory(self):
        with pytest.raises(TypeError) as excinfo:
            Database_Factory()

class TestSubclass:
    def test_mysql(self):
        assert issubclass(Mysql, Database), "Класс MySQL не является созданной абсрактного класса"

    def test_mssql(self):
        assert issubclass(Mssql, Database), "Класс MSSQL не является созданной абсрактного класса"

    def test_factory_mysql(self):
        assert issubclass(Mysql_Factory, Database_Factory), "Фабрика MySQL не является созданной абсрактной фабрикой"

    def test_factory_mssql(self):
        assert issubclass(Mssql_Factory, Database_Factory), "Фабрика MSSQL не является созданной абсрактной фабрикой"
    
    
class TestMysql:
    def test_connect(self, db_localhost, db_user, db_pwd):

        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"

        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")  

    def test_init_table(self, db_localhost, db_user, db_pwd, test_table): 
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"
        assert test_table, "таблица не может быть пустой"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"
            db.create(test_table)
        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")  

    def test_insert(self, db_localhost, db_user, db_pwd, test_table, test_value):
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"
        assert test_table, "таблица не может быть пустой"
        assert test_value, "данные для теста не могут быть пустыми"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"
            db.insert_many(test_table, test_value)
        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")  

    def test_select(self, db_localhost, db_user, db_pwd, test_table, test_value):
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"
        assert test_table, "таблица не может быть пустой"
        assert test_value, "данные для теста не могут быть пустыми"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"

            result = db.select_all(test_table)

            assert result, "запрос вернул пустой"
            assert len(result) > 1, "данные не получены"

        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}") 

    def test_delete(self, db_localhost, db_user, db_pwd, test_table):
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"
        assert test_table, "таблица не может быть пустой"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"

            db.delete(test_table)

            result = db.select_all(test_table)
            
            assert len(result) == 0, "Таблица не была очищена"

        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")

    def test_full(self, db_localhost, db_user, db_pwd, test_table, test_value):
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"
        assert test_table, "таблица не может быть пустой"
        assert test_value, "таблица не может быть пустой"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test')
            assert db.is_connected, "Соединение не установлено"

            db.delete(test_table)

            result = db.select_all(test_table)
            assert len(result) == 0, "Таблица не была очищена"

            db.insert_many(test_table, test_value)

            result = db.select_all(test_table)
            assert len(result) == len(test_value), "Размер данных для тестирования не совпадает с ответом"

            db.delete(test_table)

            result = db.select_all(test_table)
            assert len(result) == 0, "Таблица не была очищена"

        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")