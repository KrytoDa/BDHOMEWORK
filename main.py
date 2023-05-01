import psycopg2


def choose_what_to_do():
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
        add_new_client(conn, 'Иванов', 'Иван','Ivanov@mail.ru')
        print()
        print('Клиент был добавлен')
    elif lol == 0:
        delete_all(conn)
        print()
        print('Все было удалено')
    elif lol == 3:
        add_number_client(conn, 1, 24323)
    elif lol == 4:
        update_info(conn, 1, None, None, 'lol212@mail.ru')
    elif lol == 5:
        delete_number(conn, 1, 8988)
    elif lol == 6:
        delete_client(conn, 1)
    elif lol ==7:
        find_client(conn, 'Иванов')

conn = psycopg2.connect(database='netology_db', user='postgres', password='Ivankov12')

def create_table(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email TEXT UNIQUE
        );
        """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(id),
                phone VARCHAR(20) UNIQUE
                );
                """)

def add_new_client(conn, first_name, last_name, email):
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email)
        VALUES(%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email))

    print(f'Новый клиент добавлен: {cur.fetchone()[0]}')

def add_number_client(conn, client_id, phone):
    cur.execute("""
               INSERT INTO phones(client_id, phone) VALUES(%s, %s);
               """, (client_id, phone))

    cur.execute("""
            SELECT first_name, last_name
            FROM clients AS cl
            JOIN phones AS p
            ON cl.id = p.client_id
            WHERE cl.id=%s;
            """, (client_id,))
    print(f'Номер телефона клиента {cur.fetchone()[1]} добавлен.')

def update_info(conn, id, first_name=None, last_name=None, email=None):
    cur.execute("""
        SELECT *
        FROM clients
        WHERE id=%s;
        """, (id,))
    client = cur.fetchone()
    if first_name is None:
        first_name = client[1]
    if last_name is None:
        last_name = client[2]
    if email is None:
        email = client[3]
    cur.execute("""
        UPDATE clients SET first_name=%s, last_name=%s, email=%s
        WHERE id=%s;
        """, (first_name, last_name, email, id))
    print(f'Данные клиента {last_name} обновлены.')

def delete_number(conn, id, phone):
    cur.execute("""
        SELECT EXISTS(
        SELECT *
        FROM clients
        WHERE id=%s
        );
        """, (id,))
    client = cur.fetchone()[0]
    if client is False:
        print('Такого клиента нет.')
    else:
        cur.execute("""
            DELETE
            FROM phones
            WHERE phone=%s;
            """, (phone,))
        print(f'Телефон {phone} удален.')

def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM phones
        WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM clients
        WHERE id=%s;
        """, (client_id,))
    conn.commit()
    print('Все данные о клиенте удалены.')

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
            SELECT cl.id FROM clients AS cl
            JOIN phones AS ph ON ph.client_id = cl.id
            WHERE ph.phone=%s;
            """, (phone,))
    else:
        cur.execute("""
            SELECT id FROM clients 
            WHERE first_name=%s or last_name=%s or email=%s;
            """, (first_name, last_name, email))
    print(cur.fetchall())

choose_what_to_do()