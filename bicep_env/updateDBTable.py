import sqlite3

def extract_service_type(file_path):
    # Extract service type from file path
    # Assuming the service type is the second to last directory in the path
    parts = file_path.split("\\")
    if len(parts) > 2:
        return parts[-3]  # Adjust the index based on the actual path structure
    return "Unknown"

# Connect to the SQLite database
conn = sqlite3.connect('bicep_modules.db')
cursor = conn.cursor()

# Fetch all records
cursor.execute('SELECT id, path FROM bicep_modules')
records = cursor.fetchall()

# Update each record with the service type
for record in records:
    record_id, file_path = record
    service_type = extract_service_type(file_path)
    cursor.execute('UPDATE bicep_modules SET service_type = ? WHERE id = ?', (service_type, record_id))

conn.commit()
conn.close()
