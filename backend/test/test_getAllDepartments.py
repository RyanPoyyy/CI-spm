# ----------------------------------------------------------------
# Author: 2023-10-03/RP

# Description: unit test for getAllDepartments


# Last Modified: 2023-10-03/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-03/RP: Created unit tests for the getAllDepartments API

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

def test_getAllDepartments():
    response = requests.get(ENDPOINT+'/departments')
    assert response.status_code == 200
    assert response.json()[0]["message"] == "Successfully retrieved all departments"
    assert response.json()[0]['data'] == ["Engineering",
      "Finance",
      "Human Resources",
      "IT",
      "Marketing",
      "R&D",
      "Sales"]
    # print(response.json()[0])
    # assert response.message == "Successfully retrieved all departments"
    # assert response.json()["data"] == ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "Legal"]
