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
import json
# Add the directory containing the `backend` to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Now you can import app and db from backend.app


import pytest

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
from models import Role, RoleSkill, Skill, db
import pytest


def test_getAllRoles(client):
    role1 = Role(
        role_name = "Software Engineer",
        role_desc = "Develop software"
    
    )

    role2 = Role(
        role_name = "Accountant",
        role_desc = "Manage accounts"
    )

    skill1 = Skill(
        Skill_Name = "Coding",
        Skill_Desc = "Code in Python"
    )

    skill2 = Skill(
        Skill_Name = "Accounting",
        Skill_Desc = "Calculate accounts"
    )

    roleskill1 = RoleSkill(
        Role_Name = "Software Engineer",
        Skill_Name = "Coding"
    )

    roleskill2 = RoleSkill(
        Role_Name = "Accountant",
        Skill_Name = "Accounting"
    )

    db.session.add(role1)
    db.session.add(role2)
    db.session.add(skill1)
    db.session.add(skill2)
    db.session.add(roleskill1)
    db.session.add(roleskill2)
    db.session.commit()
    
    response = client.get('/roles')
    assert response.status_code == 200

    message = response.get_json()[0]['message']
    assert message == "Successfully retrieved all roles"

    data = response.get_json()[0]['data']
    # returned data is in order of role_desc, role_name, role_skill
    returned_data = [
        {
            "Role_Desc": "Manage accounts",
            "Role_Name": "Accountant",
            "Skills": ['Accounting']
        },
        {
            "Role_Desc": "Develop software",
            "Role_Name": "Software Engineer",
            "Skills": ['Coding']
        }
    ]

    assert data == returned_data

