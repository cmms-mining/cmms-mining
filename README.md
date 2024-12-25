# Компьютеризированная система управления техническим обслуживанием (CMMS Computerized Maintenance Management System)

Проект представляет из себя веб-приложение для использования в сервисной компании производственного сектора

Если у Вас есть желание помочь в развитии - будем рады предложениям и Pull Request'ам

Проект использует Django 5.1, Python 3.11

## Установка и запуск на локальной машине

### Пример локального запуска в Windows

Клонирование репозитория
```bash
git clone https://github.com/cmms-mining/cmms-mining.git .
```
Создание и активация виртуального окружения
```bash
python.exe -m venv venv
```
```bash
.\venv\Scripts\activate
```
Установка нужных библиотек
```bash
pip install -r .\requirements-dev.txt
```
Создание базы данных (Sqlite3)
```bash
python.exe .\source\manage.py migrate
```
Наполнение базы данных тестовыми данными
```bash
python .\source\manage.py loaddata .\source\fixtures\fixtures.json
```
Запуск локального сервера приложения
```bash
python.exe .\source\manage.py runserver 
```

### Пример локального запуска в Docker

Команда для развертывания и запуска с загрузкой фикстур:

```bash
docker-compose -f docker-compose-dev-fixture.yml up --build
```
Команда для развертывания и запуска без фикстур:

```bash
docker-compose -f docker-compose-dev.yml up --build
```

Суперюзер  
Имя: admin  
Пароль: admin

Обычный пользователь  
Имя: user  
Пароль: user