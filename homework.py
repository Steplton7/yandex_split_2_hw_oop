from typing import Dict, Type
from dataclasses import dataclass


MINUTE = 60


@dataclass
class InfoMessage:
    """ Информационный класс."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """ Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65     # 1.38

    def __init__(self, action, duration, weight) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self):
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """ Тренировка Бег."""
    C_RMS = 18
    C_RSS = 20

    def get_spent_calories(self) -> float:
        return ((self.C_RMS * self.get_mean_speed()
                - self.C_RSS) * self.weight / self.M_IN_KM
                * self.duration * MINUTE)


@dataclass
class SportsWalking(Training):
    """ Тренировка Ходьба."""
    C_WW = 0.035
    C_WWS = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.C_WW * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.C_WWS * self.weight) * self.duration * MINUTE)


@dataclass
class Swimming(Training):
    """ Тренировка Плавание."""
    LEN_STEP = 1.38
    C_SS = 1.1
    C_SW = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        return (self.get_mean_speed()
                + self.C_SS) * self.C_SW * self.weight
        # * self.duration

    def get_mean_speed(self):
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)


def read_package(workout_type, data):
    train_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in train_type:
        raise ValueError('Выберите подходящий вид тренировки')

    return train_type[workout_type](*data)


def main(train):
    info = train.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
