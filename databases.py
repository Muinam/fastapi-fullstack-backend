import sqlite3

conn = sqlite3.connect("products.db") # agar db h to connect or agar ni h to create kr dyti h

cursor = conn.cursor() # create a cursor object to execute sql commadns

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        status TEXT NOT NULL
    )
''')
# insert row in database
# cursor.execute('''
#     INSERT INTO products (name, price, stock, status)
#     VALUES ('keyboard', 50, 10, 'Available')
# ''')

# Read Data in database
cursor.execute("SELECT * FROM products")
all_row = cursor.fetchall() #fetch all the rows from the database
print("All rows:", all_row)

# Fetch specific colum
cursor.execute("SELECT name, status FROM products")
specific_row = cursor.fetchall()
print("Specific rows:", specific_row)

# where useing for filter condition
cursor.execute("SELECT * FROM products where id = 2")
filtered_row = cursor.fetchall()
print("Filtered rows:", filtered_row)

# update the rows
stock=input("Enter stock: ")
id=input("Enter id: ")

# ? sign ka use parameter placeholder SQL injection se bachne k liye use hota h 
# =, <, >,!=, LIKE, IN,BETWEEN in jase condition k lye use hota h 

cursor.execute('''
    UPDATE products SET stock=:stock WHERE id=:id 
''', {"stock":stock, "id":id})

# delete the rows
# cursor.execute("DELETE FROM products WHERE id = 3")

# Delete the table in database
# cursor.execute("DROP TABLE products")

conn.commit() # save the changes

conn.close() # close the connection

