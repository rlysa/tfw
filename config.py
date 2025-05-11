import dotenv
import os
dotenv.load_dotenv()


TOKEN = os.getenv('TOKEN') or '****'
ADMIN_FATHER_PSW = os.getenv('ADMIN_FATHER_PSW') or ''
ADMIN_PSW = os.getenv('ADMIN_PSW') or '****'
DB_NAME = os.getenv('DB_NAME') or 'db/db/thw_db.db'