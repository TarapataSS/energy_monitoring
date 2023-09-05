from to_db import DBConnection
import pandas as pd
import os

def fetch_and_save_data(db, table_name, csv_filename):
    count=db.database_count(table_name)  
    begin, end = db.period(table_name)     # Создание DataFrame из записей
    print(f"В таблице {table_name} {count} строк, период записи: {begin} - {end}")
    records = db.save_data(table_name)
    df = pd.DataFrame(records)
    df.to_csv(os.path.dirname(__file__)+'/'+csv_filename, index=False)

if __name__ == "__main__":
    try:
        db = DBConnection()
        fetch_and_save_data(db, 'sensor_data1', 'sensor_data1.csv')
        fetch_and_save_data(db, 'sensor_data2', 'sensor_data2.csv')
        fetch_and_save_data(db, 'sensor_data3', 'sensor_data3.csv')
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")