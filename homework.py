from typing import ClassVar

M_IN_KM = 1000

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def get_message(self,
                    training_type: str,
                    duration: float,
                    distance: float,
                    speed: float,
                    calories: float) -> None:
        print(f'Тип тренировки: {training_type}; '
              f'Длительность: {duration:.3f} ч.; '
              f'Дистанция: {distance:.3f} км; '
              f'Ср. скорость: {speed:.3f} км/ч; '
              f'Потрачено ккал: {calories:.3f}.')

class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65

    def __init__(self,
                 training_type: str,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.training_type = training_type
        self.action = action
        self.duration = duration
        self.weight = weight
        self.duration = duration

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_info = InfoMessage().get_message(self.training_type,
                                self.duration,
                                self.get_distance(),
                                self.get_mean_speed(),
                                self.get_spent_calories())
        return info_info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] =  18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] =  1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        minutes = self.duration * 60
        mean_speed = self.get_mean_speed()
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM * minutes

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_WALKING_MULTIPLIER1: ClassVar[float] = 0.035
    CALORIES_MEAN_WALKING_MULTIPLIER2: ClassVar[float] = 0.029
    SECONDS_IN_HOUR = 3600
    CENTIMETERS_PER_METER = 100   
    def __init__(self,
                 training_type: str,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(training_type, action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        minutes = self.duration * 60
        height_in_meters = self.height / self.CENTIMETERS_PER_METER
        mean_speed = self.get_mean_speed()
        mean_speed_m_sec = (mean_speed * M_IN_KM
                            / (self.duration * self.SECONDS_IN_HOUR))
        return (((self.CALORIES_MEAN_WALKING_MULTIPLIER1 * self.weight
                  + (mean_speed_m_sec**2 / height_in_meters))
                  * self.CALORIES_MEAN_WALKING_MULTIPLIER2
                  * self.weight) * minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SWIMMING_MULTIPLIER1: ClassVar[float] = 1.1
    CALORIES_MEAN_SWIMMING_MULTIPLIER2: ClassVar[float] = 2 
    def __init__(self, training_type: str, 
                       action: int, 
                       duration: float, 
                       weight: float, 
                       length_pool: int, 
                       count_pool: int) -> None:
        super().__init__(training_type, action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = 1.38
        
    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration 

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SWIMMING_MULTIPLIER1) * 
                 self.CALORIES_MEAN_SWIMMING_MULTIPLIER2 * self.weight * self.duration)
    

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type=='SWM':#плавание
        action: int = data[0] 
        duration = data[1]
        weight = data[2]
        length_pool = data[3]
        count_pool =  data[4]
        return Swimming(workout_type, action,duration,weight,length_pool,count_pool)
    if workout_type == 'RUN':#бег
        action: int = data[0] 
        duration = data[1]
        weight = data[2]
        return Running(workout_type,action,duration,weight)
    if workout_type == 'WLK':#ходьба
        action: int = data[0] 
        duration = data[1]
        weight = data[2]
        height = data[3]
        return SportsWalking(workout_type,action,duration,weight,height)


def main(training: Training) -> None:
    """Главная функция."""
    training.show_training_info()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

