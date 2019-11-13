import asyncio


# создание классов с разнесенной по отдельности логикой работы сервера

class Storage:
    """Класс для хранения метрик в памяти процесса"""
    def __init__(self):
        self._data = {}

    def put(self, key, value, timestamp):
        if key not in self._data:
            self._data[key] = {}

        self._data[key][timestamp] = value

    def get(self, key):
        data = self._data

        if key != "*":
            data = {
                key: data.get(key, {})
            }

        result = {}
        for key, timestamp_data in data.items():
            result[key] = sorted(timestamp_data.items())

        return result


class Parser:
    """Класс для реализации протокола"""

    def encode(self, responses):
        """Преобразование ответа сервера в строку для передачи в сокет"""
        rows = []
        for response in responses:
            if not response:
                continue
            for key, values in response.items():
                for timestamp, value in values:
                    rows.append(f"{key} {value} {timestamp}")

        result = "ok\n"

        if rows:
            result += "\n".join(rows) + "\n"

        return result + "\n"

    def decode(self, data):
        """Метод для разбора поступивших команд и возврата списка команд для выполнения"""
        parts = data.split("\n")
        commands = []
        for part in parts:
            if not part:
                continue

            try:
                method, params = part.strip().split(" ", 1)
                if method == "put":
                    key, value, timestamp = params.split()
                    commands.append(
                        (method, key, float(value), int(timestamp))
                    )
                elif method == "get":
                    key = params
                    commands.append(
                        (method, key)
                    )
                else:
                    raise ValueError("unknown method")
            except ValueError:
                raise ParseError("wrong command")

        return commands


class Executor:
    """Класс, реализующий логику выполнения команды сервера"""

    def __init__(self, storage):
        self.storage = storage

    def run(self, method, *params):
        if method == "put":
            return self.storage.put(*params)
        elif method == "get":
            return self.storage.get(*params)
        else:
            raise ExecutorError("Unsupported method")


class EchoServerClientProtocol(asyncio.Protocol):
    """Класс для реализации сервера при помощи asyncio"""

    storage = Storage()

    def __init__(self):
        super().__init__()

        self.parser = Parser()
        self.executor = Executor(self.storage)
        self._buffer = b''

    def process_data(self, data):
        """Обработка входной команды сервера"""

        # разбор сообщения при помощи парсера
        commands = self.parser.decode(data)

        # выполнение команды и запоминание результата
        responses = []
        for command in commands:
            resp = self.executor.run(*command)
            responses.append(resp)

        # преобразование команды в строку
        return self.parser.encode(responses)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Метод data_received вызывается при получении данных в сокете"""
        self._buffer += data
        try:
            decoded_data = self._buffer.decode()
        except UnicodeDecodeError:
            return

        # ожидание данных, если команда не завершена символом \n
        if not decoded_data.endswith('\n'):
            return

        self._buffer = b''

        try:
            # обработка поступившего запроса
            resp = self.process_data(decoded_data)
        except (ParseError, ExecutorError) as err:
            # формирование ошибки, в случае ожидаемых исключений
            self.transport.write(f"error\n{err}\n\n".encode())
            return

        # формирование успешного ответ
        self.transport.write(resp.encode())


# создание серверных исключений

class ParseError(ValueError):
    pass


class ExecutorError(Exception):
    pass


# функция, запускающая сервер

def run_server(host, port)
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        EchoServerClientProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    # запуск сервера для тестирования
    run_server('127.0.0.1', 8888)
