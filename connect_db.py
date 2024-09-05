import psycopg2

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="postgres",        # Replace with your database name
        user="postgres",            # Replace with your PostgreSQL username
        password="optimus",    # Replace with your PostgreSQL password
        host="localhost",           # PostgreSQL server address
        port="5432"                 # Default port for PostgreSQL
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")

    # Fetch and print the result
    db_version = cursor.fetchone()
    print(f"PostgreSQL database version: {db_version}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
