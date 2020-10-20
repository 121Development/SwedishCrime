# https://towardsdatascience.com/sql-on-the-cloud-with-python-c08a30807661
# https://cloud.google.com/sql/docs/mysql/connect-app-engine-standard

import mysql.connector
from mysql.connector import Error

# YOUR DB INFO #
host = "35.228.29.131"
user = "sc"
password = ""
database = "swedishCrime"



# SET BELOW ROUNDS VARIABLE TO 2 ROUNDS MORE THAN NUMBER OF LEVELS OF YOUR DB
# PARENT TABLE, CHILD, CHILD OF CHILD ETC.
rounds = 6

# def test():
#     return("Hej")

#Establish the connection and set cursor
try:
    conn = mysql.connector.connect(
        user=user, password=password, host=host, database=database)
    cursor = conn.cursor()
    print(f"\nSuccessfully connected to database {database}\n")
except Error as err:
    print(f"Error: '{err}'")

def get_all_table_names():
    sql = '''SHOW TABLES'''
    cursor.execute(sql)
    result = cursor.fetchall()
    table_names = [item for t in result for item in t] 
    return(table_names)



table_names = get_all_table_names()
¨


print(table_names)