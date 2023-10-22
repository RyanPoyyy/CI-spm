// ----------------------------------------------------------------
// Author: 2023-09-27/RP

// Description: service layer to interact with backend

// Variables:
// Function/ getIndividualRoleListingsController: to call the backend to get an individual role listing
// Function/ applyRoleListingsController: to call the backend to submit an application for a role listing
// Function/ checkIfAppliedController: to call the backend to check if user has applied for role

// Last Modified: 2023-10-20/ZL
// ----------------------------------------------------------------
// Modification history
// - 2023-09-27/RP: getAllRoleListingsController
// - 2023-09-29/KM: getIndividualRoleListingsController
// - 2023-10-02/KM: applyRoleListingsController
// - 2023-10-03/KM: checkIfAppliedController
// - 2023-10-03/RP: getAllDepartmentsController, getAllCountriesController, getAllRolesController, getAllManagersController
// - 2023-10-11/RP: getAllStaffsController
// - 2023-10-14/RP: modified getAllRoleListingsStaffController
// - 2023-10-14/ZL: modified createRoleListingController
// - 2023-10-16/RP: modified getAllRoleListingsStaffController returned format.
// - 2023-10-19/ZL: getStaffSkillByIdController
// - 2023-10-20/ZL: getRoleApplicationsByIdController

import axios from "axios";

// change the API version
const API = "http://localhost:8080";

export const getIndividualRoleListingsController = async (id) => {
  let api_url = API + "/role_listings/" + id;
  try {
    const data = (await axios.get(api_url)).data;
    return data;
  } catch (err) {
    console.log(err);
  }
};

export const getAllRoleListingsStaffController = async () => {
  console.log("controller called");
  try {
    const data = (await axios.get(API + "/rolelistings/staff")).data;
    console.log(data);
    return data[0].data;
  } catch (err) {
    console.log(err);
  }
};

export const applyRoleListingController = async (message) => {
  let api_url = API + "/apply_role";
  try {
    const data = (await axios.post(api_url, {message})).data;
    console.log(data);
    return data
  } catch (err) {
    console.log(err);
    return 500
  }
}

export const checkIfAppliedController = async (message) => { //message should contrain role listing id and staff id
  let api_url = API + "/check_apply_role"
  try {
    const data = (await axios.get(api_url, {
      params: {
        "Role_Listing_ID": message.Role_Listing_ID,
        "Staff_ID": message.Staff_ID
      }
    })).data;
    return data
  } catch (err) {
    console.log(err.response.data.status);
    if(err.response.data.status == "Role already applied"){
      return false
    }
  }
}
export const getAllStaffsController = async () => {
  console.log("getAllStaffs controller called");
  try {
    const data = (await axios.get(API + "/staffs")).data;
    console.log(data);
    return data;
  } catch (err) {
    console.log(err);
  }
};

export const getAllCountriesController = async () => {
  console.log("countries controller called");
  try {
    const data = await axios.get(API + "/countries");
    return data["data"][0]["data"];
  } catch (err) {
    console.log(err);
  }
};

export const getAllDepartmentsController = async () => {
  console.log("departments controller called");
  try {
    const data = await axios.get(API + "/departments");
    return data["data"][0]["data"];
  } catch (err) {
    console.log(err);
  }
};

export const getAllManagersController = async () => {
  console.log("managers controller called");
  try {
    const data = await axios.get(API + "/staff/managers");
    return data["data"][0]["data"];
  } catch (err) {
    console.log(err);
  }
};

export const getAllRolesController = async () => {
  console.log("roles controller called");
  try {
    const data = await axios.get(API + "/roles");
    return data["data"][0]["data"];
  } catch (err) {
    console.log(err);
  }
};

export const createRoleListingController = async (formData) => {
  console.log("creating role listing controller called");
  try {
    const data = await axios.post(API + "/role_listings", formData);
    console.log(data);
    return data;
  } catch (err) {
    console.log(err);
    return err.response;
  }
};

export const getStaffSkillByIdController = (id) => {
  console.log("staffskills controller called");
  let api_url = API + "/staff_skills/" + id;
  return fetch(api_url)
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok for staff skills controller');
    }
    return response.json(); // Parse the response as JSON
  })
  .then((data) => {
    // Work with the JSON data here
    console.log(data);
    return data;
  })
  .catch((error) => {
    console.error('There was a problem fetching staff skills:', error);
    throw error;
  });
  
};

export const getRoleApplicationsByIdController = (id) => {
  console.log("role applications controller called");
  let api_url = API + "/hr/role_applications/" + id;
  return fetch(api_url)
  .then((response) => {
    if (!response.ok) {
      throw new Error('Network response was not ok for role applications controller');
    }
    return response.json(); // Parse the response as JSON
  })
  .then((data) => {
    // Work with the JSON data here
    console.log(data);
    return data;
  })
  .catch((error) => {
    console.error('There was a problem fetching role applications:', error);
    throw error;
  });
  
};
