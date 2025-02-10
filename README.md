# "это-хобби.рф"
Моя личная соц сеть.

### Описание
Бэкенд api для моей соц сети. Тут будет описание возможно когда-то.

### Технологии
Python 3.12.4
Django 5.1.4
djangorestframework 3.15.2

### Запуск проекта в dev-режиме:
- Клонируйте код и Гитхаб себе на ПК
```
git clone git@github.com:temka778/Hobby-backend.git
```
- Перейдите в папку "Hobby-backend"
```
cd Hobby-backend
```
- Установите и активируйте виртуальное окружение (пример команды для Windows)
```
python -m venv venv
```
```
source venv/Scripts/activate
```
- Установите и активируйте виртуальное окружение (пример команды для Linux)
```
python3 -m venv venv
```
```
source venv/bin/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Перейдите во вложенную папку "hobby_backend" выполните миграции
```
cd hobby_backend
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Создайте сразу суперпользователя, для доступа в админку и запустите уже наконец локальный сервер!
```
python manage.py createsuperuser
```
```
python manage.py runserver
```
### Автор
Артём
