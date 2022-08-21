# Author: Elliott Larsen
# Date:
# Description: This is a test file for the account table.

#----------------------------------------------------------------------------------
#CREATE TABLE IF NOT EXISTS tbl_account(
#    id INT AUTO_INCREMENT NOT NULL,
#    first_name VARCHAR(255), /* These two are nullible for admin accounts */
#    last_name VARCHAR(255),
#    email VARCHAR(255) NOT NULL,
#    phone_no VARCHAR(15 /* Max Phone Number Length */),
#    password VARCHAR(255) NOT NULL,
#    type ENUM('R', 'D', 'C', 'S') NOT NULL, /* R: Restaurant Admin, D: Driver, C: Customer, S: Site Admin */
#    PRIMARY KEY (id)
#);
#----------------------------------------------------------------------------------

import mysql.connector
from faker import Faker

def rand_user_data(num_user):
    """
    This function takes an integer as parameter and creates randomly generated user data.  The function returns a list of
    first name list, last name list, email list, and phone number list.
    """
    fake = Faker()
    return_lst = []

    for i in range(num_user):
        temp_lst = []
        name_lst = fake.name().split()
        if len(name_lst) > 2:
            temp_lst.append(name_lst[-2])
            temp_lst.append(name_lst[-1])
        else:
            temp_lst.append(name_lst[0])
            temp_lst.append(name_lst[1])
        temp_lst.append(fake.email())
        temp_lst.append(fake.msisdn())
        temp_lst.append("1234")
        temp_lst.append("C")
        
        return_lst.append(tuple(temp_lst))

    return return_lst

def test_db_connection():
    """
    Tests the SQL Database connection.  
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    assert connection.is_connected() == True

def test_getting_all_tables():
    """
    Tests if all tables can be called.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "SHOW TABLES"
    cursor.execute(query)
    table_list = []
    for tab in cursor:
        table_list.append(tab)
    assert len(table_list) == 16

# CRUD with one account.
# Create
def test_create_one_user():
    """
    Creates one user and test the database.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "INSERT INTO tbl_account(first_name, last_name, email, phone_no, password, type) VALUES(%s, %s, %s, %s, %s, %s)"
    sample = ("FName", "LName", "123@123.com", "1234567890", "1234", "D")
    cursor.execute(query, sample)
    connection.commit()
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert len(result) == 1
    # Database must be rest to its original state after the test.

# Read
def test_read_one_user():
    """
    Read the account information created above.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert result == [(1, "FName", "LName", "123@123.com", "1234567890", "1234", "D")]

# Update
def test_update_one_user():
    """
    Update the account created above.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "UPDATE tbl_account SET first_name = 'updated_FName', last_name = 'updated_LName', email = 'updated@email.com', phone_no = '1111111111' WHERE id = 1"
    cursor.execute(query)
    connection.commit()
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert result == [(1, "updated_FName", "updated_LName", "updated@email.com", "1111111111", "1234", "D")]

# Delete
def test_delete_one_user():
    """
    Delete the user creaged above.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "DELETE FROM tbl_account WHERE first_name = 'updated_FName' AND last_name = 'updated_LName' AND id = 1"
    cursor.execute(query)
    connection.commit()

    query = "ALTER TABLE tbl_account AUTO_INCREMENT = 1"
    cursor.execute(query)
    connection.commit()

    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert len(result) == 0

# CRUD with multiple accounts
# Create

num_user = 5
rand_user_lst = rand_user_data(num_user)

def test_create_multiple_users():
    """
    Create multiple users using randomly generated data and test whether it persist to the database or not.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "INSERT INTO tbl_account(first_name, last_name, email, phone_no, password, type) VALUES(%s, %s, %s, %s, %s, %s)"
    
    for i in rand_user_lst:
        cursor.execute(query, i)
        connection.commit()
    
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert len(result) == num_user

# Read
def test_read_multiple_users():
    """
    Read account information created above.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    for i in range(len(result)):
        result[i] = list(result[i])
        del result[i][0]
        result[i] = tuple(result[i])

    assert result == rand_user_lst

# Update
def test_update_multiple_users():
    """
    Update the accounts created above.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    new_rand_lst = rand_user_data(num_user)
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()

    for i in range(len(new_rand_lst)):
        query = f"UPDATE tbl_account SET first_name = '{new_rand_lst[i][0]}', last_name = '{new_rand_lst[i][1]}', email = '{new_rand_lst[i][2]}', phone_no = '{new_rand_lst[i][3]}' WHERE id = {i + 1}"
        cursor.execute(query)
        connection.commit()
    
    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())
    for i in range(len(result)):
        result[i] = list(result[i])
        del result[i][0]
        result[i] = tuple(result[i])

    assert result == new_rand_lst

# Delete
def test_delete_multiple_users():
    """
    Delete the users.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    for i in range(num_user):
        query = f"DELETE FROM tbl_account WHERE id = {i + 1}"
        cursor.execute(query)
        connection.commit()

    query = "ALTER TABLE tbl_account AUTO_INCREMENT = 1"
    cursor.execute(query)
    connection.commit()

    query = "SELECT * FROM tbl_account"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert len(result) == 0

