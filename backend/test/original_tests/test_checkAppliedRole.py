# ----------------------------------------------------------------
# Author: 2023-10-16/KM

# Description: Unit test to test the check_applied_role() API


# Last Modified: 2023-10-16/KM
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-16/KM: Created unit tests for the check_applied_role() API



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


def test_get_not_applied():
    params = {
        "Role_Listing_ID": 1,
        "Staff_ID": 120001    
    }

    response = requests.get(ENDPOINT+'/check_apply_role', params=params)  # First application

    assert response.status_code == 200
    assert response.json()["status"] == "Role not applied"

def test_get_already_applied():
    params = {
        "Role_Listing_ID": 1,
        "Staff_ID": 150076    
    }

    response = requests.get(ENDPOINT+'/check_apply_role', params=params)  # Second application

    assert response.status_code == 400
    assert response.json()["status"] == "Role already applied"


