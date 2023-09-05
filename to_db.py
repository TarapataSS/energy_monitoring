import psycopg2


class DBConnection:
    def __init__(self):
        """
        для подключения к БД
        """
        self.conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="tarapatas",
                password="fasgas")
        self.cursor = self.conn.cursor()

    def check_connection(self):
            """
            вывод на экран версии PostgreSQL БД
            """
            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cursor.fetchone()
            print(db_version)

    def get_from_db(self, query="select * from worker", value=()):
        """
        Получить данные из БД
        :param query: запрос
        :param value: аргументы
        :return: итоговая таблица
        """
        self.cursor.execute(query, value)
        mobile_records = self.cursor.fetchall()
        return mobile_records

    def add_new_event(self, value):
        """
        запись нового события в БД
        :param value:
        """
        sql = """INSERT INTO event (data_time, id_worker, action, machine) VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, value)
        self.conn.commit()

    def check_workers(self, id_worker):
        """
        проверка, есть ли работник в БД
        :param id_worker:
        :return:
        """
        query_res = self.get_from_db(query="select * from workers WHERE id_worker = %s",
                                     value=(int(id_worker),))

        return len(query_res)

    def add_new_workers(self, id_worker, full_name):
        """
        Запись нового работника в БД
        :param id_worker:
        :param full_name:
        """
        sql = """INSERT INTO workers (id_worker, full_name) VALUES (%s, %s);"""
        self.cursor.execute(sql, (id_worker, full_name))
        self.conn.commit()
        
    def add_reg(self, table_name, addresses_names, *args):
        names_string = ', '.join([str(i) for i in addresses_names])
        values_string =', '.join(['%s' for _ in addresses_names])
        sql = """INSERT INTO """+table_name+""" ("""+names_string+""") VALUES ("""+values_string+""");"""
        self.cursor.execute(sql, args)
        self.conn.commit()

    def database_count(self, table_name):
        # Получение количества записей в таблице
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = self.cursor.fetchone()[0]
        return count
    
    def period(self, table_name):
        # Получение периода записи
        self.cursor.execute(f"SELECT reading_time FROM {table_name} ORDER BY reading_time ASC LIMIT 1;")
        begin = self.cursor.fetchone()[0]
        self.cursor.execute(f"SELECT reading_time FROM {table_name} ORDER BY reading_time DESC LIMIT 1;")
        end = self.cursor.fetchone()[0]
        return begin, end

    def save_data(self, table_name):
        # Получение записей из таблицы
        self.cursor.execute(f"SELECT * FROM {table_name} ORDER BY reading_time DESC;")
        records = self.cursor.fetchall()
        return records

    def __del__(self):  # Деструктор класса
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
