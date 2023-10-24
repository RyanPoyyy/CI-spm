# ----------------------------------------------------------------
# Author: 2023-09-20/RP

# Description: main flask app to receive backend API requests.


# Last Modified: 2023-10-21/ZL
# ----------------------------------------------------------------
# Modification history:
# - 2023-09-20/RP: Created main flask App.
# - 2023-09-22/ZX: Created create role_listing endpoint.
# - 2023-09-23/ZL: Created GET method /rolelisting.
# - 2023-09-29/BT: Created GET method /role_listings/<string:id>. 
# - 2023-09-30/KM: Modified GET method /role_listings/<string:id> to include reporting manager name.
# - 2023-10-02/ZL: Added check_apply_role API.
# - 2023-10-03/ZX: Added API to getAllDepartments, getAllCountries, getAllStaff, getAllManagers, getAllRoles
# - 2023-10-03/ZL: Modified apply_role API. 
# - 2023-10-11/RP: Created Get method /staffs to get all staffs
# - 2023-10-11/RP: Created Get method /staffs/<string:staff_id> to get one staff
# - 2023-10-14/RP: Fixed bug in getAllRoleListingsAsStaff method
# - 2023-10-14/KM: Modified GET method /role_listings/<string:id> to include application_start.
# - 2023-10-14/ZL: Removed "Role" from getAllManagers,getAllStaff
# - 2023-10-16/KM: Modified POST method /apply_role to apply for a role
# - 2023-10-16/RP: Modified GET method for getAllRoleListingsStaff to include application_start.
# - 2023-10-18/ZL: Created GET method /hr/role_applications/<string:role_listing_id> to get all role applications by role listing ID as hr
# - 2023-10-18/ZL: Created GET method /role_skills/<string:role_name> to get all role skills by role name
# - 2023-10-19/ZL: Created Get method /staff_skills/<string:staff_id> to get all staff skills
# - 2023-10-19/RP: Fixed app bugs
# - 2023-10-20/ZL: Modified GET method /hr/role_applications/<string:role_listing_id> to include offer_given, offer_confirmed, offer_reviewed, offer_rejected, staff_id
# - 2023-10-21/ZL: Modified GET method /hr/role_applications/<string:role_listing_id> to include code for handling in frontend

from models import db
from models import AccessControl, Role, Skill, Staff, RoleListing, StaffSkill, RoleSkill, RoleApplied, Department, Country
from flask import Flask, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func, cast, Date
from sqlalchemy.orm import joinedload
from datetime import datetime

import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()




app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DB_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TEST_DB_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def initialize_db(app):
    with app.app_context():
        db.create_all()

def teardown(app):
    with app.app_context():
        db.drop_all()


@app.route('/')
def hello_world():
    return 'Hello, World!'


    
# NOT IN USE
# @app.route('/staff', methods=["GET"])
# def get_all_staff():
#     try:
#         allStaff = db.session.query(Staff).all()

#         response = {
#             "data":[
#                 {
#                     "Staff_ID": staff.Staff_ID,
#                     "Staff_FName": staff.Staff_FName,
#                     "Staff_LName": staff.Staff_LName,
#                     "Department": staff.Department,
#                     "Country": staff.Country,
#                     "Email": staff.Email,
#                     "Access_Control_ID": staff.Access_Control_ID,
#                     "created_at": staff.created_at.strftime('%Y-%m-%d %H:%M:%S')
#                 }
#             for staff in allStaff],
#             "message": "Successfully retrieved all staff"
#         }
#         return jsonify(response, 200)
    
#     except Exception as e:
#         return jsonify({"error": "Error fetching staff: " + str(e)}), 500
    



@app.route('/departments', methods=["GET"])
def get_all_departments():
    try:
        departments = db.session.query(Department).all()

        response = {
            "data":[department.Department_Name for department in departments],
            "message": "Successfully retrieved all departments"
        }
        return jsonify(response, 200)
    
    except Exception as e:
        return jsonify({"error": "Error fetching departments: " + str(e)}), 500
    

@app.route('/countries', methods=["GET"])
def get_all_countries():
    try:
        countries = db.session.query(Country).all()

        response = {
            "data":[country.Country_Name for country in countries],
            "message": "Successfully retrieved all countries"
        }
        return jsonify(response, 200)
    
    except Exception as e:
        return jsonify({"error": "Error fetching countries: " + str(e)}), 500
    
    

