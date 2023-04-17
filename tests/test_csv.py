from main import *
from utils.csv_processing import *
from utils.sector_processing import *
import pytest
import io
import csv
from werkzeug.datastructures import FileStorage
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_csv_process(client):
    csv_file = None

    with open(r'tests\test_files\test1.csv', 'r') as csv_file:
        #csv_file = FileStorage(fp)

        expected_results = [[5.53, -5.39, 3, 1, 1, '2018-09-20T13:07:46.125'], 
                            [5.53, -5.39, 29, 1, 3, '2021-08-21T04:35:18.433'], 
                            [5.53, -5.39, 30, 1, 3, '2020-09-23T09:17:16.310']]
        
        actual_results = process_csv(csv_file, 7)

        print("EXPECTED RESULTS")
        print(expected_results)
        print("ACTUAL RESULTS")
        print(actual_results)

        assert expected_results == actual_results


def test_csv_upload(client):
    # replace with reading a csv file stored in testing data
    csv_file = None

    with open(r'tests\test_files\test1.csv', 'rb') as csv_file:
        # csv_file = FileStorage(fp)

        # Make a POST request to the csv_upload route with the temporary CSV file and a radius value
        response = client.post('/csv_upload', data={'csv_file': csv_file, 'radius': '5'})

        print(response)
        print(response.status_code)
        print(response.data)

        # Check if the response status code is 200 ()
        assert response.status_code == 200
        
        # Check if csv upload has an error
        assert b'<div id="error_message" class="alert alert-danger">' not in response.data


def test_download(client):
    req = client.get('/', query_string={"results": [
            [5.53, -5.39, 3, 1, 1, '2020-09-23T09:17:16.310'], 
            [5.53, -5.39, 30, 1, 3, '2018-09-20T13:07:46.125'], 
            [5.53, -5.39, 42, 2, 4, '2021-08-21T04:35:18.433']]
                                        })
    
    # ra, dec, sector_number, cycle, camera, obs_date

    test_response = download()
    assert test_response.status_code == 200
    assert test_response.data == b"RA,Dec,Sector,Camera,Cycle,Observation Date\r\n5.53,-5.39,3,1,1,'2020-09-23T09:17:16.310'\r\n,,30,1,3,'2018-09-20T13:07:46.125'\r\n,,42,2,4,'2021-08-21T04:35:18.433'\r\n"
    
def test_invalid_csv_upload(client):
    csv_file = None

    with open(r'C:\Users\sheim\OneDrive\Desktop\testingfinalprojecttpt\TPTtesting-master\tests\test_files\invalid_test.csv', 'rb') as csv_file:
        # Make a POST request to the csv_upload route with the temporary CSV file and a radius value
        response = client.post('/csv_upload', data={'csv_file': csv_file, 'radius': '0.01'})

        # Check if the response contains an error message
        assert b'<div id="error_message" class="alert alert-danger">' in response.data

def test_invalid_radius_value(client):
    csv_file = None

    with open(r'C:\Users\sheim\OneDrive\Desktop\testingfinalprojecttpt\TPTtesting-master\tests\test_files\test1.csv', 'rb') as csv_file:
        # Test with a non-numeric radius value
        response = client.post('/csv_upload', data={'csv_file': csv_file, 'radius': 'invalid_radius'})
        
        # Check if the response contains an error message
        assert b'<div id="error_message" class="alert alert-danger">' in response.data

def test_no_csv_file_upload(client):
    # Make a POST request to the csv_upload route without a CSV file and a radius value
    response = client.post('/csv_upload', data={'radius': '0.01'})

    # Print the response data for debugging purposes
    print(response.data)

    # Check if the response contains an error message
    assert b'<div id="error_message" class="alert alert-danger">' in response.data
    
   
# checks if error is thrown when entering only characters
def test_error1():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("sirius")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("def")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()


# checks if error is thrown when entering numbers and characters
def test_error2():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("101.2872 -16.7161")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("abc")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()


# checks if error is thrown when entering negative number for radius
def test_error3():
    driver = webdriver.Firefox("C:\\Users\\pmac3\\PycharmProjects\\Software Testing\\TPTtesting\\driver")
    driver.get("http://127.0.0.1:5000/")
    driver.maximize_window()

    element = driver.find_element(By.ID, "search_input")
    element.send_keys("101.2872 -16.7161")
    element = driver.find_element(By.ID, "radius")
    element.send_keys("-1")
    element = driver.find_element(By.ID, "search_btn")
    sleep(2)
    element.click()
    sleep(2)
    element_error = driver.find_elements(By.ID, "error_message")
    assert len(element_error) > 0
    driver.close()
