// ----------------------------------------------------------------
// Author: 2023-09-25/RT

// Description: main create role listing page

// Variables:
// Hook/ roles: all roles queried from backend API
// Hook/ departments: all departments queried from backend API
// Hook/ countries: all countries queried from backend API
// Hook/ managers: all managers queried from backend API
// Hook/ roleDesc: Description of the selected role in the dropdown
// Hook/ roleSkills: Skills of the selected role in the dropdown
// Hook/ form: form data
// Hook/ error: error message when submit is clicked
// Function/ useEffect: function called at the start of the page render. Gets details from backend API ( departments, roles, countries, managers)
// Function/ useEffect: function called whenever role is selected. Changes skill array and re render the skills array
// Function / handleChange: changes the form data
// Function / handleApplicationDeadlineDateChange: changes the applicationDeadline in the form
// Function / handleApplicationStartDateDateChange: changes the applicationStartDate in the form
// Function / handleRoleChange: handles the role change event.
// Function / handleSubmit: submit function when the submit button is clicked

// Last Modified: 2023-10-21/RP
// ----------------------------------------------------------------
// Modification history:
// - 2023-09-25/RT: created role listing page
// - 2023-10-03/RP: linked backendAPI to frontend
// - 2023-10-14/ZL: added Application Start Date field
// - 2023-10-21/RP: added authguard

import React, { useEffect, useState } from "react";
import dayjs from "dayjs";
import {
  Box,
  Typography,
  Chip,
  Card,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Alert,
  AlertTitle,
} from "@mui/material";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import * as LINKS from "./../constants/Links";
import {
  getAllCountriesController,
  getAllDepartmentsController,
  getAllManagersController,
  getAllRolesController,
  createRoleListingController,
} from "../services/service";
import { useNavigate } from "react-router-dom";
import AuthGuard from "../components/AuthGuard";

