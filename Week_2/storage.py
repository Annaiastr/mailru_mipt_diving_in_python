import os
import json
import argparse
import tempfile

# создание файла-хранилища
STORAGE_PATH = os.path.join(tempfile.gettempdir(), 'storage.data')


def read(key):
    """Функция чтения данных по ключу из JSON-хранищища"""
    data = get_data()
    return data.get(key)


def write(key, value):
    """Функция записи данных ключ:значение в JSON-хранилище"""
    data = get_data()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]

    with open(STORAGE_PATH, 'w') as f:
        f.write(json.dumps(data))


def get_data():
    """Функция для чтения JSON-объекта из хранилища"""
    if not os.path.exists(STORAGE_PATH):
        return {}

    with open(STORAGE_PATH, 'r') as f:
        raw_data = f.read()
        if raw_data:
            return json.loads(raw_data)

        return {}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    parser.add_argument("--val")
    args = parser.parse_args()

    if args.key and args.val:
        write(args.key, args.val)
    elif args.key:
        print(' '.join(read(args.key)))
    else:
        print('Wrong command')