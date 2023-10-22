// ----------------------------------------------------------------
// Author: 2023-10-11/RP

// Description: FE for login page

// Variables:
// Function/ useEffect: get backend data for allStaffs.
// Hook/ open: useState hook for open state of dropdown
// Hook/ value: useState hook for value of dropdown
// Hook/ allStaffs: List containing all staffs

// Last Modified: 2023-10-11/RP
// ----------------------------------------------------------------
// Modification history:
// - 2023-10-11/RP: Added Login page

import React, { useEffect, useState } from "react";
import {
  Avatar,
  Button,
  TextField,
  Link,
  Box,
  Typography,
  Container,
  Snackbar,
} from "@mui/material";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { getAllStaffsController } from "../services/service";
import { useNavigate } from "react-router-dom";
import * as LINKS from "../constants/Links";

export default function Login() {
  const [open, setOpen] = useState(false);
  //   const [staffID, setStaffID] = useState("");
  //   const [accessName, setAccessName] = useState("");
  const [value, setValue] = useState("");
  const [allStaffs, setAllStaffs] = useState([]);
  const navigate = useNavigate();

  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (event) => {
    // need to find the staff ID
    // console.log(event);
    const id = event.target.value;
    const staff = allStaffs.find((staff) => staff.Staff_ID === id);

    localStorage.setItem("accessGroup", staff.Access_Control_Name);
    localStorage.setItem("staffID", id);
    // navigate(LINKS.ALL_ROLE_LISTINGS);
    window.location.href = LINKS.ALL_ROLE_LISTINGS;
    return;
  };

  useEffect(() => {
    getAllStaffsController()
      .then((res) => {
        setAllStaffs(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: "60%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
        textAlign={"center"}
      >
        <Typography variant="h4" fontWeight={"bold"}>
          Login to All-In-One's Skill Based Role Portal
        </Typography>
        <Box marginTop={4}>
          <FormControl sx={{ m: 1, minWidth: "300px" }}>
            <InputLabel id="demo-controlled-open-select-label">
              Select Staff
            </InputLabel>
            <Select
              labelId="demo-controlled-open-select-label"
              id="demo-controlled-open-select"
              open={open}
              onClose={handleClose}
              onOpen={handleOpen}
              value={value}
              label="Select Staff"
              onChange={handleChange}
            >
              {allStaffs.length !== 0 &&
                allStaffs.map((staff) => {
                  return (
                    <MenuItem value={staff.Staff_ID} key={staff.Staff_ID}>
                      {staff.Staff_FName} {staff.Staff_LName},{" "}
                      {staff.Access_Control_Name}
                    </MenuItem>
                  );
                })}
            </Select>
          </FormControl>
        </Box>
      </Box>
    </Container>
  );
}
