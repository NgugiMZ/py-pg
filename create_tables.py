import psycopg2

def create_tables():
    try:
        # Connect to your PostgreSQL DB
        conn = psycopg2.connect(
            dbname="postgres",        # Replace with your database name
            user="postgres",            # Replace with your PostgreSQL username
            password="optimus",    # Replace with your PostgreSQL password
            host="localhost",           # PostgreSQL server address
            port="5432"                 # Default port for PostgreSQL
        )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # SQL query to create a table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS employes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            position VARCHAR(100),
            salary DECIMAL
        );
        '''
        
        # Execute the query
        cursor.execute(create_table_query)
        
        # Commit changes
        conn.commit()
        print("Table created successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
