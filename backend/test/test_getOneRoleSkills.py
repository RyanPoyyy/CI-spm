# ----------------------------------------------------------------
# Author: 2023-10-18/ZL

# Description: Unit testing for get_one_role_skills(role_name) API


# Last Modified: 2023-10-18/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-10-18/ZL: Created unit tests for the get_one_role_skills(role_name) API

import requests
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.environ.get("DB")

class TestGetRoleListingAPI(unittest.TestCase):

    def test_getOneRoleSkills_happy_path(self):
        # Query a valid role:
        response = requests.get(ENDPOINT + "/role_skills/Sales Manager")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["message"], "Successfully retrieved role skills")

        data = response_data["data"]
        expected_role_skills = [
            "Budgeting",
            "Business Negotiation",
            "Business Presentation Delivery",
            "Collaboration",
            "Communication",
            "Customer Acquisition Management",
            "Customer Relationship Management",
            "Problem Solving",
            "Sales Closure",
            "Stakeholder Management",
            "Strategy Planning",
            "Technology Integration"
        ]
        self.assertListEqual(data["role_skills"], expected_role_skills)
        

    def test_getOneRoleSkills_invalid_role(self):
        # query an invalid role:
        response = requests.get(ENDPOINT + "/role_skills/abc")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Role name not found")


if __name__ == "__main__":
    unittest.main()

