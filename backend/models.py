# ----------------------------------------------------------------
# Author: 2023-01-21/RP

# Description: file containing sqlalchemy models


# Last Modified: 2023-10-21/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-09-21/RP: Created sqlalchemy models
# - 2023-09-28/ZL: Added "offer_reviewed and offer_rejected to role_applied"
# - 2023-09-30/ZL: Added "brief message to role_applied"
# - 2023-10-11/ZX: Added country and department, and modified role_listing, staff, and role_applied
# - 2023-10-21/ZL: added brief_description to Role_Applied


# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()


class AccessControl(db.Model):
    __tablename__ = 'Access_Control'

    Access_ID = Column(Integer, primary_key=True)
    Access_Control_Name = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))


class Country(db.Model):
    __tablename__ = 'Country'

    Country_Name = Column(String(255), primary_key=True)


class Department(db.Model):
    __tablename__ = 'Department'

    Department_Name = Column(String(50), primary_key=True)


class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = Column(String(20), primary_key=True)
    Role_Desc = Column(LONGTEXT, nullable=False)
    def __init__(self,role_desc, role_name):
        self.Role_Desc = role_desc
        self.Role_Name = role_name

    def json(self):
        return {
                "Role_Name": self.Role_Name,
            "Role_Desc": self.Role_Desc,
                }



class Skill(db.Model):
    __tablename__ = 'Skill'

    Skill_Name = Column(String(50), primary_key=True)
    Skill_Desc = Column(LONGTEXT)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))


class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'

    Role_Name = Column(ForeignKey('Role.Role_Name'),
                       primary_key=True, nullable=False)
    Skill_Name = Column(ForeignKey('Skill.Skill_Name'),
                        primary_key=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    role = relationship('Role')
    skill = relationship('Skill')


class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = Column(Integer, primary_key=True)
    Staff_FName = Column(String(50), nullable=False)
    Staff_LName = Column(String(50), nullable=False)
    Department = Column(ForeignKey(
        'Department.Department_Name'), nullable=False, index=True)
    Country = Column(ForeignKey('Country.Country_Name'),
                     nullable=False, index=True)
    Email = Column(String(50), nullable=False)

    Access_Control_ID= Column(ForeignKey(
        'Access_Control.Access_ID'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    access_control = relationship('AccessControl')
    country = relationship('Country')
    department = relationship('Department')



class RoleListing(db.Model):
    __tablename__ = 'Role_Listing'
    __table_args__ = (
        Index('uniq_listing', 'Role_Name', 'Department',
              'Country', 'application_start', unique=True),
    )

    Role_Listing_ID = Column(Integer, primary_key=True)
    Role_Name = Column(ForeignKey('Role.Role_Name'))
    Openings = Column(Integer, nullable=False, server_default=text("'0'"))
    Status = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    Department = Column(ForeignKey(
        'Department.Department_Name'), nullable=False, index=True)
    Country = Column(ForeignKey('Country.Country_Name'),
                     nullable=False, index=True)
    Reporting_Manager_ID = Column(ForeignKey(
        'Staff.Staff_ID'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    application_start = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    application_deadline = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    country = relationship('Country')
    department = relationship('Department')
    staff = relationship('Staff')
    role = relationship('Role')


class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = Column(ForeignKey('Staff.Staff_ID'),
                      primary_key=True, nullable=False)
    Skill_Name = Column(ForeignKey('Skill.Skill_Name'),
                        primary_key=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    skill = relationship('Skill')
    staff = relationship('Staff')


class RoleApplied(db.Model):
    __tablename__ = 'Role_Applied'

    Role_Listing_ID = Column(ForeignKey(
        'Role_Listing.Role_Listing_ID'), primary_key=True, nullable=False)
    Staff_ID = Column(ForeignKey('Staff.Staff_ID'),
                      primary_key=True, nullable=False, index=True)
    brief_description = Column(LONGTEXT, nullable=True)
    applied_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    offer_given = Column(TINYINT(1), server_default=text("'0'"))
    offer_confirmed = Column(TINYINT(1), server_default=text("'0'"))
    offer_reviewed = Column(TINYINT(1), server_default=text("'0'"))
    offer_rejected = Column(TINYINT(1), server_default=text("'0'"))
    brief_description = Column(TEXT)
    role_listing = relationship('RoleListing')
    staff = relationship('Staff')
