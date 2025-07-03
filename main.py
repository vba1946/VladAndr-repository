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



