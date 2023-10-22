# ----------------------------------------------------------------
# Author: 2023-10-03/RP

# Description: unit test for getAllRoles


# Last Modified: 2023-10-03/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-03/RP: Created unit tests for the getAllRoles API

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

def test_getAllRoles():
    response = requests.get(ENDPOINT+'/roles')
    assert response.status_code == 200
    assert response.json()[0]["message"] == "Successfully retrieved all roles"
    columns = [
        "Role_Desc",
        "Role_Name",
        "Skills"
    ]

    data = response.json()[0]['data']
    for obj in data:
        for key,values in obj.items():
            assert key in columns
           
 

