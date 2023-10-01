# 📌На семинаре 13 был создан проект по работе с пользователями (имя, id, уровень).
# 📌Напишите 3-7 тестов unittest для данного проекта.
# 📌Используйте setUp

import unittest
from PythonFourteen import user_class

class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user_one = user_class.User('Антон П', '546', 6)
        self.user_two = user_class.User('Василиса Аендреевна', '256', 3)
        self.user_three = user_class.User('Петр Иванов', '222', 5)
        self.user_base = user_class.Terminal()
        self.login_user = self.user_base.login('Василиса Аендреевна', '000256')
        
    def test_str(self):
        self.assertEqual(self.user_two.__str__(), 'Имя: Василиса Аендреевна (000256) -- Уровень доступа: 3')

    def test_eq(self):
        self.assertEqual(self.user_two, self.user_two)
        self.assertFalse(self.user_one == self.user_two)
        
    def test_login(self):
        self.assertTrue(self.login_user, 'Имя: Василиса Аендреевна (000256) -- Уровень доступа: 3')

    def test_create_user(self):
        self.assertTrue(user_class.Terminal().create_new_user(self.user_two, self.user_three)
                        == 'Новый пользователь Петр Иванов добавлен')


if __name__ == '__main__':
    unittest.main(verbosity=2)