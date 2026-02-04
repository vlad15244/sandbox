import pytest

from abstarct_factory import Database, Mysql, Database_Factory, Mysql_Factory, Mssql, Mssql_Factory

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
            db.connect(db_user, db_pwd,db_localhost, 'test', 'Table_Order')


        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")        
        
    def test_insert(self, insert_values, db_localhost, db_user, db_pwd):
        assert db_localhost, "db_localhost не может быть пустым"
        assert db_user, "db_user не может быть пустым"
        assert db_pwd, "db_pwd не может быть пустым"

        factory = Mysql_Factory()
        db = factory.create_db()

        try:
            db.connect(db_user, db_pwd,db_localhost, 'test', 'Table_Order')
            db.insert(("dfgdfg", ))
        except Exception as e:
            pytest.fail(f"Ошибка : {e}")
        except ConnectionError as e:
            pytest.fail(f"Ошибка : {e}")               





    

    
