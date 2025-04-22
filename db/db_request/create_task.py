import sqlite3
from datetime import datetime

from config import DB_NAME


def new_task(task, admin):
    name, interns, description, deadline, report = task['name'], ' '.join(task['selected']), task['description'], task['deadline'], task['report']
    deadline = datetime.strptime(deadline, "%d.%m.%Y").date()

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO Tasks (name, interns, admin, description, deadline, report) VALUES (?, ?, ?, ?, ?, ?)''',
                   (name, interns, admin, description, deadline, report))
    connection.commit()
    connection.close()
