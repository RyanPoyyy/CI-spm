# ----------------------------------------------------------------
# Author: 2023-10-11/RP

# Description: unit test for get all staffs


# Last Modified: 2023-10-11/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-11/RP: Created unit tests for the getAllStaffs API
# - 2023-10-12/RP: Modified endpoint



import requests
import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")

def test_getAllStaffs():
    response = requests.get(ENDPOINT + "/staffs") 
    status = response.status_code
    assert status == 200
    assert response.json()["message"] == "Successfully retrieved all staffs"

    list_of_keys = [
        "Staff_ID",
        "Staff_FName",
        "Staff_LName",
        "Department",
        "Country",
        "Email",
        "Access_Control_ID",
        "Access_Control_Name",
    ]
    data = response.json()['data']
    for obj in data:
        assert obj['Staff_ID'] != None
        assert obj['Staff_FName'] != None
        assert obj['Staff_LName'] != None
        assert obj['Department'] != None
        assert obj['Country'] != None
        assert obj['Email'] != None
        assert obj['Access_Control_ID'] != None
        assert obj['Access_Control_Name'] != None
        for key in obj.keys():
            assert key in list_of_keys



