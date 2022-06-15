# Imported libraries
import pandas as pd
import sqlite3


# Converting excel data to CSV format function - needed only after updating ItemList
def convert_to_csv(path):
    read_file = pd.read_excel(path)
    read_file.to_csv(r'Data/CSVItemList.csv', index=None, header=False)
    print("Excel file was converted to CSV file")


# Creating new Item Part database file function - 1 time run
def create_new_db():
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    cursor.execute("""create table PARTS (
                        SKU text, 
                        Part_Name text, 
                        Category text, 
                        Storing text, 
                        LOT integer
                        )""")
    print("New PART table has been created")
    connection.commit()
    connection.close()


# Creating new Warehouse Storing Spot database file function - 1 time run
def create_wss_db():
    connection = sqlite3.connect("WSS.db")
    cursor = connection.cursor()
    cursor.execute("""create table WSS (
                        Item_Name text, 
                        Quantity integer, 
                        Order_ID text, 
                        SKU text, 
                        LOT integer,
                        WSS text
                        )""")
    print("New WSS table has been created")
    connection.commit()
    connection.close()


# Filling the database with CSV data function
def fill_db():
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    with open('Data/CSVItemList.csv', 'r') as file:
        no_records = 0
        for row in file:
            cursor.execute("insert into PARTS values (?,?,?,?,?)", row.split(","))
            connection.commit()
            no_records += 1
    connection.close()
    print(f"\n {no_records} records have been uploaded into database.")


# Print the data from database function
def print_all_db():
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    for row in cursor.execute("select * from PARTS"):
        print(row)
    print("****************************************************************\n")
    connection.close()


# Select specific data category function
def select_db_cat(category):
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    cursor.execute("select * from PARTS where Category=:c", {"c": category})
    select_cat = cursor.fetchall()
    for row in select_cat:
        print(row)
    connection.close()
    print("****************************************************************\n")


# Manually create databases:
# convert_to_csv()
# create_new_db()
# fill_db()
# create_wss_db()

# TEST RUNNING AND PRINTING ALL + SEPARATE BY CATEGORY
# print_all_db()
# select_db_cat("ELECTRO")
# select_db_cat("METAL")
# select_db_cat("PLASTIC")
# select_db_cat("CH&G")
# select_db_cat("OFFICE")
# select_db_cat("OTHER")
