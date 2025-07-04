# Система управления учетными записями пользователей

class User:
# Базовый класс для пользователя.
# Содержит ID, имя и уровень доступа.

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