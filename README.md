-[ ] развернуть БД

https://dzen.ru/media/bu11zy/kak-ustanovit-i-nastroit-postgresql-i-dbeaver-v-wsl-v-windows-11-630f40cc9846372162d467e1

Для бота нужна библиотека:
PyTelegramBotAPI


Для работы с БД:
```
CREATE TABLE worker (
    data_time timestamp,
    fio varchar(255),
    machine varchar(255))
```

```
CREATE TABLE workersID (
id_worker INT,
full_name varchar(255)
)
```

```
TRUNCATE TABLE workersid; 
```