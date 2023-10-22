// ----------------------------------------------------------------
// Author: 2023-09-25/KM

// Description: main FE app to render individual role listing

// Variables:
// Hook/ skills: list of skills required for role
// Hook/ roleListing: object containing role listing details
// Hook/ isApplied: boolean to check if user has applied for role
// Hook/ snackOpen: boolean to check if snackbar should be opened or closed
// Hook/ isClosed: boolean to check if role listing is closed or expired
// Function/ UseEffect: to render skills required for role
// Function/ getIndividualRoleListingsController: to call the backend to get an individual role listing
// Function/ checkIfAppliedController: to call the backend to check if user has applied for role
// Function/ handleClose: to close snackbar
// Function/ UseEffect: to close snackbar after 4 seconds

// Last Modified: 2023-10-21/RP
// ----------------------------------------------------------------
// Modification history:
// - 2023-09-25/KM: Render individual role listing.
// - 2023-09-29/KM: Added controller to interact with backend
// - 2023-10-01/KM: Added error handling for role listing
// - 2023-10-03/KM: Added checkifApplied controller to check if user has applied to role and disable apply button if so.
// - 2023-10-03/KM: Added snackbar to show success message when user applies for role.
// - 2023-10-03/KM: Added function to close snackbar after 4 seconds.
// - 2023-10-03/KM: Added isClosed boolean to check if role listing is closed or expired.
// - 2023-10-09/KM: Added Application Start Date for role listing
// - 2023-10-14/KM: Added scroll for skills required
// - 2023-10-19/KM: Removed hardcoded role listing id
// - 2023-10-19/ZL: Added color matching for skills, added percentage matching for skills
// - 2023-10-20/ZL: Added role applications datagrid for HR
// - 2023-10-20/ZL: Added handling when there are no role applicants for HR
// - 2023-10-21/RP: added authguard

import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Chip,
  Alert,
  Button,
  Snackbar,
  Link,
} from "@mui/material";
import ManIcon from "@mui/icons-material/Man";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import EventBusyIcon from "@mui/icons-material/EventBusy";
import {
  getIndividualRoleListingsController,
  getRoleApplicationsByIdController,
  checkIfAppliedController,
  getStaffSkillByIdController,
} from "../services/service";
import { useParams } from "react-router-dom";
import FormDialog from "../components/ApplyButton";
import AuthGuard from "../components/AuthGuard";
import RoleApplications from '../components/RoleApplications';

