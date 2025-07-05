# Система описания птиц

class Bird:
# Базовый класс для всех птиц. Содержит общие характеристики и поведение.

    def __init__(self, name, voice, color):
        self.name = name      # Имя птицы
        self.voice = voice    # Голос птицы
        self.color = color    # Цвет оперения

    def fly(self):
        """Метод: птица летает"""
        print(f"{self.name} летает")

    def eat(self):
        """Метод: птица кушает"""
        print(f"{self.name} кушает")

    def sing(self):
        """Метод: птица поёт"""
        print(f"{self.name} поет - {self.voice}")

    def info(self):
        """Метод: вывод информации о птице"""
        print("===== Информация о птице =====")
        print(f"Имя: {self.name}")
        print(f"Голос: {self.voice}")
        print(f"Цвет: {self.color}")


class Pigeon(Bird):
    """
    Класс голубя, наследуется от Bird.
    Может выполнять все действия базового класса.
    """

    def __init__(self):
        super().__init__(
            name="Голубь",
            voice="курлы-курлы",
            color="Серый"
        )

    def walk(self):
        """Метод: голубь гуляет"""
        print(f"{self.name} гуляет по площади")


# Точка входа — тестирование программы
if __name__ == "__main__":
    # Создаем объект класса Pigeon
    bird1 = Pigeon()

    # Выводим информацию о птице
    bird1.info()

    # Вызываем методы
    bird1.sing()
    bird1.fly()
    bird1.eat()
    bird1.walk()
