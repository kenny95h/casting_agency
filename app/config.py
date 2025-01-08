import os
SECRET_KEY = os.urandom(32)

# Enable debug mode.
DEBUG = True

# REMOVED PERSONAL LOGIN DETAILS
# Connect to the database
db_name = "postgres"
db_pword = "CHANGETOPASSWORD"

try:
    database_path = os.environ['DATABASE_URL']
    if database_path.startswith("postgres://"):
        database_path = database_path.replace("postgres://", "postgresql://", 1)
except:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = f'postgresql://{db_name}:{db_pword}@localhost:5432/castingapp'