const RoleListingIndiv = () => {
  const [skills, setSkills] = useState([]);
  const [roleSkills, setRoleSkills] = useState([]);
  const [roleListing, setRoleListing] = useState({});
  const [isApplied, setIsApplied] = useState(false);
  const [snackOpen, setSnackOpen] = React.useState(false);
  const [isClosed, setIsClosed] = useState(false);
  const [closedMessage, setClosedMessage] = useState("");
  const [error, setError] = useState(null);
  const { id } = useParams();
  const [staffSkills, setStaffSkills] = useState([]);
  const [staffID, setStaffID] = useState(localStorage.getItem("staffID"));
  const [staffAccessGroup, setStaffAccessGroup] = useState(localStorage.getItem('accessGroup'))
  const [skillsMatch, setSkillsMatch] = useState(0);
  const [skillsMatchComment, setSkillsMatchComment] = useState("");
  const [skillsMatchColor, setSkillsMatchColor] = useState();
  const [isLoadingStaffSkills, setIsLoadingStaffSkills] = useState(true);
  const [roleApplicants, setRoleApplicants] = useState([])
  const [roleApplicantsRows, setRoleApplicantsRows] = useState([]);
  const [ifRoleApplicants, setIfRoleApplicants] = useState(true);
  const linkStyle = {
    color: "white",
    textDecoration: "none",
  };

  function fetchRoleListing() {
    getIndividualRoleListingsController(id)
      .then((response) => {
        if (response.data.status != 0) {
          setIsClosed(true);
          setClosedMessage("Closed");
          setError("Role listing has been closed");
        } else if (new Date(response.data.application_deadline) < new Date()) {
          setIsClosed(true);
          setClosedMessage("Listing Expired");
          setError("Role listing has expired");
        } else {
          console.log(response);
          setRoleListing(response.data);
          var skillList = [];
          var roleSkills = [];
          for (var skill of response.data.skills) {
            console.log(skill);
            roleSkills.push(skill);
            var component = (
              <Box marginRight={1} key={skill}>
                <Chip label={skill} color={handleChipColor(skill)} />
              </Box>
            );
            skillList.push(component);
          }
          setSkills(skillList);
          setRoleSkills(roleSkills);
        }

        checkIfAppliedController({
          Role_Listing_ID: id,
          Staff_ID: staffID,
        }).then((response) => {
          if (response == false) {
            setIsApplied(true);
          }
        });
      })
      .catch((error) => {
        setError("Error fetching role listing");
      });
  }

  useEffect(() => {
    let staff_ID = localStorage.getItem("staffID");
    setStaffID(staff_ID);

    if (!isLoadingStaffSkills) {
      fetchRoleListing();
    }
  }, [id, skillsMatch, staffSkills]);

  function handleChipColor(skill) {
    if (staffSkills.includes(skill)) {
      return "success";
    } else {
      return "error";
    }
  }

  useEffect(() => {
    // Fetch staff skills data
    const fetchStaffSkills = async () => {
      try {
        const response = await getStaffSkillByIdController(staffID);
        // error handling based on your API response
        if (response.code !== 200) {
            setError("Error fetching staff skills");
          }
          setStaffSkills(response.data[0].Staff_Skills);
          setIsLoadingStaffSkills(false);
        } catch (error) {
          setError(error.message);
          setIsLoadingStaffSkills(false);
          console.log("fetch error");
        }
      }
    });

    useEffect(() => {
        // Fetch staff skills data
        const fetchStaffSkills = async () => {
            try {
                const response = await getStaffSkillByIdController(staffID);
                // error handling based on your API response
                
                if (response.code !== 200) {
                   setError('Error fetching staff skills');
                }
                setStaffSkills(response.data[0].Staff_Skills);
                setIsLoadingStaffSkills(false);

            } catch (error) {
                setError(error.message);
                setIsLoadingStaffSkills(false);
                console.log("fetch error current staff skills")
            }
        };

        fetchStaffSkills();
    }, [staffID]); 

    useEffect(()=>{
        // Fetch role applicants data okay
        const fetchRoleApplications = async () => {
            try{
                const response = await getRoleApplicationsByIdController(id);
                if (response.code !== 200) {
                    console.log(response)
                    setError('Error fetching role applicants');
                }
                if (response.message !== "No staff applied for this role") {
                    setRoleApplicants(response.data.staff_applications);
                }
                else {
                    setIfRoleApplicants(false);
                }
            } catch (error){
                setError(error.message);
                console.log("fetch role applicants error")
            }
        };
        fetchRoleApplications(id);
    },[]);


    useEffect(() => {
        // Fetch one staff skills data
        const fetchOneStaffSkills = async (id) => {
            try {
                const response = await getStaffSkillByIdController(id);
                // error handling based on your API response
                
                if (response.code !== 200) {
                   setError('Error fetching staff skills');
                }
                return(response.data[0].Staff_Skills);
                

            } catch (error) {
                setError(error.message);
                console.log("fetch error one staff skills")
            }
        };
        const processRoleApplicants = async () => {
            var roleApplicantsRowsProcessed = []
            var id_count = 1
            if (roleApplicants.length !== 0) {
                for (let roleApplicantsRow of roleApplicants) 
                    try {
                        let applicantStaffSkills = await fetchOneStaffSkills(roleApplicantsRow.staff_id); 
                        let overlappedSkills = roleSkills.filter(skill => applicantStaffSkills.includes(skill));
                        let skillMatchPercentage = Math.floor((overlappedSkills.length / roleSkills.length) * 100);
                        let roleApplicantsRowProcessed = {
                            id: id_count,
                            staff_id: roleApplicantsRow.staff_id,
                            name: roleApplicantsRow.name,
                            department: roleApplicantsRow.department,
                            country: roleApplicantsRow.country,
                            email: roleApplicantsRow.email,
                            skillsMatch: skillMatchPercentage,
                            offer_reviewed: roleApplicantsRow.offer_reviewed,
                            offer_given: roleApplicantsRow.offer_given,
                        }
                        id_count += 1;
                        roleApplicantsRowsProcessed.push(roleApplicantsRowProcessed);
                    } catch (error) {
                        console.log("Error processing role applicant:", error);
                        // Handle the error appropriately here, such as setting an error state or message
                    }
                }
                id_count = 1;
                console.log(roleApplicantsRowsProcessed)
                setRoleApplicantsRows(roleApplicantsRowsProcessed);
            }
            
            processRoleApplicants(); // execute the async function
        }, [roleApplicants, roleSkills]);
     
    // Effect for calculating skill match percentage
    useEffect(() => {
        if (roleSkills.length && staffSkills.length) {
            const overlappedSkills = roleSkills.filter(skill => staffSkills.includes(skill));
            setSkillsMatch(Math.floor((overlappedSkills.length / roleSkills.length) * 100));
        }
    }, [skills, staffSkills]);

    useEffect(() =>  {
        if(parseInt(skillsMatch) >= 80) {
            setSkillsMatchComment("You are a great match for this role!")
            setSkillsMatchColor("green.main")
          
        }
        else if(parseInt(skillsMatch) >= 50) {
            
            setSkillsMatchComment("You are a match for this role!")
            setSkillsMatchColor("secondary.main")
           
            
        }
        else {
            setSkillsMatchComment("Expand your skills to be a better match for this role!")
            setSkillsMatchColor("error")
            
        }
    },[skillsMatch,roleSkills,staffSkills])

  // Effect for calculating skill match percentage
  useEffect(() => {
    if (roleSkills.length && staffSkills.length) {
      const overlappedSkills = roleSkills.filter((skill) =>
        staffSkills.includes(skill)
      );
      setSkillsMatch(
        Math.floor((overlappedSkills.length / roleSkills.length) * 100)
      );
    }
  }, [skills, staffSkills]);

  useEffect(() => {
    console.log(skillsMatch);
    if (parseInt(skillsMatch) >= 80) {
      setSkillsMatchComment("You are a great match for this role!");
      setSkillsMatchColor("green.main");
    } else if (parseInt(skillsMatch) >= 50) {
      setSkillsMatchComment("You are a match for this role!");
      setSkillsMatchColor("secondary.main");
    } else {
      setSkillsMatchComment(
        "Expand your skills to be a better match for this role!"
      );
      setSkillsMatchColor("error");
    }
  }, [skillsMatch, roleSkills, staffSkills]);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (snackOpen) {
        setSnackOpen(false);
      }
    }, 4000);

    return () => clearTimeout(timer); // Clear the timer on component unmount
  }, [snackOpen]);

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      setSnackOpen(false);
      return;
    }
    setSnackOpen(false);
  };

  return (
    <Box marginLeft={15} marginRight={5} marginTop={1}>
      <AuthGuard />
      {error ? (
        <Box>
          <Box margin={2}>
            <Button variant="contained" color="secondary">
              <Link to="/role-listings" style={linkStyle}>
                Back to Role Listings
              </Link>
            </Button>
          </Box>

          <Box margin={2}>
            <Alert severity="error">{error}</Alert>
          </Box>
        </Box>
      ) : (
        <React.Fragment>
          <Box>
            <Typography variant="h4" fontWeight={"bold"}>
              {roleListing.role_name}
            </Typography>
            <Typography variant="p">
              {roleListing.department} · {roleListing.country} ·{" "}
              {roleListing.created_at} · {roleListing.openings} openings
            </Typography>
          </Box>
          <Box marginTop={4}>
            <Box alignItems={"center"} display={"flex"}>
              <ManIcon />
              <Typography variant="p" marginLeft={0.8}>
                <b>Reports to:</b> {roleListing.reporting_manager_name}
              </Typography>
            </Box>
            <Box alignItems={"center"} display={"flex"}>
              <EventAvailableIcon />
              <Typography variant="p" marginLeft={0.8}>
                <b>Application Start Date:</b>{" "}
                {new Date(roleListing.application_start).toLocaleDateString()}
              </Typography>
            </Box>
            <Box alignItems={"center"} display={"flex"}>
              <EventBusyIcon />
              <Typography variant="p" marginLeft={0.8}>
                <b>Application Deadline:</b>{" "}
                {new Date(
                  roleListing.application_deadline
                ).toLocaleDateString()}
              </Typography>
            </Box>
          </Box>
          <Box marginTop={4}>
            <Typography variant="h6" fontWeight={"bold"}>
              Skills Required
            </Typography>
            <Box
              display={"flex"}
              style={{ overflowX: "auto", maxHeight: "200px", padding: "10px" }}
            >
              {skills}
            </Box>
            <Typography variant="body1" marginTop={2}>
              *Skills in <span sx={{ color: "green" }}>green</span> are skills
              you have
            </Typography>
          </Box>
          <Box marginTop={4}>
            <Typography variant="h6" fontWeight={"bold"}>
              Skills Match Percentage{" "}
            </Typography>
            <Typography variant="h4" color={skillsMatchColor}>
              {skillsMatch} %
            </Typography>
            <Typography variant="body1">{skillsMatchComment}</Typography>
          </Box>
          <Box marginTop={4}>
            <Typography variant="h6" fontWeight={"bold"}>
              About the Role
            </Typography>
            <Typography variant="p">{roleListing.role_desc}</Typography>
          </Box>
          <Box marginTop={4}>
            {isApplied ? (
              <Button
                variant="contained"
                size="medium"
                color="primary"
                disabled
              >
                Applied
              </Button>
            ) : isClosed ? (
              <Button
                variant="contained"
                size="medium"
                color="primary"
                disabled
              >
                {closedMessage}
              </Button>
            ) : (
                <React.Fragment>
                     <Box>
                        <Typography variant='h4' fontWeight={'bold'}>{roleListing.role_name}</Typography>
                        <Typography variant='p'>{roleListing.department} · {roleListing.country} · {roleListing.created_at} · {roleListing.openings} openings</Typography>
                    </Box>
                    <Box marginTop={4}>
                        <Box alignItems={'center'} display={'flex'}>
                            <ManIcon/>
                            <Typography variant='p' marginLeft={0.8}><b>Reports to:</b> {roleListing.reporting_manager_name}</Typography>
                        </Box>
                        <Box alignItems={'center'} display={'flex'}>
                            <EventAvailableIcon />
                            <Typography variant='p' marginLeft={0.8}><b>Application Start Date:</b> {new Date(roleListing.application_start).toLocaleDateString()}</Typography>
                        </Box>
                        <Box alignItems={'center'} display={'flex'}>
                            <EventBusyIcon />
                            <Typography variant='p' marginLeft={0.8}><b>Application Deadline:</b> {new Date(roleListing.application_deadline).toLocaleDateString()}</Typography>
                        </Box>
                    </Box>
                    <Box marginTop={4}>
                        <Typography variant='h6' fontWeight={'bold'}>Skills Required</Typography>
                        <Box display={'flex'} style={{ overflowX: 'auto', maxHeight: '200px' ,padding: '10px'}}>
                            {skills}
                        </Box>
                        <Typography variant='body1' marginTop={2}>
                            *Skills in <span sx={{ color: 'green' }}>green</span> are skills you have
                        </Typography>
                    </Box>
                    <Box marginTop={4}>
                        <Typography variant='h6' fontWeight={'bold'}>Skills Match Percentage </Typography>
                        <Typography variant='h4' color={skillsMatchColor}>
                            {skillsMatch} %
                        </Typography>
                        <Typography variant='body1' >
                            {skillsMatchComment}
                        </Typography>
                    </Box>
                    <Box marginTop={4}>
                        <Typography variant='h6' fontWeight={'bold'}>About the Role</Typography>
                        <Typography variant='p'>{roleListing.role_desc}</Typography>
                    </Box>
                    
                    {staffAccessGroup === "HR" &&ifRoleApplicants?(
                    <Box marginTop={4}>
                        <RoleApplications rows={roleApplicantsRows}/>
                    </Box>):null}
                    {staffAccessGroup === "HR" && (ifRoleApplicants ===false) ?(
                    <Box marginTop={4}>
                        <Typography variant='h6' fontWeight={'bold'}>Role Applicants</Typography>
                        <Typography>There are no applicants for this role.</Typography>
                    </Box>):null}
                    <FormDialog
                        roleListingId={id}
                        roleName={roleListing.role_name}
                        staffID={staffID}
                        isApplied={isApplied}
                        setIsApplied={setIsApplied}
                        snackOpen={snackOpen}
                        setSnackOpen={setSnackOpen}
                    ></FormDialog>
                </React.Fragment>
            )}
          </Box>
          {snackOpen && isApplied && (
            <Snackbar open={true} autoHideDuration={6000} onClose={handleClose}>
              <Alert
                onClose={handleClose}
                severity="success"
                sx={{ width: "100%" }}
              >
                You have successfully applied for {roleListing.role_name} role
                listing!
              </Alert>
            </Snackbar>
          )}
          {!isApplied && snackOpen && (
            <Snackbar open={true} autoHideDuration={6000} onClose={handleClose}>
              <Alert
                onClose={handleClose}
                severity="error"
                sx={{ width: "100%" }}
              >
                Error: There was an error applying for this role.
              </Alert>
            </Snackbar>
          )}
        </React.Fragment>
      )}
    </Box>
  );
};

export default RoleListingIndiv;
