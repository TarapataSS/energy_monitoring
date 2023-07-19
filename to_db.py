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
        
    def add_reg(self, reg_ip, reg_info):
        """
        Запись нового работника в БД
        :param id_worker:
        :param full_name:
        """
        sql = """INSERT INTO regs (reg_ip, reg_info) VALUES (%s, %s);"""
        self.cursor.execute(sql, (reg_ip, reg_info))
        self.conn.commit()

    def __del__(self):  # Деструктор класса
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
