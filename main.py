# ДЗ урока ОВ03 Композиция и полиморфизм
import json
import os

# 1. Базовый класс Animal
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        print("Животное издаёт звук...")

    def eat(self):
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, возраст: {self.age}"

    # Для сериализации
    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age
        }

    @staticmethod
    def from_dict(data):
        class_name = data['type']
        if class_name == 'Bird':
            return Bird(data['name'], data['age'])
        elif class_name == 'Mammal':
            return Mammal(data['name'], data['age'])
        elif class_name == 'Reptile':
            return Reptile(data['name'], data['age'])
        else:
            return Animal(data['name'], data['age'])


# 2. Подклассы животных
class Bird(Animal):
    def make_sound(self):
        print(f"{self.name} поёт: Чирик-чирик!")

class Mammal(Animal):
    def make_sound(self):
        print(f"{self.name} говорит: Гав! Или Мяу? Или Уааа!")

class Reptile(Animal):
    def make_sound(self):
        print(f"{self.name} шипит: Шшшшш!")


# 3. Полиморфизм — вызов разных методов make_sound()
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()


# 5. Классы сотрудников
class ZooKeeper:
    def feed_animal(self, animal):
        print(f"Смотритель кормит {animal.name}")

class Veterinarian:
    def heal_animal(self, animal):
        print(f"Ветеринар лечит {animal.name}")


# 4. Класс Zoo с использованием композиции
class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def add_staff(self, person):
        self.staff.append(person)

    def show_animals(self):
        print("\nЖивотные в зоопарке:")
        for animal in self.animals:
            print(animal)

    def show_staff(self):
        print("\nСотрудники зоопарка:")
        for person in self.staff:
            print(person.__class__.__name__)

    def save_to_file(self, filename='zoo_state.json'):
        data = {
            'animals': [animal.to_dict() for animal in self.animals],
            'staff': [person.__class__.__name__ for person in self.staff]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Состояние зоопарка сохранено в {filename}")

    @staticmethod
    def load_from_file(filename='zoo_state.json'):
        if not os.path.exists(filename):
            print("Файл не найден.")
            return None

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        zoo = Zoo()

        # Восстановление животных
        for animal_data in data['animals']:
            animal = Animal.from_dict(animal_data)
            zoo.add_animal(animal)

        # Восстановление сотрудников (упрощённо)
        for staff_type in data['staff']:
            if staff_type == 'ZooKeeper':
                zoo.add_staff(ZooKeeper())
            elif staff_type == 'Veterinarian':
                zoo.add_staff(Veterinarian())

        print(f"Состояние зоопарка загружено из {filename}")
        return zoo


# === Пример использования ===
if __name__ == "__main__":
    # Создание нового зоопарка
    my_zoo = Zoo()

    # Добавляем животных
    my_zoo.add_animal(Bird("Твитти", 2))
    my_zoo.add_animal(Mammal("Лев", 5))
    my_zoo.add_animal(Reptile("Шустрый ящер", 3))

    # Добавляем сотрудников
    keeper = ZooKeeper()
    vet = Veterinarian()
    my_zoo.add_staff(keeper)
    my_zoo.add_staff(vet)

    # Вызов полиморфного метода
    print("\n=== Звуки животных ===")
    animal_sound(my_zoo.animals)

    # Сценарий работы сотрудников
    print("\n=== Работа сотрудников ===")
    keeper.feed_animal(my_zoo.animals[0])
    vet.heal_animal(my_zoo.animals[1])

    # Информация о зоопарке
    my_zoo.show_animals()
    my_zoo.show_staff()

    # Сохранение в файл
    my_zoo.save_to_file()

    # Загрузка из файла
    loaded_zoo = Zoo.load_from_file()
    loaded_zoo.show_animals()