const CreateRoleListing = () => {
  //   const [roleName, setRoleName] = useState("");
  //   const [description, setDescription] = useState(
  //     "Please select a role name first"
  //   );
  const [skills, setSkills] = useState(
    <Typography variant="p">Please select a role name first</Typography>
  );
  const [applicantsFormatted, setApplicantsFormatted] = useState([]);

  const [form, setForm] = useState({
    country: "",
    department: "",
    reportingManagerID: 0,
    applicationStartDate: "",
    applicationDeadline: "",
    openings: 0,
    roleName: "",
    status: 1,
  });

  // backend input data:
  const navigate = useNavigate();
  const [roles, setRoles] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [managers, setManagers] = useState([]);
  const [countries, setCountries] = useState([]);

  // FE hooks:
  const [roleDesc, setRoleDesc] = useState("");
  const [roleSkills, setRoleSkills] = useState([]);
  const isFormFilled =
    form.country != "" &&
    form.department != "" &&
    form.reportingManagerID != "" &&
    form.applicationDeadline != "" &&
    form.applicationStartDate != "" &&
    form.roleName != "";

  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // backend call to the Database
  useEffect(() => {
    // checks if user is HR, else redirect
    if (localStorage.getItem("accessGroup") == "User") {
      navigate(LINKS.ALL_ROLE_LISTINGS);
    }

    // get all countries
    getAllCountriesController().then((res) => {
      setCountries(res);
    });

    // get all departments
    getAllDepartmentsController().then((res) => {
      setDepartments(res);
    });

    // get all managers
    getAllManagersController().then((res) => {
      setManagers(res);
    });

    // get all roles
    getAllRolesController().then((res) => {
      setRoles(res);
    });
  }, []);

  useEffect(() => {
    console.log(form);
  }, [form]);

  useEffect(() => {
    console.log(error);
  }, [error]);

  useEffect(() => {
    console.log(errorMessage);
  }, [errorMessage]);

  const handleChange = (formControl, event) => {
    console.log(formControl, event.target.value);
    if (formControl == "openings") {
      setForm({
        ...form,
        [formControl]: event.target.value - 0,
      });
      return;
    }
    setForm({
      ...form,
      [formControl]: event.target.value,
    });
  };

  const handleApplicationDeadlineDateChange = (newDate) => {
    setForm({
      ...form,
      ["applicationDeadline"]: newDate,
    });
  };

  const handleApplicationStartDateDateChange = (newDate) => {
    setForm({
      ...form,
      ["applicationStartDate"]: newDate,
    });
  };

  const handleRoleChange = (role_name) => {
    setForm({
      ...form,
      ["roleName"]: role_name,
    });
    let role = roles.filter((r) => r.Role_Name === role_name)[0];
    // console.log(role);
    setRoleDesc(role.Role_Desc);
    setRoleSkills(role.Skills);
  };

  const handleSubmit = () => {
    const currentDate = dayjs().format("YYYY-MM-DD");
    console.log("submit clicked, current date is ", currentDate);
    if (currentDate > form.applicationDeadline) {
      setError(true);
      setErrorMessage("Please set a valid Application Deadline");
      return;
    }
    if (currentDate > form.applicationStartDate) {
      setError(true);
      setErrorMessage("Please set a valid Application Start Date");
      return;
    }

    if (form.openings <= 0) {
      setError(true);
      setErrorMessage("Please set a valid number of openings");
      return;
    }

    // submit function:
    createRoleListingController(form)
      .then((res) => {
        console.log(res);
        if (res.status === 400 || res.status === 500) {
          setError(true);
          setErrorMessage(res.data.error);
          return;
        } else {
          navigate(`${LINKS.ALL_ROLE_LISTINGS}`);
          return;
          //   console.log(res);
        }
      })
      .catch((err) => {
        console.log(err);
        setError(true);
        setErrorMessage(err);
      });
  };

  useEffect(() => {
    var skillList = [];
    for (var skill of roleSkills) {
      console.log(skill);
      var component = (
        <Box marginRight={1}>
          <Chip key={skill} label={skill} color="secondary" />
        </Box>
      );
      skillList.push(component);
    }
    setSkills(<Box display={"flex"}>{skillList}</Box>);
  }, [roleSkills]);

  return (
    <Box marginLeft={15} marginRight={5} marginTop={15}>
      <AuthGuard />

      <Box>
        <Typography variant="h4" fontWeight={"bold"}>
          Create new role listing
        </Typography>
      </Box>
      {error && (
        <Box>
          <Alert severity="error">
            <AlertTitle>Error</AlertTitle>
            {errorMessage}
          </Alert>
        </Box>
      )}
      <Box marginTop={2} width={"50%"}>
        <FormControl fullWidth margin="normal">
          <InputLabel id="demo-simple-select-label">Role Name</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={form.roleName}
            label="Role Name"
            onChange={(event) => handleRoleChange(event.target.value)}
          >
            {roles.map((role, index) => {
              return (
                <MenuItem key={role.Role_Name} value={role.Role_Name}>
                  {role.Role_Name}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
      </Box>
      <Box marginTop={4}>
        <Typography variant="h6" fontWeight={"bold"}>
          Description
        </Typography>
        <Typography variant="p">{roleDesc}</Typography>
      </Box>
      <Box marginTop={4}>
        <Typography variant="h6" fontWeight={"bold"}>
          Skills Required
        </Typography>
        {skills}
      </Box>
      <Box marginTop={4} width={"50%"}>
        <FormControl fullWidth margin="normal">
          <InputLabel id="demo-simple-select-label">Department</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={form.department}
            label="Department"
            onChange={(event) => handleChange("department", event)}
          >
            {departments.map((department, index) => {
              return (
                <MenuItem key={index} value={department}>
                  {department}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
        <FormControl fullWidth margin="normal">
          <InputLabel id="demo-simple-select-label">
            Reporting Manager
          </InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={form.reportingManagerID}
            label="Reporting Manager"
            onChange={(event) => handleChange("reportingManagerID", event)}
          >
            {managers.map((manager, index) => {
              return (
                <MenuItem key={manager.Staff_ID} value={manager.Staff_ID}>
                  {manager.Staff_FName} {manager.Staff_LName}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
        <FormControl fullWidth margin="normal">
          <InputLabel id="demo-simple-select-label">Country</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={form.country}
            label="Country"
            onChange={(event) => handleChange("country", event)}
          >
            {countries.map((country, index) => {
              return (
                <MenuItem key={index} value={country}>
                  {country}
                </MenuItem>
              );
            })}
          </Select>
        </FormControl>
        <TextField
          type="number"
          label="Number of openings"
          value={form.openings}
          onChange={(event) => handleChange("openings", event)}
          fullWidth
          margin="normal"
        ></TextField>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Box width={"100%"}>
            <DatePicker
              label="Application StartDate"
              id="startdate"
              name="startdate"
              value={
                // dayjs(form.StartDate)
                form.applicationStartDate == "" ||
                form.applicationStartDate == undefined
                  ? null
                  : dayjs(form.applicationStartDate)
              }
              onChange={
                (newDate) =>
                  handleApplicationStartDateDateChange(
                    newDate.format("YYYY-MM-DD")
                  )
                // console.log(newDate.format("YYYY-MM-DD"))
              }
              format="YYYY-MM-DD"
              required
              slotProps={{ textField: { fullWidth: true, margin: "normal" } }}
            />
          </Box>
        </LocalizationProvider>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Box width={"100%"}>
            <DatePicker
              label="Application Deadline"
              id="deadline"
              name="deadline"
              value={
                // dayjs(form.applicationDeadline)
                form.applicationDeadline == "" ||
                form.applicationDeadline == undefined
                  ? null
                  : dayjs(form.applicationDeadline)
              }
              onChange={
                (newDate) =>
                  handleApplicationDeadlineDateChange(
                    newDate.format("YYYY-MM-DD")
                  )
                // console.log(newDate.format("YYYY-MM-DD"))
              }
              format="YYYY-MM-DD"
              required
              slotProps={{ textField: { fullWidth: true, margin: "normal" } }}
            />
          </Box>
        </LocalizationProvider>
      </Box>
      <Box marginTop={4}>
        <Button
          disabled={!isFormFilled}
          type="submit"
          variant="contained"
          color="tertiary"
          onClick={handleSubmit}
        >
          Create
        </Button>
      </Box>
    </Box>
  );
};

export default CreateRoleListing;
