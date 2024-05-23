import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Function to get .bicep file paths from a local directory
def get_bicep_file_paths(local_directory):
    bicep_file_paths = []
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            if file.endswith('.bicep'):
                bicep_file_paths.append(os.path.join(root, file))
    return bicep_file_paths

# Path to the local directory containing Bicep modules
local_directory = r'D://Bicep-Templates//bicep_env//src//avm//res'

# Get the list of .bicep file paths from the local directory
bicep_file_paths = get_bicep_file_paths(local_directory)

# Database setup
db_path = 'bicep_files.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BicepFiles (
        id INTEGER PRIMARY KEY,
        path TEXT NOT NULL
    )
''')

# Insert file paths into the database
cursor.executemany('INSERT INTO BicepFiles (path) VALUES (?)', [(path,) for path in bicep_file_paths])
conn.commit()

# Verify database content
cursor.execute('SELECT * FROM BicepFiles')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()
