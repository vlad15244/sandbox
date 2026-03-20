from flask import Flask, request, jsonify
import random
import dbf

app = Flask(__name__)


@app.route('/api/commands/', methods=['GET'])
def get_command():
    """
    Получение статуса
    Проверим корректна ли команда - если нет сформируем ошибку и статус 404
    Если команда корректна сформируем статус 200
    """
    dice_roll = random.randint(1, 6)
    command = f"This is web server for SCADA - {dice_roll}"

    return command, 200

@app.route('/api/db/', methods=['GET'])
def get_db():
    with dbf.Table('name.dbf') as some_table:
        # Получаем список полей из таблицы
        field_names = some_table.field_names
        result = {}

        # Итерируем по записям с индексами (id)
        for i, record in enumerate(some_table, start=1):
            record_dict = {}
            for field_name in field_names:
                value = record[field_name]
                # Обрабатываем bytes, если есть
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='ignore').strip()
                record_dict[field_name] = value
            # Добавляем запись в итоговый словарь с ключом‑id
            result[i] = record_dict

        print(result)

    return result, 200


@app.route('/api/new_string/', methods=['POST'])
def get_list():

    id_new = request.get_json()['id']
    name_new = request.get_json()['name']
    print(float(id_new))   

    with dbf.Table('name.dbf') as some_table:
        some_table.open(dbf.READ_WRITE)
        some_table.append({'ID' : 1.0, 'NAME' : name_new})


    return jsonify({
        'id': id_new,
        'name' : name_new,
        'status': 'NEW'
    }), 201

@app.route('/api/test/', methods=['GET'])
def get_test():
    """
    Получение статуса
    Проверим корректна ли команда - если нет сформируем ошибку и статус 404
    Если команда корректна сформируем статус 200
    """
    data = {
        'filed1': 'this is filed1',
        'filed2': 'this is filed2'
    }


    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)