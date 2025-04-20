import sqlite3

from config import DB_NAME



def delete_user(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Users WHERE username={username}')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    delete_user('rlysa')
