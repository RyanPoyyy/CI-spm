# ----------------------------------------------------------------
# Author: 2023-10-03/RT

# Description: unit test for createRoleListing


# Last Modified: 2023-10-14/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-02/RT: Created unit tests for the createRoleListing API
# - 2023-10-03/RT: Attempted to resolve comments from senior development but having issues, have added comments
# - 2023-10-14/ZL: Modified data payloads in accordance to updated database

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")
'''
# Retrieve all Role Listings in the database
def test_getAllRoleListings():
    response = requests.get(ENDPOINT+'/countries')
    assert response.status_code == 200
    assert response.json()[0]["message"] == "Successfully retrieved all countries"
    
    columns = [
        "Role_Listing_ID",
       "Role_Name",
        "Openings",
        "Status",
        "Department",
        "Country",
        "Reporting_Manager_ID",
        "created_at",
        "updated_at",
        "application_Deadline"
    ]

    ## ========== Reg's comments ===========
    ## in app.py, theres role description,
    ## i don't know what to do about it

    data = response.json()[0]['data']
    assert data == [
      {
         "Role_Listing_ID": 1,
       "Role_Name": "Admin",
        "Openings": 2,
        "Status": 1,
        "Department": "IT",
        "Country": "United States",
        "Reporting_Manager_ID": 1,
        "created_at": "2023-10-03 06:39:42",
        "updated_at": "2023-10-03 06:39:42",
        "application_Deadline": "2023-10-01 00:00:00"
      },
      {
         "Role_Listing_ID": 2,
       "Role_Name": "Manager",
        "Openings": 1,
        "Status": 1,
        "Department": "R&D",
        "Country": "Spain",
        "Reporting_Manager_ID": 3,
        "created_at": "2023-10-03 06:39:42",
        "updated_at": "2023-10-03 06:39:42",
        "application_Deadline": "2023-09-30 00:00:00"
      },
      {
         "Role_Listing_ID": 3,
       "Role_Name": "Supervisor",
        "Openings": 2,
        "Status": 0,
        "Department": "Engineering",
        "Country": "Brazil",
        "Reporting_Manager_ID": 4,
        "created_at": "2023-10-03 06:39:42",
        "updated_at": "2023-10-03 06:39:42",
        "application_Deadline": "2023-10-02 00:00:00"
      }]
    ## ========== Ken's comments ===========
    ## i don't think need to test get all rolelistings because thats a diffent api,
    ## so im going to comment this out
'''

# Role listing not in database and is successfully created
def test_happy_path():
    payload = { 
        "roleName": "Account Manager",
        "openings": 2,
        "status": 0,
        "department": "IT",
        "country": "United States",
        "reportingManagerID": 130001,
        "applicationStartDate": "2023-10-20 00:00:00",
        "applicationDeadline": "2024-10-01 00:00:00"
    }

    ## ========== Reg's comments ===========
    ## in app.py, theres role description,
    ## will we have role description? help resolve thank you
    ## ========== Ken's comments ===========
    ## no need, role desc is only returned if the post request is valid,
    ## so there is no need to test for it 

    response = requests.post(ENDPOINT+'/role_listings', json=payload)
    #print(response.json())
    assert response.status_code == 201
    assert response.json()["role_name"] == payload["roleName"]

# Role listing has already been created
def test_role_listing_already_created():
    payload = {
        "roleName": "Sales Manager",
        "openings": 2,
        "status": 0,
        "department": "Sales",
        "country": "Singapore",
        "reportingManagerID": 140894,
        "applicationStartDate": "2023-10-01 00:00:00",
        "applicationDeadline": "2023-10-14 13:40:42"
    }
    response = requests.post(ENDPOINT+'/role_listings', json=payload)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["error"] == "Role listing already exists"

# Role listing creation has missing fields
def test_missing_required_fields():
    payload = {
        "roleName": "Sales Manager",
        "openings": 2,
    }
    response = requests.post(ENDPOINT+'/role_listings', json=payload)
    assert response.status_code == 500  

# Role listing creation has invalid data
def test_invalid_openings_data(): 
    payload = {
        "roleName": "Consultant",
        "openings": -3,
        "status": 1,
        "department": "IT",
        "country": "United States",
        "reportingManagerID": 1,
        "applicationStartDate": "2023-10-01 00:00:00",
        "applicationDeadline": "2023-10-01 00:00:00"
    }
    response = requests.post(ENDPOINT+'/role_listings', json=payload)
    assert response.status_code == 400  
    assert response.json()["error"] == "Invalid data"