import psycopg2

# Подключаемся к PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="work",
    password="fasgas")

cursor = conn.cursor()

print('PostgreSQL database version:')
cursor.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cursor.fetchone()
print(db_version)

# Чтение из таблицы
postgreSQL_select_Query = "select * from worker"
cursor.execute(postgreSQL_select_Query)
print("Selecting rows from mobile table using cursor.fetchall")
mobile_records = cursor.fetchall()
print(mobile_records)


# запись в БД
sql = """INSERT INTO worker (data_time, fio, machine) VALUES (%s, %s, %s);"""
cursor.execute(sql, ('2023-03-03', 1, 1))
conn.commit()

# закрываем курсор
if conn is not None:
    conn.close()
    print('Database connection closed.')