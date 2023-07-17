import psycopg2


class DBConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="work",
            password="fasgas")
        self.cursor = self.conn.cursor()

    def check_connection(self):
        # display the PostgreSQL database server version
        db_version = self.cursor.fetchone()
        print(db_version)

    def get_from_db(self, query="select * from worker", value=()):
        # Чтение из таблицы
        self.cursor.execute(query, value)
        mobile_records = self.cursor.fetchall()
        return mobile_records

    def to_db(self, value=('2023-03-03', 1, 1)):
        # запись в БД
        sql = """INSERT INTO worker (data_time, fio, machine) VALUES (%s, %s, %s);"""
        self.cursor.execute(sql, value)
        self.conn.commit()

    def check_workers(self, id_worker):
        query_res = self.get_from_db(query="select * from workersID WHERE id_worker = %s",
                                     value=(int(id_worker),))

        return len(query_res)

    def add_new_workers(self, id_worker, full_name):
        sql = """INSERT INTO workersID (id_worker, full_name) VALUES (%s, %s);"""
        self.cursor.execute(sql, (id_worker, full_name))
        self.conn.commit()

    def __del__(self):  # Деструктор класса
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

