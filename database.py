import sqlite3

class Db:

    def __init__(self):
        self.conn = sqlite3.connect('draw.db')
        self.cursor = self.conn.cursor()

########################### DRAW
    # добавляема розыгрыш в бд
    def add_post(self, id_post, data_post):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS draw (
                id_post INTEGER PRIMARY KEY AUTOINCREMENT,
                data_post datetime,
                use boll
            )
        ''')

        self.cursor.execute('''
            INSERT INTO draw (id_post, data_post, use) VALUES (?, ?, ?)
            ''', (id_post, data_post, 1))

        self.conn.commit()
        self.conn.close()

    # достаем активные розыгрыши
    def post_use(self):

        self.cursor.execute(
            'select * from draw where use = 1')

        return self.cursor.fetchall()

########################### USERS

    # добавляема пользователя в бд
    def add_user(self, info_users):

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                serial_number INTEGER,
                id_post INTEGER,
                data_coments datetime,
                id_user INTEGER,
                last_name TEXT,
                first_name TEXT,
                username TEXT,
                message_text TEXT    
                
            )
        ''')

        max_num = Db().max_num_post(info_users)[0][0]

        self.cursor.execute('''
                    INSERT INTO users ( serial_number, id_post, data_coments, id_user, last_name, first_name, username, message_text) VALUES
                                     ( ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',  ( max_num+1,
                                       info_users['id_post'],
                                       info_users['data_coments'],
                                       info_users['id_users'],
                                       info_users['last_name'],
                                       info_users['first_name'],
                                       info_users['username'],
                                       info_users['message_text']))




        self.conn.commit()
        self.conn.close()

        return max_num+1

    # достаем активные розыгрыши
    def max_num_post(self, info_users):
        self.cursor.execute(
             f'''
                select count(*) from users
                where id_post = {info_users['id_post']}
             ''')

        return self.cursor.fetchall()

    # закрываем все розыгрыши
    def up_posts(self):
        self.cursor.execute(
                    f'''
                        update  draw
                        set use = 0
                        
                     ''')

        self.conn.commit()
        self.conn.close()

    # проверка, занесен ли этот юзер
    def check_user_for_post(self, user):

        self.cursor.execute(
            f'''
                select count(*) from users
                where id_post = {user['id_post']}
                  and id_user = {user['id_users']}
             ''')

        return self.cursor.fetchall()