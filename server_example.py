from flask import Flask, request, jsonify
import random

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


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)