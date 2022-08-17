# Author: Elliott Larsen
# Date:
# Description: This is a test file for http requests.

"""
Import requests module.
"""
import requests

def test_home():
    """
    Tests the http request from the home page.
    As of 8/13/2022, the status code 404 should be returned as there is no front end yet.
    """
    response = requests.get("http://127.0.0.1:8081")
    assert response.status_code == 404

def test_get_customer():
    """
    Tests http request for /customer.
    As of 8/13/2022, there is no customer in the database and
    the status code 204 should be returned.
    """
    response = requests.get("http://127.0.0.1:8081/customer")
    assert response.status_code == 204
