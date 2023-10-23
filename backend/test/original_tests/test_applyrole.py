# ----------------------------------------------------------------
# Author: 2023-10-03/ZL

# Description: Unit test to test the apply_role() API


# Last Modified: 2023-10-16/KM
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-03/ZL: Created unit tests for the apply_role() API
# - 2023-10-16/KM: Modified unit tests for the apply_role() API



import sys
import os
import requests
import pytest
import json
# Add the directory containing the `backend` to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")

def test_happy_path():
    payload = {
        "message" : {
            "Role_Listing_ID": 1,
            "Staff_ID": 140025,
            "brief_message": "I am a good fit for this role"
        
        }
    }
    response = requests.post(ENDPOINT+'/apply_role', json=payload)
    assert response.status_code == 201
    print(response.json())
    assert response.json()["role_listing_id"] == payload["message"]["Role_Listing_ID"]
    assert response.json()["staff_id"] == payload["message"]["Staff_ID"]
    assert response.json()["brief_message"] == payload["message"]["brief_message"]
    assert isinstance(response.json()["applied_at"], str)

def test_role_already_applied():
    payload = {
        "message" : {
            "Role_Listing_ID": 1,
            "Staff_ID": 150076   
        
        }
    }

    response = requests.post(ENDPOINT+'/apply_role', json=payload)  # First application
    response = requests.post(ENDPOINT+'/apply_role', json=payload)  # Second application

    assert response.status_code == 400
    assert response.json()["error"] == "Role already applied"
    assert 1==1

def test_missing_required_fields():
    payload = {
        "message" : {
            "Staff_ID": 140025
        }
       
    }
    response = requests.post(ENDPOINT+'/apply_role', json=payload)
    # Depending on how your application handles it, adjust the expected output
    assert response.status_code == 500
    assert "error" in response.json()

def test_invalid_role_or_staff_id():
    # Assuming you have validations in place for non-existent IDs
    payload = {
        "message" :{
            "Role_Listing_ID": 9999,  # Assuming this ID doesn't exist
            "Staff_ID": 4
        }

    }
    response = requests.post(ENDPOINT+'/apply_role', json=payload)
    assert response.status_code == 500  # or 404, based on your error handling
    assert "error" in response.json()

