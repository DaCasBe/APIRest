import psycopg2

# Hay que rellenar los campos de la función connect


def create_database():
    connection = psycopg2.connect(
        database="", user="", password="", host="", port="")
    connection.autocommit = True

    cursor = connection.cursor()

    sql = '''CREATE DATABASE apirest'''

    cursor.execute(sql)

    connection.close()


def create_table_joke():
    connection = psycopg2.connect(
        database="", user="", password="", host="", port="")

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS JOKE")

    sql = '''
		CREATE TABLE JOKE (
			id_joke integer primary key,
			description text not null
		)
	'''

    cursor.execute(sql)
    connection.commit()

    connection.close()


if __name__ == "__main__":
    create_database()
    create_table_joke()
