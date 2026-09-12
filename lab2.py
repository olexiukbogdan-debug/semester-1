users = {
    "bohdan": {"password": "1234", "grades": [12, 10, 8, 5, 4, 3]},
    "anna": {"password": "1111", "grades": [11, 9, 7, 6, 5]},
    "oleh": {"password": "2222", "grades": [4, 3, 2, 1, 8]},
    "maria": {"password": "3333", "grades": [12, 10, 9, 6, 4]}
}

login = input("Логін: ")
password = input("Пароль: ")

if login in users and users[login]["password"] == password:
    grades = users[login]["grades"]
    good = sum(5 <= grade <= 12 for grade in grades)
    bad = sum(1 <= grade <= 4 for grade in grades)

    print("Оцінки:", grades)
    print("Задовільних оцінок:", good)
    print("Незадовільних оцінок:", bad)
else:
    print("Неправильний логін або пароль")
