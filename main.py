
# Выполнение ДЗ урока OB04 Принципы SOLID

# Импортируем ABC и abstractmethod из модуля abc — это необходимо для создания абстрактных классов.
from abc import ABC, abstractmethod

# Шаг 1: Создаём абстрактный класс Weapon (Оружие), который служит "интерфейсом" для всех видов оружия.
# Все подклассы должны реализовать метод attack().
class Weapon(ABC):
    # Абстрактный метод attack() определяет, как будет выглядеть атака конкретным оружием.
    @abstractmethod
    def attack(self) -> str:
        pass  # Реализация метода будет в каждом конкретном типе оружия.

# Шаг 2: Реализуем конкретные типы оружия — меч и лук.
# Эти классы наследуются от абстрактного класса Weapon и реализуют свой собственный attack().

# Класс Sword (Меч)
class Sword(Weapon):
    # Метод attack() возвращает строку, описывающую действие при использовании меча.
    def attack(self) -> str:
        return "боец наносит удар мечом"

# Класс Bow (Лук)
class Bow(Weapon):
    def attack(self) -> str:
        return "боец наносит удар из лука"

# Пример нового оружия — Axe (Топор). Мы можем добавить его без изменения других классов.
class Axe(Weapon):
    def attack(self) -> str:
        return "боец рубит топором"

# Шаг 3: Класс Fighter (Боец)
# Этот класс представляет игрока или персонажа, который может использовать разное оружие.
class Fighter:
    # Конструктор принимает имя бойца.
    def __init__(self, name: str):
        self.name = name      # Имя бойца
        self.weapon: Weapon = None  # Поле для текущего оружия, изначально пустое

    # Метод set_weapon позволяет бойцу выбрать новое оружие.
    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon  # Сохраняем выбранное оружие у бойца
        print(f"{self.name} выбирает {weapon.__class__.__name__}")  # Выводим информацию о выборе

    # Метод attack заставляет бойца атаковать с помощью текущего оружия.
    def attack(self):
        if self.weapon:  # Если оружие есть
            print(f"{self.name} {self.weapon.attack()}")  # Вызываем attack() текущего оружия
        else:
            print("У бойца нет оружия!")

# Класс Monster (Монстр)
# Представляет противника, которого можно победить.
class Monster:
    # Метод defeat() выводит сообщение о том, что монстр побеждён.
    def defeat(self):
        print("Монстр побежден!")

# Функция battle (поединок) моделирует простую атаку бойца на монстра.
def battle(fighter: Fighter, monster: Monster):
    fighter.attack()       # Боец атакует
    monster.defeat()       # Монстр побеждается

# Точка входа программы — основной блок, где происходит выполнение действий.
if __name__ == "__main__":
    # Создаём экземпляр бойца с именем "Боец"
    hero = Fighter("Боец")
    # Создаём экземпляр монстра
    monster = Monster()

    # Бой 1 — с мечом
    sword = Sword()                 # Создаем объект меча
    hero.set_weapon(sword)          # Передаем бойцу меч
    battle(hero, monster)           # Запускаем бой

    print()  # Пустая строка для разделения боёв в консоли

    # Бой 2 — с луком
    bow = Bow()
    hero.set_weapon(bow)
    battle(hero, monster)

    print()  # Разделитель

    # Бой 3 — с новым оружием (например, топор), без изменения старого кода!
    axe = Axe()
    hero.set_weapon(axe)
    battle(hero, monster)

# C:\Users\VA_Biryukov\AppData\Local\Programs\Python\Python310\python.exe D:\Documents\GitHub\bva-repository\test13.py
# Боец выбирает Sword
# Боец боец наносит удар мечом
# Монстр побежден!

# Боец выбирает Bow
# Боец боец наносит удар из лука
# Монстр побежден!

# Боец выбирает Axe
# Боец боец рубит топором
# Монстр побежден!
# Process finished with exit code 0