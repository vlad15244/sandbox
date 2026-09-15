import time
import json

FILE_NAME = "buffer.txt"
ATTEMP_COUNTER = 0
while True:
    try:
        with open("buffer.txt", "r", encoding="utf-8-sig") as file:
            content = file.read()
            ATTEMP_COUNTER += 1
            print(f"Попытка {ATTEMP_COUNTER}")
            json_content = json.loads(content)
            print(json_content)


            time.sleep(5)            
    except (PermissionError, OSError) as e:
        print(f"Не удалось открыть файл: {e}. Повтор через 5 секунд...")
        time.sleep(5)