import sqlite3  # Import SQLite library

CAMERA_DATABASE = 'CameraInfo.db'
TABLE_NAME = 'VideoMetadata'


def read_metadata_from_db():
    """Reads and prints all entries from the CameraMetadata table."""
    conn = sqlite3.connect(CAMERA_DATABASE)
    # conn = sqlite3.connect('CameraInfo.db')
    c = conn.cursor()
    
    c.execute(f"SELECT * FROM {TABLE_NAME}")
    # c.execute("SELECT * FROM VideoMetadata")
    rows = c.fetchall()  # Fetch all rows from the executed query
    
    if rows:
        print("Current entries in the CameraMetadata database:")
        for row in rows:
            print(f"ID: {row[0]}, Camera Name: {row[1]}, Camera IP: {row[2]}, "
                  f"Location: {row[3]}, Start Time: {row[4]}, Stop Time: {row[5]}, "
                  f"Video Filename: {row[6]}")
    else:
        print(f"No entries found in the {CAMERA_DATABASE} database.")
        # print("No entries found in the CameraMetadata database.")

    conn.close()

# Call this function to display the entries
read_metadata_from_db()