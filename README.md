- [x] развернуть БД

Чтобы восстановить таблицы БД, используйте команды SQL в файле `init_db.sql`

Когда код `bot_code.py` запущен, бота можно использовать в телеграмме в @energy_monitoring_log_bot

https://dzen.ru/media/bu11zy/kak-ustanovit-i-nastroit-postgresql-i-dbeaver-v-wsl-v-windows-11-630f40cc9846372162d467e1

Для бота нужна библиотека: PyTelegramBotAPI

Чтобы сделать меню: https://stackoverflow.com/questions/34457568/how-to-show-options-in-telegram-bot



#### Заметки
Удалить все строки в таблице:
```
TRUNCATE TABLE workersid; 
```
Удаление таблиц недоступно, если запущен бот (так как там происходить взаимодействие с БД)

