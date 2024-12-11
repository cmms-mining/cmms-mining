# Компьютеризированная система управления техническим обслуживанием (CMMS Computerized Maintenance Management System)

Если у Вас есть желание помочь в развитии - будем рады предложениям и Pull Request'ам

Проект использует Django 5.1, Python 3.11

## Конфигурация

Конфигурация хранится в `environment/.env.dev-docker`

## Установка и запуск на локальной машине

Для локального запуска требуется docker и docker-compose

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