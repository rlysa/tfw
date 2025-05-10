import sqlite3

from config import DB_NAME


def new_task(task, admin):
    name, interns, description, deadline, report = task['name'], ' '.join(task['selected']), task['description'], task['deadline'], task['report']

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Tasks (name, interns, admin, description, deadline, report, done) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (name, interns, admin, description, deadline, report, 'False'))
    connection.commit()
    connection.close()
