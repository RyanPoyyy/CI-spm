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
    
    def __init__(self, Access_ID, Access_Control_Name):
        self.Access_ID = Access_ID
        self.Access_Control_Name = Access_Control_Name
    
    def json(self):
        return {
                "Access_ID": self.Access_ID,
                "Access_Control_Name": self.Access_Control_Name,
                "created_at": self.created_at
        }


class Country(db.Model):
    __tablename__ = 'Country'

    Country_Name = Column(String(255), primary_key=True)

    def __init__(self,  Country_Name):
        self.Country_Name = Country_Name

    def json(self):
        return {
                "Country_Name": self.Country_Name
        }


class Department(db.Model):
    __tablename__ = 'Department'

    Department_Name = Column(String(50), primary_key=True)

    def __init__(self, Department_Name):
        self.Department_Name = Department_Name
    
    def json(self):
        return {
                "Department_Name": self.Department_Name
        }



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
    
    def __init__(self, Skill_Name, Skill_Desc):
        self.Skill_Name = Skill_Name
        self.Skill_Desc = Skill_Desc

    def json(self):
        return {
                "Skill_Name": self.Skill_Name,
                "Skill_Desc": self.Skill_Desc,
                "created_at": self.created_at
        }


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

    def __init__(self, Role_Name, Skill_Name):
        self.Role_Name = Role_Name
        self.Skill_Name = Skill_Name

    def json(self):
        return {
                "Role_Name": self.Role_Name,
                "Skill_Name": self.Skill_Name,
                "created_at": self.created_at
        }


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

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Department, Country, Email, Access_Control_ID):
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Department = Department
        self.Country = Country
        self.Email = Email
        self.Access_Control_ID = Access_Control_ID

    def json(self):
        return {
                "Staff_ID": self.Staff_ID,
                "Staff_FName": self.Staff_FName,
                "Staff_LName": self.Staff_LName,
                "Department": self.Department,
                "Country": self.Country,
                "Email": self.Email,
                "Access_Control_ID": self.Access_Control_ID,
                "created_at": self.created_at
        }



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

    def __init__(self, Role_Listing_ID, Role_Name, Openings, Status, Department, Country, Reporting_Manager_ID, application_start, application_deadline):
        self.Role_Listing_ID = Role_Listing_ID
        self.Role_Name = Role_Name
        self.Openings = Openings
        self.Status = Status
        self.Department = Department
        self.Country = Country
        self.Reporting_Manager_ID = Reporting_Manager_ID
        self.application_start = application_start
        self.application_deadline = application_deadline

    def json(self):
        return {
                "Role_Listing_ID": self.Role_Listing_ID,
                "Role_Name": self.Role_Name,
                "Openings": self.Openings,
                "Status": self.Status,
                "Department": self.Department,
                "Country": self.Country,
                "Reporting_Manager_ID": self.Reporting_Manager_ID,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "application_start": self.application_start,
                "application_deadline": self.application_deadline
        }


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

    def __init__(self, Staff_ID, Skill_Name):
        self.Staff_ID = Staff_ID
        self.Skill_Name = Skill_Name

    def json(self):
        return {
                "Staff_ID": self.Staff_ID,
                "Skill_Name": self.Skill_Name,
                "created_at": self.created_at
        }


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

    def __init__(self, Role_Listing_ID, Staff_ID, brief_description, applied_at, offer_given, offer_confirmed, offer_reviewed, offer_rejected):
        self.Role_Listing_ID = Role_Listing_ID
        self.Staff_ID = Staff_ID
        self.brief_description = brief_description
        self.applied_at = applied_at
        self.offer_given = offer_given
        self.offer_confirmed = offer_confirmed
        self.offer_reviewed = offer_reviewed
        self.offer_rejected = offer_rejected

    def json(self):
        return {
                "Role_Listing_ID": self.Role_Listing_ID,
                "Staff_ID": self.Staff_ID,
                "brief_description": self.brief_description,
                "applied_at": self.applied_at,
                "offer_given": self.offer_given,
                "offer_confirmed": self.offer_confirmed,
                "offer_reviewed": self.offer_reviewed,
                "offer_rejected": self.offer_rejected
        }