@app.route('/staff/managers', methods=["GET"])
def get_all_managers():
    try:
        managers = db.session.query(Staff).filter(Staff.Access_Control_ID == "3").all()

        response = {
            "data":[
                {
                    "Staff_ID": manager.Staff_ID,
                    "Staff_FName": manager.Staff_FName,
                    "Staff_LName": manager.Staff_LName,
                    "Department": manager.Department,
                    "Country": manager.Country,
                    "Email": manager.Email,
                    "Access_Control_ID": manager.Access_Control_ID,
                    "created_at": manager.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            for manager in managers],
            "message": "Successfully retrieved all managers"
        }
        return jsonify(response, 200)
    
    except Exception as e:
        return jsonify({"error": "Error fetching managers: " + str(e)}), 500


@app.route('/roles', methods=["GET"])
def get_all_roles():
    try:
        roles = db.session.query(
            Role.Role_Name,
            Role.Role_Desc,
            func.group_concat(Skill.Skill_Name).label("Skills")
        ).join(
            RoleSkill, Role.Role_Name == RoleSkill.Role_Name
        ).join(
            Skill, RoleSkill.Skill_Name == Skill.Skill_Name
        ).group_by(
            Role.Role_Name, Role.Role_Desc
        ).all()

        for role in roles:
            print(role[2].split(","))

        response = {
            "data":[
                {
                    "Role_Name": role[0],
                    "Role_Desc": role[1],
                    "Skills": role[2].split(",")
                }
            for role in roles],
            "message": "Successfully retrieved all roles"
        }
        return jsonify(response, 200)
    
    except Exception as e:
        return jsonify({"error": "Error fetching roles: " + str(e)}), 500


@app.route('/rolelistings/staff', methods=["GET"])
def get_all_role_listings_as_staff():
    try:
        role_listing_data = (
                db.session.query(RoleListing, Role.Role_Desc, func.group_concat(RoleSkill.Skill_Name).label("Skill_Names"))
                .join(Role, RoleListing.Role_Name == Role.Role_Name)
                .join(RoleSkill, Role.Role_Name == RoleSkill.Role_Name)
                .filter(RoleListing.application_deadline > datetime.utcnow())
                .filter(RoleListing.application_start < datetime.utcnow())
                .filter(RoleListing.Status == 0)
                .group_by(
                    RoleListing.Role_Listing_ID,
                    RoleListing.Role_Name,
                    RoleListing.Openings,
                    RoleListing.Status,
                    RoleListing.Department,
                    RoleListing.Country,
                    RoleListing.Reporting_Manager_ID,
                    RoleListing.created_at,
                    RoleListing.updated_at,
                    RoleListing.application_deadline,
                    Role.Role_Desc
                )
                .all()
        )

        response = {
            "data":[
            {
                "id": result[0].Role_Listing_ID,
                "role_name": result[0].Role_Name,
                "role_desc": result[1],
                "openings": result[0].Openings,
                "status": result[0].Status,
                "department": result[0].Department,
                "country": result[0].Country,
                "reporting_manager_id": result[0].Reporting_Manager_ID,
                "created_at": result[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": result[0].updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                "application_deadline": result[0].application_deadline.strftime('%Y-%m-%d %H:%M:%S'),
                "application_start": result[0].application_start.strftime('%Y-%m-%d %H:%M:%S'),
                "skills": result[2].split(',') if result[2] else []
            }
            for result in role_listing_data
        ]
        ,
        "message": "Successfully retrieved all role listings",
        }
        print(role_listing_data)



        return jsonify(response, 200)
    except Exception as e:
        return jsonify({"error": "Error fetching role listings: "+str(e)}), 500
    finally:
        db.session.close()


@app.route("/role_listings/<string:id>", methods=["GET"])
def get_one_role_listing(id):
    role_listing_data = (
            db.session.query(RoleListing, Role.Role_Desc, func.group_concat(RoleSkill.Skill_Name).label("Skill_Names"), Staff.Staff_FName, Staff.Staff_LName)
            .join(Role, RoleListing.Role_Name == Role.Role_Name)
            .join(RoleSkill, Role.Role_Name == RoleSkill.Role_Name)
            .join(Staff, RoleListing.Reporting_Manager_ID == Staff.Staff_ID)
            .filter(RoleListing.Role_Listing_ID == id)
            .group_by(
                RoleListing.Role_Listing_ID,
                RoleListing.Role_Name,
                RoleListing.Openings,
                RoleListing.Status,
                RoleListing.Department,
                RoleListing.Country,
                RoleListing.Reporting_Manager_ID,
                RoleListing.created_at,
                RoleListing.updated_at,
                RoleListing.application_start,
                RoleListing.application_deadline,
                Role.Role_Desc,
                Staff.Staff_FName,
                Staff.Staff_LName
            )
            .first()
        )
    if role_listing_data:
        response = {
            "data":
            {
                "id": role_listing_data[0].Role_Listing_ID,
                "role_name": role_listing_data[0].Role_Name,
                "role_desc": role_listing_data[1],
                "openings": role_listing_data[0].Openings,
                "status": role_listing_data[0].Status,
                "department": role_listing_data[0].Department,
                "country": role_listing_data[0].Country,
                "reporting_manager_id": role_listing_data[0].Reporting_Manager_ID,
                "reporting_manager_name": role_listing_data[3] + " " + role_listing_data[4],
                "created_at": role_listing_data[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": role_listing_data[0].updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                "application_start": role_listing_data[0].application_start.strftime('%Y-%m-%d %H:%M:%S'),
                "application_deadline": role_listing_data[0].application_deadline.strftime('%Y-%m-%d %H:%M:%S'),
                "skills": role_listing_data[2].split(',') if role_listing_data[2] else []
            }
            ,
            "message": "Successfully retrieved role listing"
        }
        return jsonify(response), 200
    
    else:
        return jsonify({"message": "Role listing not found"}), 404

@app.route("/role_listings", methods=["GET", "POST"])
def role_listings():
    if request.method == "POST":
        request_body = request.json
        new_role_listing = RoleListing(
            Role_Name = request_body["roleName"],
            Openings = request_body["openings"],
            Status = request_body["status"],
            Department = request_body["department"],
            Country = request_body["country"],
            Reporting_Manager_ID = request_body["reportingManagerID"],
            application_start = request_body["applicationStartDate"],
            application_deadline = request_body["applicationDeadline"]
        )
    

        role = db.session.query(Role).filter(Role.Role_Name == request_body["roleName"]).all()
        
        role_skills = db.session.query(RoleSkill).filter(RoleSkill.Role_Name == request_body["roleName"]).all()
        
        countries = db.session.query(Country).all()
        countries = [country.Country_Name for country in countries]
        try:
            if(RoleListing.query.filter(RoleListing.Role_Name == request_body["roleName"],
                                        RoleListing.Country == request_body["country"],
                                        RoleListing.Department == request_body["department"],
                                        RoleListing.application_start == request_body["applicationStartDate"]).first()):
                return jsonify({"error": "Role listing already exists"}), 400
            if (new_role_listing.Openings < 0 or 
                new_role_listing.Status < 0 or 
                new_role_listing.Status > 1 or 
                new_role_listing.application_deadline < str(datetime.now()) or
                new_role_listing.application_start < str(datetime.now()) or 
                new_role_listing.Country not in countries or
                role == [] or
                role_skills == []):
                return jsonify({"error": "Invalid data"}), 400
            db.session.add(new_role_listing)
            db.session.commit()
            return jsonify({
                    "id": new_role_listing.Role_Listing_ID,
                    "role_name": new_role_listing.Role_Name,
                    "role_desc": role[0].Role_Desc,
                    "openings": new_role_listing.Openings,
                    "status": new_role_listing.Status,
                    "department": new_role_listing.Department,
                    "country": new_role_listing.Country,
                    "reporting_manager_id": new_role_listing.Reporting_Manager_ID,
                    "created_at": new_role_listing.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": new_role_listing.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "application_deadline": new_role_listing.application_deadline.strftime('%Y-%m-%d %H:%M:%S'),
                    "skills": [role_skill.Skill_Name for role_skill in role_skills]
                }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error inserting role listings: " + str(e)}), 500
        
    else:
        try:
            role_listing_data = (
                db.session.query(RoleListing, Role.Role_Desc, func.group_concat(RoleSkill.Skill_Name).label("Skill_Names"))
                .join(Role, RoleListing.Role_Name == Role.Role_Name)
                .join(RoleSkill, Role.Role_Name == RoleSkill.Role_Name)
                .group_by(
                    RoleListing.Role_Listing_ID,
                    RoleListing.Role_Name,
                    RoleListing.Openings,
                    RoleListing.Status,
                    RoleListing.Department,
                    RoleListing.Country,
                    RoleListing.Reporting_Manager_ID,
                    RoleListing.created_at,
                    RoleListing.updated_at,
                    RoleListing.application_deadline,
                    Role.Role_Desc
                    ## ========== Reg's comments ===========
                    ## database don't have role description why is it here,
                    ## even when adding role listing test doesn't have desc
                )
                .all()
            )
            response = { "data":[
                    {
                        "id": result[0].Role_Listing_ID,
                        "role_name": result[0].Role_Name,
                        "role_desc": result[1],
                        "openings": result[0].Openings,
                        "status": result[0].Status,
                        "department": result[0].Department,
                        "country": result[0].Country,
                        "reporting_manager_id": result[0].Reporting_Manager_ID,
                        "created_at": result[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        "updated_at": result[0].updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                        "application_deadline": result[0].application_deadline.strftime('%Y-%m-%d %H:%M:%S'),
                        "skills": result[2].split(',') if result[2] else []
                    }
                    for result in role_listing_data
                ],
                "message": "Successfully retrieved all role listings"
                }
            return jsonify(response,200)
        except Exception as e:
            return jsonify({"error": "Error fetching role listings: " + str(e)}), 500
        finally:
            db.session.close()        
# get all staffs:
@app.route("/staffs", methods=['GET'])
def getAllStaffs():
    try:
        staff_data = db.session.query(Staff, AccessControl.Access_Control_Name) \
        .join(AccessControl, Staff.Access_Control_ID == AccessControl.Access_ID).all()
        response = {
            "data":[
                {
                    "Staff_ID":result[0].Staff_ID,
                    "Staff_FName":result[0].Staff_FName,
                    "Staff_LName":result[0].Staff_LName,
                    "Department":result[0].Department,
                    "Country":result[0].Country,
                    "Email":result[0].Email,
                    "Access_Control_ID":result[0].Access_Control_ID,
                    "Access_Control_Name": result[1]
                }
                for result in staff_data
            ],
            "message": "Successfully retrieved all staffs"
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error":"Error fetching staffs " + str(e)}),500
    finally:
        db.session.close()

#get one staff by ID:
@app.route("/staffs/<string:staff_id>", methods=['GET'])
def getOneStaff(staff_id):
    try:
        staff= db.session.query(Staff, AccessControl.Access_Control_Name) \
            .join(AccessControl, Staff.Access_Control_ID == AccessControl.Access_ID) \
            .filter(Staff.Staff_ID == staff_id) \
            .first()
        
        if not staff:
            return jsonify({"error": "Staff not found",}), 404
        response = {
            "data": {
                "Staff_ID": staff[0].Staff_ID,
                "Staff_FName": staff[0].Staff_FName,
                "Staff_LName": staff[0].Staff_LName,
                "Department": staff[0].Department,
                "Country": staff[0].Country,
                "Email": staff[0].Email,
                "Access_Control_ID": staff[0].Access_Control_ID,
                "Access_Control_Name": staff[1]
            },
            "message": "Successfully retrieved staff"
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Error fetching staff: " + str(e)}), 500
    finally:
        db.session.close()

#get one staff skills by ID:
@app.route("/staff_skills/<string:staff_id>", methods=['GET'])
def getOneStaffSkills(staff_id):
    try:
        staff = db.session.query(Staff).filter(Staff.Staff_ID == staff_id).first()
        if not staff:
            return jsonify({"error": "Staff not found",
                            "code":404}), 404
        
        staff_skills = db.session.query(StaffSkill, Skill.Skill_Name) \
            .join(Skill, StaffSkill.Skill_Name == Skill.Skill_Name) \
            .filter(StaffSkill.Staff_ID == staff_id) \
            .all()
        
        if not staff_skills:
            return jsonify({"message": "Staff has no skills",
                            "code":200}), 200
        staff_skills_list =[]
        for result in staff_skills:
            staff_skills_list.append(result[1])
        response = {
            "data": [
                {
                    "Staff_ID": result[0].Staff_ID,
                    "Staff_Skills" : staff_skills_list
                }
            ],
            "message": "Successfully retrieved staff skills",
            "code": 200
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Error fetching staff skills: " + str(e),
                        "code":500}), 500
    finally:
        db.session.close()#get all role applications by role listing ID as hr
@app.route("/hr/role_applications/<string:role_listing_id>", methods=['GET'])
def get_role_applications_by_id(role_listing_id):
    try:
        staff_applications = (
                            db.session.query(Staff, StaffSkill, RoleApplied)
                            .join(RoleApplied, RoleApplied.Staff_ID == Staff.Staff_ID)
                            .join(StaffSkill, StaffSkill.Staff_ID == Staff.Staff_ID)
                            .filter(RoleApplied.Role_Listing_ID == role_listing_id)
                            .all()
                        )
        if not staff_applications:
            return jsonify({"message": "No staff applied for this role",
                            "code":200}), 200
        staff_details = {}
        for staff, staff_skill, role_applied in staff_applications:
            staff_id = staff.Staff_ID
            if staff_id not in staff_details:
                staff_details[staff_id] = {
                    "staff_id": staff_id,
                    "name": staff.Staff_FName + " " + staff.Staff_LName,
                    "department": staff.Department,
                    "country": staff.Country,
                    "email": staff.Email,
                    "skills": [],
                    "offer_given": role_applied.offer_given,
                    "offer_confirmed": role_applied.offer_confirmed,
                    "offer_reviewed": role_applied.offer_reviewed,
                    "offer_rejected": role_applied.offer_rejected,
                    "brief_description": role_applied.brief_description if role_applied.brief_description else "No description"
                }
            staff_details[staff_id]["skills"].append(staff_skill.Skill_Name)
        response = {
                    "data" :{
                        "staff_applications": list(staff_details.values())
                        },
                    "message": "Successfully retrieved role applications",
                    "code":200
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Error fetching role applications: " + str(e),
                        "code":500}), 500
    finally:
        db.session.close()
    
#get all role skills by role name
@app.route("/role_skills/<string:role_name>", methods=['GET'])
def get_all_role_skills(role_name):
    try:
        role_details = (
                        db.session.query(Role, RoleSkill)
                        .join(RoleSkill, RoleSkill.Role_Name == Role.Role_Name)
                        .filter(Role.Role_Name == role_name)
                        .all()
                    )
        if not role_details:
            return jsonify({"error": "Role name not found"}), 404 
        role_skills = [detail[1].Skill_Name for detail in role_details]
        response = {
            "data" :{
                "role_skills": role_skills,
                },
            "message": "Successfully retrieved role skills"
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Error fetching role skills: " + str(e)}), 500

@app.route('/apply_role',methods=['POST'])
def apply_role():

    ## check parameters
    contents = request.json["message"]
    if "Role_Listing_ID" not in contents or "Staff_ID" not in contents:
        return jsonify({"error":"Missing required fields"}),500

    query = db.session.query(RoleApplied).filter_by(Role_Listing_ID=int(request.json['message']['Role_Listing_ID']),Staff_ID=int(request.json['message']['Staff_ID'])).first()
    print(query)
    if query != None:
        return jsonify({"error" : "Role already applied"}),400
    
    if "brief_message" not in contents:
        applicant_message = None
    else:
        applicant_message = contents["brief_message"]
        
    new_role_application = RoleApplied(
        Role_Listing_ID =int(request.json['message']['Role_Listing_ID']),
        Staff_ID = request.json['message']['Staff_ID'],
        brief_description = applicant_message, 
        applied_at = datetime.now() , 
        offer_given = 0, 
        offer_confirmed = 0, 
        offer_reviewed = 0, 
        offer_rejected = 0
    )
    try:
        db.session.add(new_role_application)
        db.session.commit()
        return jsonify({
            "role_listing_id": new_role_application.Role_Listing_ID,
            "staff_id": new_role_application.Staff_ID,
            "brief_description": new_role_application.brief_description,
            "applied_at": new_role_application.applied_at,
            "offer_given": new_role_application.offer_given,
            "offer_confirmed": new_role_application.offer_confirmed,
            "offer_reviewed": new_role_application.offer_reviewed,
            "offer_rejected": new_role_application.offer_rejected
        }),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating new role application: " + str(e)}), 500

    finally:
        db.session.close()

@app.route('/check_apply_role',methods=['GET'])
def check_applied_role():
    print(request)
    role_listing_id = request.args.get('Role_Listing_ID')
    staff_id = request.args.get('Staff_ID')
    query = db.session.query(RoleApplied).filter_by(Role_Listing_ID=int(role_listing_id),Staff_ID=staff_id).first()
    if query:
        return jsonify({"status":"Role already applied"}),400 
    else:    
        return jsonify({"status":"Role not applied"}),200
    
if __name__ == '__main__':
    initialize_db(app)
    app.run(host='0.0.0.0', port=8080, debug=True)

