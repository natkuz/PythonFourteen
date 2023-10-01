import json
import os

from exceptions import AccessError, LevelError, NameAccessError, IDAccessError

class User:

    def __init__(self, name: str, u_id: str, lvl: int):
        self.name = name
        self.u_id = str(u_id).zfill(6)
        self.lvl = int(lvl)

    def __str__(self):
        return f'Имя: {self.name} ({self.u_id}) -- Уровень доступа: {self.lvl}'

    def __repr__(self):
        return f'User({self.name}, {self.u_id}, {self.lvl})'

    def __hash__(self):
        return hash((self.name + self.u_id) * self.lvl)

    def __eq__(self, other):
        if not isinstance(other, User):
            raise TypeError
        return self.name == other.name and self.u_id == other.u_id


class Terminal:

    def __init__(self):
        self.user_base = Terminal.users_db()

    @staticmethod
    def users_db():
        users_list = set()
        with open('users.json', 'r', encoding='UTF-8') as file:
            data_users = json.load(file)
        for lvl, users in data_users.items():
            for user in users:
                name, u_id = user
                users_list.add(User(name, u_id, lvl))
        return users_list

    def login(self, name: str, u_id: str):
        log_user = User(name, u_id, 0)
        users_name = [u_name.name for u_name in self.user_base]
        if name in users_name:
            for cur_user in self.user_base:
                if cur_user == log_user:
                    return cur_user
            raise IDAccessError(name, u_id)
        raise NameAccessError(name)

    def create_new_user(self, log_user: User, new_user: User):
        if new_user.lvl < log_user.lvl:
            raise LevelError(log_user.lvl, new_user.lvl)
        user_dict = {}
        self.user_base.add(new_user)
        for user in self.user_base:
            if user.lvl in user_dict:
                user_dict[user.lvl].append([user.name, user.u_id])
            else:
                user_dict[user.lvl] = [[user.name, user.u_id]]
        with open('users.json', 'w', encoding='UTF-8') as file:
            json.dump(user_dict, file, indent=4, ensure_ascii=False)
        return f'Новый пользователь {new_user.name} добавлен'

    def users(self):
        users = []
        for user in self.user_base:
            users.append(user)
        return users


def create_json(path: str = 'users.json'):
    MIN_LVL = 1
    MAX_LVL = 7
    user_data = {}
    id_list =[]
    while True:
        if os.path.exists(path):
            with open(path, 'r', encoding='UTF-8') as file:
                user_data = json.load(file)
        if user_data:
            for users in user_data.values():
                for user in users:
                    id_list.append(user[1])
        name = input("Введите имя пользователя: ")
        if not name:
            break
        while True:
            u_id = input("Введите личный ID: ")
            if u_id.isdigit():
                if int(u_id) not in id_list:
                    u_id = int(u_id)
                    break
                else:
                    print(f'ID {u_id} уже занят. Введите другой ID.')
            else:
                print('ID должен быть целым числом')
        while True:
            u_lvl = input("Введите уровень доступа: ")
            if u_lvl.isdigit() and MIN_LVL <= int(u_lvl) <= MAX_LVL:
                break
            else:
                print(f'Уровень доступа должен быть от {MIN_LVL} до {MAX_LVL}')

        if u_lvl in user_data:
            user_data[u_lvl].append((name, u_id))
        else:
            user_data[u_lvl] = [(name, u_id)]

        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(user_data, file, indent=6, ensure_ascii=False)


# create_json()

user_base = Terminal()
login_user = user_base.login('Василиса Аендреевна', '000256')
# print(login_user)
new_user = User('Петр Иванов', '222', 5)

# user_base.users()
# user_o = User('Антон П', '546', 6)
user_t = User('Василиса Аендреевна', '256', 3)
# print(Terminal().create_new_user(user_t, new_user))
# print(user_t.__str__())
# print(user_t.__eq__(user_o))
print(Terminal().users())
