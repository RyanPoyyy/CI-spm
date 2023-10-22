# ----------------------------------------------------------------
# Author: 2023-09-29/BT

# Description: main flask app to receive backend API requests.


# Last Modified: 2023-10-14/KM
# ----------------------------------------------------------------
# Modification history:
# - 2023-09-29/BT: Created unit tests for the get_one_role_listing(id) API
# - 2023-10-12/RP: Modified endpoint
# - 2023-10-14/KM: Modified unit tests to consistently validate created_at and updated_at fields

import requests
import unittest
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = os.environ.get("DB")

class TestGetRoleListingAPI(unittest.TestCase):

    def test_getOneRoleListing_happy_path(self):
        # Query a valid role listing:
        response = requests.get(ENDPOINT + "/role_listings/1")
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["message"], "Successfully retrieved role listing")

        data = response_data["data"]

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["department"], "Sales")
        self.assertEqual(data["role_name"], "Sales Manager")
        self.assertEqual(data["role_desc"], "The Sales Manager is responsible for managing the organisation's sales growth. By analysing client segmentation and competitor landscape, he/she develops sales strategies. He supports lead generation, and conducts business and contract negotiations to increase client acquisition and boost retention. Innovative and resourceful, he demonstrates initiative in identifying new opportunities both locally and regionally and converting them into actual sales. He builds good rapport with new and existing clients by pro-actively anticipating clients' needs and identifying business solutions to meet those needs. He networks extensively outside of the office to stay in close contact with the key industry stakeholders.")
        self.assertEqual(data["reporting_manager_id"], 140894)
        self.assertEqual(data["reporting_manager_name"], "Rahim Khalid")
        self.assertEqual(data["openings"], 2)
        self.assertEqual(data["country"], "Singapore")
        self.assertEqual(data["status"], 0)
        self.assertEqual(data["application_start"], "2023-10-01 00:00:00")
        self.assertEqual(data["application_deadline"], "2024-01-01 00:00:00")
        self.assertEqual(data["skills"], ["Budgeting", "Business Negotiation", "Business Presentation Delivery", "Collaboration", "Communication", "Customer Acquisition Management", "Customer Relationship Management", "Problem Solving", "Sales Closure", "Stakeholder Management", "Strategy Planning", "Technology Integration"])
        self.assertEqual(len(data["skills"]), 12)
        self.assertRegex(data["created_at"], r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        self.assertRegex(data["updated_at"], r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_get_one_role_listing_invalid_id(self):
        # query an invalid role_listing:
        response = requests.get(ENDPOINT + "/role_listings/abc")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Role listing not found")


if __name__ == "__main__":
    unittest.main()

