import os
import csv


class CarBase:
    """Базовый класс для всех видов машин"""

    # Запись индексов каждого полей в строках csv-файла
    idx_car_type = 0
    idx_brand = 1
    idx_passenger_seats_count = 2
    idx_photo_filename = 3
    idx_body_whl = 4
    idx_carrying = 5
    idx_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        """Метод для определения расширения файла изображения машины"""
        _, ext = os.path.splitext(self.photo_file_name)
        return ext


class Car(CarBase):
    """Класс, представляющий легковую машину"""

    # тип машины
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @classmethod
    def create(cls, row):
        """Метод класса для создания экземпляра класса из полей строки в csv-файле"""
        return cls(
            row[cls.idx_brand],
            row[cls.idx_photo_filename],
            row[cls.idx_carrying],
            row[cls.idx_passenger_seats_count],
        )


class Truck(CarBase):
    """Класс, представляющий грузовик"""

    # тип машины
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            # получение длины, ширины и высоты кузова
            length, width, height = (float(c) for c in body_whl.split("x", 2))
        except ValueError:
            # в случае ошибки присваиваем нули
            length, width, height = .0, .0, .0

        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length

    @classmethod
    def create(cls, row):
        """Метод класса для создания экземпляра класса из полей строки в csv-файле"""

        return cls(
            row[cls.idx_brand],
            row[cls.idx_photo_filename],
            row[cls.idx_carrying],
            row[cls.idx_body_whl],
        )


class SpecMachine(CarBase):
    """Класс, представляющий спецтехнику"""

    # тип машины
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def create(cls, row):
        """Метод класса для создания экземпляра класса из полей строки в csv-файле"""

        return cls(
            row[cls.idx_brand],
            row[cls.idx_photo_filename],
            row[cls.idx_carrying],
            row[cls.idx_extra],
        )


def get_car_list(csv_filename):
    """Функция, предназначенная для создания списка объектов машин из данных в csv-файле"""

    # открытие csv-файла
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        # пропуск строки с названиями колонок
        next(reader)

        # создание пустого списка, который и будет возвращаться
        car_list = []

        # создание словаря, в котором в качестве объектов используются типы машин
        # а в качестве ключей объекты каждого из типов
        car_classes = {car_class.car_type: car_class for car_class in (Car, Truck, SpecMachine)}

        # построчное чтение файла
        for row in reader:
            try:
                # определяем тип машины
                car_type = row[CarBase.idx_car_type]
            except IndexError:
                # если достаточное количество колонок в строке отсутствует, то пропускаем её
                continue

            try:
                # определяем класс экземпляра машины
                car_class = car_classes[car_type]
            except KeyError:
                # если тип неопределен или некорректен, то пропускаем создание
                continue

            try:
                # создаем экземпляр и добавляем его в результирующий список
                car_list.append(car_class.create(row))
            except (ValueError, IndexError):
                # если операция прошла некорректно, то пропускаем
                pass

    return car_list


if __name__ == '__main__':
    print(get_car_list('coursera_week3_cars.csv'))