import psycopg2

def choose_what_to_do():
    while True:
        print('Функция, создающая структуру БД (таблицы) -- Введите цифру - 1',
          'Функция, позволяющая добавить нового клиента -- Введите цифру - 2',
          'Функция, позволяющая добавить телефон для существующего клиента. -- Введите цифру - 3',
          'Функция, позволяющая изменить данные о клиенте. -- Введите цифру - 4',
          'Функция, позволяющая удалить телефон для существующего клиента. -- Введите цифру - 5',
          'Функция, позволяющая удалить существующего клиента. -- Введите цифру - 6',
          'Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону. -- Введите цифру - 7',
          'Функция, удаляющая все -- Введите цифру - 0', sep= '\n')
        lol = int(input())
        if lol == 1:
            create_table(conn)
            print()
            print('Таблицы были созданы')
        elif lol == 2:
            add_new_client(conn, 'Иванов', 'Иван','Ivanov@mail.ru', 8988)
            add_new_client(conn, 'Оленев', 'Олень', 'olen@mail.ru')
            print()
            print('Клиент был добавлен')
        elif lol == 0:
            delete_all(conn)
            print()
            print('Все было удалено')
        elif lol == 3:
            add_number_client(conn, 1, 14312)
            add_number_client(conn, 2, 24323)
        elif lol == 4:
            update_info(conn, 1, None, None, 'lol212@mail.ru')
        elif lol == 5:
            delete_number(conn, 2, 24323)
        elif lol == 6:
            delete_client(conn, 1)
        elif lol ==7:
            find_client(conn, 'Иванов')
            print('Конец программы')
            break





conn = psycopg2.connect(database='netology_db', user='postgres', password='Ivankov12')

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE,
            last_name VARCHAR(40) UNIQUE,
            email  VARCHAR(255) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            number INTEGER,
            client_id INTEGER  REFERENCES client(client_id)
        );
        """)
        conn.commit()


def add_new_client(conn, first_name, last_name, email, number = None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) VALUES( %s, %s, %s);
        """, (first_name, last_name, email))
        cur.execute("""
        INSERT INTO phone(number) VALUES( %s);
        """, (number, ))
        cur.execute("""
        SELECT * FROM client;
        """)
        print(cur.fetchall())
        cur.execute("""
        SELECT * FROM phone;
        """)
        print(cur.fetchall())
        conn.commit()


def delete_all(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        conn.commit()

def add_number_client(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone(client_id, number) VALUES(%s, %s);
        """, (client_id, number))
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name
        FROM client AS cl
        JOIN phone AS p
        ON cl.client_id = p.client_id
        WHERE cl.client_id=%s;
        """, (client_id,))
        print(f'Номер телефона клиента {cur.fetchone()[1]} добавлен.')


def update_info(conn, client_id, first_name = None, last_name = None, email = None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT *
        FROM client
        WHERE client_id=%s;
        """, (client_id,))
        client = cur.fetchone()
        if first_name is None:
            first_name = client[1]
        if last_name is None:
            last_name = client[2]
        if email is None:
            email = client[3]
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client SET first_name=%s, last_name=%s, email=%s
        WHERE client_id=%s;
        """, (first_name, last_name, email, client_id))
        print(f'Данные клиента {last_name} обновлены.')


def delete_number(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT EXISTS(
        SELECT *
        FROM client
        WHERE client_id=%s
        );
        """, (client_id,))
        client = cur.fetchone()[0]
        if client is False:
            print('Такого клиента нет.')
        else:
            with conn.cursor() as cur:
                cur.execute("""
                DELETE
                FROM phone
                WHERE number=%s;
                """, (number,))
                print(f'Телефон {number} удален.')


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone
        WHERE client_id=%s;
         """, (client_id,))
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client
        WHERE client_id=%s;
        """, (client_id,))
        conn.commit()
        print('Все данные о клиенте удалены.')


def find_client(conn, first_name = None, last_name = None, email = None, number = None):
    if number is not None:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT cl.client_id FROM client AS cl
            JOIN phone AS ph ON ph.client_id = cl.client_id
            WHERE ph.phone=%s;
            """, (number,))
    else:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM client 
            WHERE first_name=%s or last_name=%s or email=%s;
            """, (first_name, last_name, email))
            print(cur.fetchall())



choose_what_to_do()
