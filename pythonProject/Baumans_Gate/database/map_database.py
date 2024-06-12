#класс для работы с базой данных, куда будут записываться сериализованные пиклы
from .db_config import host, user, password, db_name
import psycopg2
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('database/db_logs.txt','a','utf-8')
formatter = logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)s-8s [%(asctime)s]  %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Database:
    def __init__(self):
        pass

    def insert_into(self, file_path):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = connection.cursor()

            with open(file_path, 'rb') as f:
                pickled_data = f.read()

            name = input('Введите название карты...\n')

            query = "INSERT INTO maps (data, name) VALUES (%s, %s)"
            values = (psycopg2.Binary(pickled_data), name)
            cursor.execute(query, values)
            logger.info('Карта успешно добавлена в БД')
            connection.commit()

        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
            logger.error(ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                logger.info('Завершение подключения к БД')
                print('PostgreSQL connection closed')

    def delete_from(self, NAME):

        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = connection.cursor()

            query = "DELETE FROM maps WHERE name = %s"
            values = (NAME,)
            cursor.execute(query, values)
            connection.commit()
            print(f'Карта {NAME} была успешно удалена')
            logger.info('Успешное удаление данных из БД')
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
            logger.error(ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                logger.info('Завершение подключения к БД')
                print('PostgreSQL connection closed')

    def show_maps(self):

        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = connection.cursor()

            query = "SELECT name FROM maps"
            cursor.execute(query)
            data = cursor.fetchall()
            data = list(data)
            connection.commit()
            print(data)
            logger.info('Карты из БД успешно показаны')
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
            logger.error(ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                logger.info('Завершение подключения к БД')
                print('PostgreSQL connection closed')

    def update_table(self, DATA, NAME):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = connection.cursor()

            query = "UPDATE maps SET data = %s WHERE name = %s"
            values = (DATA, NAME)
            cursor.execute(query, values)
            connection.commit()
            print(f'Карта {NAME} была успешно изменена')
            logger.info('Успешное обновление данных в таблице')
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
            logger.error(ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                logger.info('Завершение подключения к БД')
                print('PostgreSQL connection closed')

    def return_map(self, name):
        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            cursor = connection.cursor()

            query = "SELECT data FROM maps WHERE name = %s"
            values = (name,)
            cursor.execute(query, values)
            data = cursor.fetchone()
            connection.commit()
            logger.info('Карта из БД успешно передана в программу')
            return data
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
            logger.error(ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                logger.info('Завершение подключения к БД')
                print('PostgreSQL connection closed')