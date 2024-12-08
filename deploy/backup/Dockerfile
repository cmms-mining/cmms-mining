FROM postgres:16-alpine

# Установка cron и PostgreSQL клиента
RUN apk add --no-cache postgresql-client bash curl tzdata && \
    apk add --no-cache --virtual .build-deps gcc libc-dev && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*
RUN apk add --no-cache tzdata
ENV TZ Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Копирование скрипта бэкапа
COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

# Копирование задания cron
COPY cronjob /etc/crontabs/root

# Создание директории для бэкапов
RUN mkdir -p /backups

# Настройка cron для выполнения
CMD ["crond", "-f"]
