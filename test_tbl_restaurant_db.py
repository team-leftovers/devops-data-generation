# Author: Elliott Larsen
# Date:
# Description: This is a test file for the restaurant table.

#----------------------------------------------------------------------------------
#CREATE TABLE IF NOT EXISTS tbl_restaurant(
#    id INT AUTO_INCREMENT NOT NULL,
#    name VARCHAR(255) NOT NULL,
#    address_id INT NOT NULL,
#    phone_no VARCHAR(15) NOT NULL,
#    website VARCHAR(255),
#    open_time TIME NOT NULL,
#    close_time TIME NOT NULL,
#    rating DECIMAL,
#    rating_count INT,
#    PRIMARY KEY(id),
#    FOREIGN KEY (address_id) REFERENCES tbl_address(id)
#);
#----------------------------------------------------------------------------------

import mysql.connector
from faker import Faker
import random
import datetime
import decimal


def rand_restaurant(num):
    """
    This function takes an integer as parameter and generates restaurant information.
    """
    fake = Faker()
    return_lst = []

    for i in range(num):
        temp_lst = []
        temp_lst.append(fake.company())
        temp_lst.append(i + 1)
        temp_lst.append(fake.msisdn())
        temp_lst.append(fake.domain_name())
        temp_lst.append(fake.time())
        temp_lst.append(fake.time())
        temp_lst.append(round(random.uniform(0.00, 10.00), 1))
        temp_lst.append(random.randint(num * 1, num * 100))

        return_lst.append(temp_lst)

    return return_lst

def generate_address_db(num):
    """
    This function takes an integer as parameter, randomly generates addresses, and persists to the tlb_address database.
    """
    fake = Faker()
    address_lst = []

    for i in range(num):
        temp_lst = []
        temp_lst.append(fake.latlng()[0])
        temp_lst.append(fake.latlng()[1])
        temp_lst.append(fake.postcode())
        temp_lst.append(fake.current_country())
        temp_lst.append(fake.city())
        temp_lst.append(fake.address().split()[-2])
        temp_lst.append(fake.street_address())

        address_lst.append(tuple(temp_lst))
    
    cursor = connection.cursor()
    query = "INSERT INTO tbl_address(latitude, longitude, zip_code, country, city, state, street_address) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    for i in address_lst:
        cursor.execute(query, i)
        connection.commit()


num_restaurant = 5
generate_address_db(num_restaurant)
rand_restaurant_lst = rand_restaurant(num_restaurant)
# Create
def test_create_restaurants():
    """
    Create multiple restaurants using randomly generated data and test whether it persist to the database or not.
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    query = "INSERT INTO tbl_restaurant(name, address_id, phone_no, website, open_time, close_time, rating, rating_count) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    
    for i in rand_restaurant_lst:
        cursor.execute(query, i)
        connection.commit()
    
    query = "SELECT * FROM tbl_restaurant"
    cursor.execute(query)
    result = list(cursor.fetchall())

    assert len(result) == num_restaurant

# Read
def test_read_restaurant():
    """
    TODO
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    status = False
    cursor = connection.cursor()
    query = "SELECT * FROM tbl_restaurant"
    cursor.execute(query)
    result = list(cursor.fetchall())
    for i in range(len(result)):
        result[i] = list(result[i])
        del result[i][0]
        result[i] = result[i]
    
    for i in range(num_restaurant):
        for j in range(len(result[i])):
            if type(result[i][j]) == datetime.timedelta or type(result[i][j]) == decimal.Decimal:
                continue
            elif result[i][j] != rand_restaurant_lst[i][j]:
                status = False
            else:
                status = True

    assert status

# Update
def test_update_restaurant():
    """
    TODO
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    new_res_lst = rand_restaurant(num_restaurant)
    cursor = connection.cursor()
    
    for i in range(len(new_res_lst)):
        query = f"UPDATE tbl_restaurant SET name = '{new_res_lst[i][0]}', address_id = '{new_res_lst[i][1]}', phone_no = '{new_res_lst[i][2]}', website = '{new_res_lst[i][3]}' WHERE id = {i + 1}"
        cursor.execute(query)
        connection.commit()
    
    query = "SELECT * FROM tbl_restaurant"
    cursor.execute(query)
    result = list(cursor.fetchall())
    for i in range(len(result)):
        result[i] = list(result[i])
        del result[i][0]
        result[i] = tuple(result[i])

    status = False
    for i in range(num_restaurant):
        for j in range(4):
            if result[i][j] == new_res_lst[i][j]:
                status = True
            else:
                status = False

    return status

# Delete
def test_delete_restaurant():
    """
    TODO
    DELETE USER AND PASSWORD BEFORE EXITING.
    """
    #connection = mysql.connector.connect(host='localhost', database='leftovers', user='USERNAME', password='PASSWORD')
    cursor = connection.cursor()
    for i in range(1000):
        query = f"DELETE FROM tbl_restaurant WHERE id = {i + 1}"
        cursor.execute(query)
        connection.commit()

    query = "ALTER TABLE tbl_restaurant AUTO_INCREMENT = 1"
    cursor.execute(query)
    connection.commit()

    cursor = connection.cursor()
    for i in range(1000):
        query = f"DELETE FROM tbl_address WHERE id = {i + 1}"
        cursor.execute(query)
        connection.commit()

    query = "ALTER TABLE tbl_address AUTO_INCREMENT = 1"
    cursor.execute(query)
    connection.commit()

    query = "SELECT * FROM tbl_restaurant"
    cursor.execute(query)
    res_delete_result = list(cursor.fetchall())

    query = "SELECT * FROM tbl_address"
    cursor.execute(query)
    address_delete_result = list(cursor.fetchall())

    assert len(res_delete_result) == 0 and len(address_delete_result) == 0