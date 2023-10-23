# ----------------------------------------------------------------
# Author: 2023-09-27/RP

# Description: main flask app to receive backend API requests.


# Last Modified: 2023-10-16/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-09-27/RP: Created unit tests for the get_all_role_listings_as_staff() API
# - 2023-10-12/RP: Modified endpoint
# - 2023-10-14/RP: Modified unit test
# - 2023-10-16/RP: Added application_start to unit test


import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")



# response = requests.get(ENDPOINT+ "/role_listings")

# status = response.status_code
# # data = response.json()
# # print(response.)
# print(response.headers)
# print(response.reason)
# print(status)

def test_getAllRoleListingsStaff():
    response = requests.get(ENDPOINT + "/rolelistings/staff") 
    print(response.status_code)
    print(response.headers)
    print(response.reason)
    # print(response.json())
    status = response.status_code
    assert status == 200
    assert response.json()[0]["message"] == "Successfully retrieved all role listings"
    

    list_of_keys = ["id", "role_name", "role_desc", "openings", "status",
                    "department", "country", "reporting_manager_id", "created_at",
                    "updated_at", "application_deadline", "skills", "application_start"]
    data = response.json()[0]['data']
    for obj in data:
        assert obj['id'] != None
        assert obj['role_name'] != None
        assert obj['role_desc'] != None
        assert obj['openings'] != None
        assert obj['status'] != None
        assert obj['department'] != None
        assert obj['country'] != None
        assert obj['reporting_manager_id'] != None
        assert obj['created_at'] != None
        assert obj['updated_at'] != None
        assert obj['application_deadline'] != None
        assert obj['application_deadline'] > str(datetime.utcnow())
        assert obj['skills'] != None
        assert obj['status'] == 0
        assert obj['application_start'] != None
        assert obj['application_start'] < str(datetime.utcnow())
        for keys in obj.keys():
            assert keys in list_of_keys
    print(data)
    
