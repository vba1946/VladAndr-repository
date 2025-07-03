# Задача: Разработай систему управления учетными записями пользователей для небольшой компании
# Компания разделяет сотрудников на обычных работников и администраторов.
# У каждого сотрудника есть уникальный идентификатор (ID), имя и уровень доступа.
# Администраторы, помимо обычных данных пользователей, имеют дополнительный уровень доступа и могут добавлять или удалять пользователя из системы.

# Требования: 1.Класс `User*: Этот класс должен инкапсулировать данные о пользователе: ID, имя и уровень доступа ('user' для обычных сотрудников).
# 2.Класс `Admin`: Этот класс должен наследоваться от класса `User`.
# Добавь дополнительный атрибут уровня доступа, специфичный для администраторов ('admin').
# Класс должен также содержать методы `add_user` и `remove_user`, которые позволяют добавлять и удалять пользователей из списка
# представь, что это просто список экземпляров `User`).
# 3.Инкапсуляция данных: Убедись, что атрибуты классов защищены от прямого доступа и модификации снаружи.
# Предоставь доступ к необходимым атрибутам через методы (например, get и set методы).

class User:
    def __init__(self, user_id, name):
        self.__user_id = user_id     # Инкапсулированный атрибут
        self.__name = name           # Инкапсулированный атрибут
        self.__access_level = 'user' # Уровень доступа по умолчанию

    # Геттеры для доступа к приватным атрибутам
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_access_level(self):
        return self.__access_level

    def __str__(self):
        return f"ID: {self.__user_id}, Имя: {self.__name}, Уровень доступа: {self.__access_level}"


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.__access_level = 'admin'  # Уровень доступа для администратора

    def get_access_level(self):
        return self.__access_level

    def add_user(self, user_list, user):
        """
        Добавляет пользователя в список пользователей.
        Проверяет, что пользователь не существует с таким ID.
        """
        if any(u.get_user_id() == user.get_user_id() for u in user_list):
            print("Ошибка: Пользователь с таким ID уже существует.")
        else:
            user_list.append(user)
            print(f"Пользователь {user.get_name()} добавлен.")

    def remove_user(self, user_list, user_id):
        """
        Удаляет пользователя из списка по ID.
        """
        for user in user_list:
            if user.get_user_id() == user_id:
                user_list.remove(user)
                print(f"Пользователь с ID {user_id} удален.")
                return
        print(f"Ошибка: Пользователь с ID {user_id} не найден.")


# Пример использования
if __name__ == "__main__":
    # Создаем список пользователей
    users = []

    # Создаем администратора
    admin = Admin(1, "Александр")

    # Создаем обычных пользователей
    user1 = User(2, "Мария")
    user2 = User(3, "Иван")

    # Администратор добавляет пользователей
    admin.add_user(users, user1)
    admin.add_user(users, user2)

    # Выводим список пользователей
    print("\nСписок пользователей:")
    for u in users:
        print(u)

    # Администратор удаляет пользователя
    admin.remove_user(users, 2)

    # Выводим обновленный список
    print("\nОбновленный список пользователей:")
    for u in users:
        print(u)


# Задача: Создай класс `Task`, который позволяет управлять задачами (делами).
# У задачи должны быть атрибуты: описание задачи, срок выполнения и статус (выполнено/не выполнено). Реализуй функцию для добавления задач, отметки выполненных задач и вывода списка текущих (не выполненных) задач.
# *Дополнительное задание:
# Ты разрабатываешь программное обеспечение для сети магазинов.
# Каждый магазин в этой сети имеет свои особенности, но также существуют общие характеристики, такие как адрес, название и ассортимент товаров.
# Ваша задача — создать класс `Store`, который можно будет использовать для создания различных магазинов.
# Определяем класс User — базовый класс для обычных пользователей

"""
Система управления учетными записями пользователей
"""

class User:
    """
    Базовый класс для пользователя.
    Содержит ID, имя и уровень доступа.
    """

    def __init__(self, user_id, name):
        self.__user_id = user_id       # Приватный атрибут
        self.__name = name             # Приватный атрибут
        self.__access_level = 'user'   # Уровень доступа по умолчанию

    def get_user_id(self):
        """Получить ID пользователя"""
        return self.__user_id

    def get_name(self):
        """Получить имя пользователя"""
        return self.__name

    def get_access_level(self):
        """Получить уровень доступа"""
        return self.__access_level

    def set_name(self, new_name):
        """Изменить имя пользователя с проверкой"""
        if isinstance(new_name, str) and new_name.strip():
            self.__name = new_name
        else:
            raise ValueError("Имя должно быть непустой строкой.")

    def set_access_level(self, level):
        """Изменить уровень доступа (только 'user' или 'admin')"""
        if level in ['user', 'admin']:
            self.__access_level = level
        else:
            raise ValueError("Недопустимый уровень доступа. Используйте 'user' или 'admin'.")

    def __str__(self):
        """Строковое представление объекта"""
        return f"ID: {self.__user_id}, Имя: {self.__name}, Уровень доступа: {self.__access_level}"


class Admin(User):
    """
    Класс администратора, наследуется от User.
    Может добавлять и удалять пользователей.
    """

    def __init__(self, user_id, name):
        super().__init__(user_id, name)           # Вызываем конструктор родителя
        self.set_access_level('admin')           # Устанавливаем уровень доступа как 'admin'

    def add_user(self, user_list, user):
        """
        Добавляет пользователя в список.
        Проверяет уникальность ID.
        """
        for existing_user in user_list:
            if existing_user.get_user_id() == user.get_user_id():
                print("Ошибка: Пользователь с таким ID уже существует.")
                return
        user_list.append(user)
        print(f"Пользователь {user.get_name()} успешно добавлен.")

    def remove_user(self, user_list, user_id):
        """
        Удаляет пользователя из списка по ID.
        Если не найден — выводит сообщение об ошибке.
        """
        for user in user_list:
            if user.get_user_id() == user_id:
                user_list.remove(user)
                print(f"Пользователь с ID {user_id} удален.")
                return
        print(f"Ошибка: Пользователь с ID {user_id} не найден.")


# Точка входа в программу
if __name__ == "__main__":
    users = []  # Список пользователей компании

    # Создаём администратора
    admin = Admin(1, "Александр")
    print("Создан администратор:", admin)

    # Создаём обычных пользователей
    user1 = User(2, "Мария")
    user2 = User(3, "Иван")

    # Администратор добавляет пользователей
    admin.add_user(users, user1)
    admin.add_user(users, user2)

    # Выводим текущих пользователей
    print("\nСписок пользователей:")
    for u in users:
        print(u)

    # Изменяем имя одного из пользователей
    user1.set_name("Мария Петрова")
    print("\nИмя пользователя изменено:", user1)

    # Попытка установить недопустимый уровень доступа
    try:
        user1.set_access_level("manager")  # Неверное значение
    except ValueError as e:
        print("\nОшибка при изменении уровня доступа:", e)

    # Удаляем одного из пользователей
    admin.remove_user(users, 2)

    # Выводим обновлённый список
    print("\nОбновлённый список пользователей:")
    for u in users:
        print(u)


