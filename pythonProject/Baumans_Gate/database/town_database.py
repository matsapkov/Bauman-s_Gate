#класс для работы с базой данных, куда будут записываться сериализованные пиклы
from Baumans_Gate.database.db_config import host, user, password, db_name
import psycopg2


class CityDatabase:
    def __init__(self):
        pass

    def insert_into_(self, file_path):
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

            name = input('Введите название города...\n')
            login = input('Введите логин пользователя... \n')
            user_password = input('Введите пароль для пользователя... \n')

            query = "INSERT INTO city_data (data, username, password, city_name) VALUES (%s, %s, %s, %s)"
            values = (psycopg2.Binary(pickled_data), login, user_password, name)
            cursor.execute(query, values)

            connection.commit()

        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print('PostgreSQL connection closed')

    def return_town(self, login, user_password):
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

            query = "SELECT data FROM city_data WHERE username = %s and password = %s"
            values = (login, user_password,)
            cursor.execute(query, values)
            data = cursor.fetchone()
            connection.commit()
            return data
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print('PostgreSQL connection closed')

    def update_table_(self, DATA, NAME):

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

            query = "UPDATE city_data SET data = %s WHERE city_data.city_name = %s"
            values = (DATA, NAME)
            cursor.execute(query, values)
            connection.commit()
            print(f'Город {NAME} был успешно изменен')
        except Exception as ex:
            print('[INFO] Error while working with PostgreSQL', ex)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print('PostgreSQL connection closed')
