# ----------------------------------------------------------------
# Author: 2023-10-03/RP

# Description: unit test for getAllManagers


# Last Modified: 2023-10-03/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-03/RP: Created unit tests for the getAllManagers API

import sys
import os
import requests
# Add the directory containing the `backend` to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Now you can import app and db from backend.app


import pytest

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

ENDPOINT = os.environ.get("DB")

import pytest

def test_getAllManagers():
    response = requests.get(ENDPOINT+'/staff/managers')
    assert response.status_code == 200
    assert response.json()[0]["message"] == "Successfully retrieved all managers"
    columns = [
       "Access_Control_ID",
        "Country",
        "Department",
        "Email",
        "Role",
        "Staff_FName",
        "Staff_ID",
        "Staff_LName",
        "created_at"
    ]

    data = response.json()[0]['data']
    for obj in data:
        for key,values in obj.items():
            assert key in columns
            if key == "Role":
                assert values == "Manager"
 

