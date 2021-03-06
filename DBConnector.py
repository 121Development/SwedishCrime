# https://towardsdatascience.com/sql-on-the-cloud-with-python-c08a30807661
# https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard

import mysql.connector
from mysql.connector import Error

# # YOUR DB INFO #
# host = "35.228.29.131"
# user = "sc"
# password = "!"
# database = "swedishCrime"
#YOUR DB INFO #
host = "localhost"
user = "root"
password = ""
database = "swedishCrime"

def whichConnection(number):
    global conn, cursor
    if number == 1:
        conn = mysql.connector.connect(user="sc", password="PoliceP4rser!", host="35.228.29.131", database="swedishCrime")
        cursor = conn.cursor()
        print(f"\nSuccessfully connected to Google DB {database}\n")
    else:
        conn = mysql.connector.connect(user="root", password="", host="localhost", database="swedishCrime")
        cursor = conn.cursor()
        print(f"\nSuccessfully connected to local DB {database}\n")



#Establish the connection and set cursor
# try:
#     conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
#     cursor = conn.cursor()
#     print(f"\nSuccessfully connected to database {database}\n")
# except Error as err:
#     print(f"Error: '{err}'")
# try:
#     if fp.google == True:
#         conn = mysql.connector.connect(user="sc", password="PoliceP4rser!", host="35.228.29.131", database="swedishCrime")
#         print("database used Google Cloud")
#     else:
#         conn = mysql.connector.connect(user="root", password="", host="localhost", database="swedishCrime")
#         print("databaseUsed Local SQL")
#     cursor = conn.cursor()
#     print(f"\nSuccessfully connected to database {database}\n")
# except Error as err:
#     print(f"Error: '{err}'")

# Function to read passed query
def read_query(query):
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# Function to execute passed query
global commitedSum
commitedSum = 0
def execute_query(query):
    global commitedSum
    try:
        cursor.execute(query)
        conn.commit()
        commitedSum += 1
        #print("Commited data")
    except Error as err:
        print(f"Error: '{err}'")

global updatedSum
updatedSum = 0
def update_query(query):
    global updatedSum
    try:
        cursor.execute(query)
        conn.commit()
        updatedSum += 1
        #print("Updated data")
    except Error as err:
        print(f"Error: '{err}'")

def delete_data(query):
    try:
        cursor.execute(query)
        conn.commit()
    except Error as err:
        return("Error")
# Function to delete table data, takes variable rounds
def delete_table_data(rounds):
    n = 0
    while n < rounds:
        for name in table_names:
            delete_data(f"DELETE FROM {name};")
        n += 1
    print("Sucessfully deleted all table data\n")

def get_all_table_names():
    sql = '''SHOW TABLES'''
    cursor.execute(sql)
    result = cursor.fetchall()
    table_names = [item for t in result for item in t] 
    return(table_names)

def closeConnection():
    cursor.close()
    conn.close()

#table_names = get_all_table_names()
