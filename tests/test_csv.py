from main import *
from utils.csv_processing import *
from utils.sector_processing import *
import pytest
import io
import csv
from werkzeug.datastructures import FileStorage

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_csv_process(client):
    csv_file = None

    with open(r'tests\test_files\test1.csv', 'r') as csv_file:
        #csv_file = FileStorage(fp)

        expected_results = [[5.53, -5.39, 3, 1, 1, '2020-09-23T09:17:16.310'], 
                            [5.53, -5.39, 29, 1, 3, '2018-09-20T13:07:46.125'], 
                            [5.53, -5.39, 30, 1, 3, '2021-08-21T04:35:18.433']]
        
        actual_results = process_csv(csv_file, 7)

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
        assert b'<div class="alert alert-danger">' not in response.data


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