# ----------------------------------------------------------------
# Author: 2023-10-18/ZL

# Description: Unit testing for get_one_role_skills(role_name) API


# Last Modified: 2023-10-18/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-18/ZL: Created unit tests for the get_role_applications_by_id(role_listing_id) API
# - 2023-10-21/ZL: Modified unit tests for the get_role_applications_by_id(role_listing_id) API
import requests
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.environ.get("DB")

class TestGetRoleListingAPI(unittest.TestCase):

    def test_getAllRoleApplications_happy_path(self):
        # Query a valid role:
        response = requests.get(ENDPOINT + "/hr/role_applications/1")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["message"], "Successfully retrieved role applications")

        data = response_data["data"]
        expected_staff_applications = [
            {   "brief_description":"No description",
                "country": "Singapore",
                "department": "Engineering",
                "email": "Oliver.Chan@allinone.com.sg",
                "name": "Oliver Chan",
                "offer_confirmed":0,
                "offer_given":0,
                "offer_rejected":0,
                "offer_reviewed":0,
                "skills": [
                    "Budgeting",
                    "Communication",
                    "Sense Making",
                    "System Integration"
                ],
                "staff_id": 150076,
                
            }
        ]
        self.assertEqual(data["staff_applications"], expected_staff_applications)

    def test_getAllRoleApplications_no_applications(self):
        # query a role listing with no applications:
        response = requests.get(ENDPOINT + "/hr/role_applications/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "No staff applied for this role")


if __name__ == "__main__":
    unittest.main()

