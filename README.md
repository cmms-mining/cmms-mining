# Компьютеризированная система управления техническим обслуживанием (CMMS Computerized Maintenance Management System)

Система представляет из себя CRM для использования в сервисной компании производственного сектора

Если у Вас есть желание помочь в развитии - будем рады предложениям и Pull Request'ам

Проект использует Django 5.1, Python 3.11

## Установка и запуск на локальной машине

### Для локального запуска потребуется создать виртуальное окружение (пример на Windows)

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

### Также возможен локальный запуск в docker-compose

Команда для развертывания и запуска с загрузкой фикстур:

```bash
docker-compose -f docker-compose-dev-fixture.yml up --build
```
Команда для развертывания и запуска без фикстур:

```bash
docker-compose -f docker-compose-dev.yml up --build
```

Имя пользователя: admin  
Пароль: admin