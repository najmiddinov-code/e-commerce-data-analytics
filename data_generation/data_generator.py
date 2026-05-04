import psycopg2
import time
import random
from faker import Faker
from insert_records import create_table

fake = Faker()

def connect_to_db():
    return psycopg2.connect(
        host='db',
        port='5432',
        dbname='db',
        user='db_user',
        password='db_password'
    )

def generate_dirty_data():
    conn = connect_to_db()
    create_table(conn)  
    conn.autocommit = True
    cursor = conn.cursor()

    print("Data Generator is started!")
    print("-" * 75)

    try:
        for _ in range(10):
            #===========================================
            # 1. Customers table
            #===========================================

            customer_name = fake.name()
            if random.random() < 0.2:
                customer_name = f"      {customer_name}"
            
            customer_email = fake.unique.email()

            if random.random() < 0.15:
                bad_emails = ['no_email', 'user.gmail.com', 'N/A', '@gs', '     ']
                customer_email = random.choice(bad_emails)
            
            customer_location = fake.city()

            if random.random() < 0.1:
                customer_location = customer_location + '123'

            cursor.execute("""
                INSERT INTO raw.customers (name, email, customer_location)
                VALUES (%s, %s, %s) RETURNING customer_id;
            """, (customer_name, customer_email, customer_location))
            customer_id = cursor.fetchone()[0]

            #===========================================
            # 2. Products table
            #===========================================

            adjectives = ['Wireless', 'Smart', 'Ergonomic', 'Portable', 'Gaming', 'Premium', 'Bluetooth', 'Compact', 'Heavy-Duty', 'Eco-friendly']
            
            category_mapping = {
                'Electronics': ['Headphones', 'Laptop', 'Smartphone', 'Mechanical Keyboard', 'Monitor', 'Mouse', 'Tablet', 'Smartwatch'],
                'Clothing': ['Cotton T-Shirt', 'Running Shoes', 'Winter Jacket', 'Denim Jeans', 'Backpack', 'Sneakers'],
                'Home': ['Coffee Maker', 'Air Purifier', 'Vacuum Cleaner', 'Desk Lamp', 'Blender', 'Sofa'],
                'Toys': ['Action Figure', 'Board Game', 'Lego Set', 'Puzzle', 'Remote Control Car'],
                'Books': ['Novel', 'Biography', 'Science Fiction Book', 'Cookbook', 'Data Engineering Guide']
            }

            base_category = random.choice(list(category_mapping.keys()))
            
            product_noun = random.choice(category_mapping[base_category])
            product_name = f"{random.choice(adjectives)} {product_noun}"
            
            product_category = base_category
            if random.random() < 0.15:
                product_category = random.choice(["UNKNOWN", "n/a", "", "                  Books                    "])
            
            price = round(random.uniform(5.0, 300.0), 2)

            if random.random() < 0.05:
                price = -price
            elif random.random() < 0.05:
                price = random.choice([99999.99, 5456546546, 123404425])
            
            cursor.execute("""
                INSERT INTO raw.products (name, product_category, price)
                VALUES (%s, %s, %s) RETURNING product_id;
            """, (product_name, product_category, price))
            product_id = cursor.fetchone()[0]

            #===========================================
            # 3. Orders table
            #===========================================

            quantity = random.randint(1, 10)
            if random.random() < 0.1:
                quantity = random.choice([-2, 0, -1])
            
            total_price = round(price * quantity, 2)
            if random.random() < 0.05:
                total_price = total_price + 500.0
                
            order_date = fake.date_time_between(start_date="-90d", end_date="now")

            cursor.execute("""
                INSERT INTO raw.orders (customer_id, product_id, quantity, total_price, order_date)
                VALUES (%s, %s, %s, %s, %s);
            """, (customer_id, product_id, quantity, total_price, order_date))

            status = "DIRTY DATA" if price < 0 or quantity <= 0 or "@" not in customer_email else "CLEAN"
            print(f"[{status}] Customer: '{customer_name}', Email: {customer_email}, Price: ${price}, Quantity: {quantity}, Total: ${total_price}")

            # time.sleep(random.randint(5, 7) * 60)

    except KeyboardInterrupt:
        print("\n Generator has stopped")
    except Exception as e:
        print(f"\n Recording error in database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_dirty_data()


            