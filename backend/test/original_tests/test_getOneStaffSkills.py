# ----------------------------------------------------------------
# Author: 2023-10-19/ZL

# Description: main flask app to receive backend API requests.


# Last Modified: 2023-10-19/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-19/ZL: Created unit tests for the getOneStaffSkills(staff_id) API

import requests
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.environ.get("DB")

class TestGetRoleListingAPI(unittest.TestCase):

    def test_get_one_staff_skills_happy_path(self):
        # Query a valid role listing:
        response = requests.get(ENDPOINT + "/staff_skills/140002")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["message"], "Successfully retrieved staff skills")

        data = response_data["data"]
        self.assertEqual(data[0]["Staff_ID"], 140002)
        expected_skills = ['Accounting and Tax Systems','Business Environment Analysis','Customer Relationship Management','Professional and Business Ethics']
        self.assertEqual(data[0]["Staff_Skills"], expected_skills)

        

    def test_get_one_staff_skills_invalid_id(self):
        # query an invalid staff id:
        response = requests.get(ENDPOINT + "/staff_skills/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Staff not found")

    def test_get_one_staff_skills_no_skills(self):
        # query a staff with not skills:
        response = requests.get(ENDPOINT + "/staff_skills/130001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Staff has no skills")


if __name__ == "__main__":
    unittest.main()

