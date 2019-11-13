import socket
import time


class Client:
    """Класс, реализующий интерфейс клиента"""
    def __init__(self, host, port, timeout=None):
        # класс инкапсулирует создание сокета
        self.host = host
        self.port = port
        # создание клиентского сокета, запоминание объекта сокета в self
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("error create connection", err)

    def _read(self):
        """Метод для чтения ответа сервера"""
        data = b""

        # накопление буфера, до тех пор пока не встретится "\n\n" в конце сообщения клиента
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError("error recv data", err)

        # преобразование байтов в строки для дальнейшей работы
        decoded_data = data.decode()

        status, response = decoded_data.split("\n", 1)
        response = response.strip()

        # в случае ошибки выбрасывается исключение ClientProtocolError
        if status == "error":
            raise ClientProtocolError(response)

        return response

    def put(self, key, value, timestamp=None):
        """Метод отправки put-запроса с метриками на сервер"""
        timestamp = timestamp or int(time.time())

        # отправка запроса
        try:
            self.connection.sendall(
                f"put {key} {value} {timestamp}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # разборка ответа
        self._read()

    def get(self, key):
        """Метод формирования и отправления get-запроса по ключу на сервер"""

        # отправка запроса
        try:
            self.connection.sendall(
                f"get {key}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # чтение ответа
        response = self._read()

        data = {}
        if response == "":
            return data

        # разбор ответа
        for row in response.split("\n"):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))

        return data

    def close(self):
        """Метод для закрытия соединения"""
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("error close connection", err)


# создание клиентских исключений

class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class ClientSocketError(ClientError):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class ClientProtocolError(ClientError):
    """Исключение, выбрасываемое клиентом при ошибке протокола"""
    pass


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=5)
    client.put("test", 1.0, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 3.0, timestamp=3)
    print(client.get("*"))

    client.close()