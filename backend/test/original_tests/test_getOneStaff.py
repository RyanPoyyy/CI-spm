# ----------------------------------------------------------------
# Author: 2023-10-11/RP

# Description: unit test for get one staff


# Last Modified: 2023-10-12/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-11/RP: Created unit tests for the getOneStaff API
# - 2023-10-12/RP: Modified endpoint


import requests
import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")

def test_getOneStaff_happy_path():
    response = requests.get(ENDPOINT + "/staffs/130001") 
    status = response.status_code
    assert status == 200
    assert response.json()["message"] == "Successfully retrieved staff"
    dummy_data = {
            "Access_Control_ID": 1,
            "Access_Control_Name": "Admin",
            "Country": "Singapore",
            "Department": "Chariman",
            "Email": "jack.sim@allinone.com.sg",
            "Staff_FName": "John",
            "Staff_ID": 130001,
            "Staff_LName": "Sim"
        }

    list_of_keys = [
        "Staff_ID",
        "Staff_FName",
        "Staff_LName",
        "Department",
        "Country",
        "Email",
        "Access_Control_ID",
        "Access_Control_Name"
    ]
    obj = response.json()['data']
    assert obj['Staff_ID'] != None
    assert obj['Staff_FName'] != None
    assert obj['Staff_LName'] != None
    assert obj['Department'] != None
    assert obj['Country'] != None
    assert obj['Email'] != None
    assert obj['Access_Control_ID'] != None
    assert obj["Access_Control_Name"] != None
    for key in obj.keys():
        assert key in list_of_keys
    assert obj == dummy_data


# When Staff_ID is not in database
def test_getOneStaff_negative():
    response = requests.get(ENDPOINT + "/staffs/1") 
    status = response.status_code
    assert status == 404
    assert response.json()["error"] == "Staff not found"