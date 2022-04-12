from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self. MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight
        self.duration_in_min = self.duration_h * self.MIN_IN_H

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в {}.'
                                  .format(type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight_kg
                / self.M_IN_KM * self.duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALKING_CALORIE_1: float = 0.035
    WALKING_CALORIE_2: float = 0.029

    def __init__(self,
                 action,
                 duration,
                 weight,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        return ((self.WALKING_CALORIE_1 * self.weight_kg
                + (self.get_mean_speed()**2 // self.height_sm)
                * self.WALKING_CALORIE_2 * self.weight_kg)
                * self.duration_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIMMING_CALORIE_1: float = 1.1
    SWIMMING_CALORIE_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        mean_speed: float = self.get_mean_speed()
        spent_calories: float = ((mean_speed + self.SWIMMING_CALORIE_1)
                                 * self.SWIMMING_CALORIE_2 * self.weight_kg)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    information: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in information:
        raise KeyError('Передаваемого типа нет в словаре')
    return information[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
