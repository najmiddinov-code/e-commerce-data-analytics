import psycopg2


def connect_to_db():

    print(f"Connecting to the PostgreSQL database")
    try:
        conn = psycopg2.connect(
            host='db',
            port=5432,
            dbname='db',
            user='db_user',
            password='db_password'
        )

        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise


def create_table(conn):
    try:
        with conn.cursor() as cursor:
            print("Creating schema 'raw' if it doesn't exist")
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;
            """)

            print("Creating the 'raw.customers' table if it doesn't exist")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw.customers (
                    customer_id SERIAL PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    customer_location TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            print("Creating the 'raw.products' table if it doesn't exist")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw.products (
                    product_id SERIAL PRIMARY KEY,
                    name TEXT,
                    product_category TEXT,
                    price NUMERIC,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            print("Creating the 'raw.orders' table if it doesn't exist")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw.orders (
                    order_id SERIAL PRIMARY KEY,
                    customer_id INTEGER REFERENCES raw.customers(customer_id),
                    product_id INTEGER REFERENCES raw.products(product_id),
                    quantity INTEGER,
                    total_price NUMERIC,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                ALTER TABLE raw.orders
                ADD COLUMN IF NOT EXISTS order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)

        conn.commit()
        print("Tables created successfully")

    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise

def main():
    try:
        
        conn = connect_to_db()
        create_table(conn)
    
    except Exception as e:
        print(f"An error occured during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    main()