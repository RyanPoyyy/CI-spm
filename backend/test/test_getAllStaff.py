# ----------------------------------------------------------------
# Author: 2023-10-03/RP

# Description: unit test for getAllStaff


# Last Modified: 2023-10-03/RP
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-03/RP: Created unit tests for the getAllStaff API

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

def test_getAllStaff():
    response = requests.get(ENDPOINT+'/staff')
    assert response.status_code == 200
    assert response.json()[0]["message"] == "Successfully retrieved all staff"
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
    assert data == [
      {
        "Access_Control_ID": 1,
        "Country": "United States",
        "Department": "Human Resources",
        "Email": "john.doe@example.com",
        "Role": "Admin",
        "Staff_FName": "John",
        "Staff_ID": 1,
        "Staff_LName": "Doe",
        "created_at": "2023-10-03 03:29:41"
      },
      {
        "Access_Control_ID": 2,
        "Country": "Canada",
        "Department": "Marketing",
        "Email": "jane.smith@example.com",
        "Role": "Supervisor",
        "Staff_FName": "Jane",
        "Staff_ID": 2,
        "Staff_LName": "Smith",
        "created_at": "2023-10-03 03:29:41"
      },
      {
        "Access_Control_ID": 2,
        "Country": "United Kingdom",
        "Department": "Finance",
        "Email": "michael.johnson@example.com",
        "Role": "Supervisor",
        "Staff_FName": "Michael",
        "Staff_ID": 3,
        "Staff_LName": "Johnson",
        "created_at": "2023-10-03 03:29:41"
      },
      {
        "Access_Control_ID": 1,
        "Country": "Australia",
        "Department": "Engineering",
        "Email": "emily.williams@example.com",
        "Role": "Admin",
        "Staff_FName": "Emily",
        "Staff_ID": 4,
        "Staff_LName": "Williams",
        "created_at": "2023-10-03 03:29:41"
      },
      {
        "Access_Control_ID": 1,
        "Country": "Germany",
        "Department": "Sales",
        "Email": "daniel.brown@example.com",
        "Role": "Manager",
        "Staff_FName": "Daniel",
        "Staff_ID": 5,
        "Staff_LName": "Brown",
        "created_at": "2023-10-03 03:29:41"
      }]
 

