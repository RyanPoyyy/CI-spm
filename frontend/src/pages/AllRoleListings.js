// ----------------------------------------------------------------
// Author: 2023-09-23/RP
//
// Description: Screen for get all role listings page. Page features a table containing all role listings
//
// Variables:
// function/ useEffect: Get all role listings from backend
// Hook/ roleListings: variable containing all role listings.
//
// Last Modified: 2023-10-21/RP
// ----------------------------------------------------------------
// Modification history:
// - 2023-09-23/RP: Created get all role listings page.
// - 2023-09-25/RP: Formatted and style table. Filled it with dummy data.
// - 2023-09-27/RP: added controller and linked backend to frontend
// - 2023-10-14/RP: Added datagrid and filter/search function
// - 2023-10-16/RP: added application_start to FE datagrid
// - 2023-10-21/RP: added authguard

// Todo, Access control and how the data differs each role (staff cannot see closed role listings)
// sorting, searching, etc.
// navbar

import {
  Table,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
  Paper,
  Box,
  TableBody,
  Chip,
} from "@mui/material";
import { useEffect, useState } from "react";
import { getAllRoleListingsStaffController } from "../services/service";
import * as LINKS from "./../constants/Links";
import { useNavigate } from "react-router-dom";
import { DataGrid } from "@mui/x-data-grid";
import AuthGuard from "../components/AuthGuard";

const dayjs = require("dayjs");

const AllRoleListings = () => {
  // roleListings variable
  const [roleListings, setRoleListings] = useState([]);
  const navigate = useNavigate();
  const [roleName, setRoleName] = useState(localStorage.getItem("accessGroup"));

  const handleClick = (params) => {
    navigate(LINKS.ALL_ROLE_LISTINGS + "/" + params.row.id);
  };

  useEffect(() => {
    // getting roleName control:
    if (roleName == "User") {
      getAllRoleListingsStaffController().then((res) => {
        let data = res;
        setRoleListings(data);
      });
    }
    // if roleName is not user (HR or manager)
    // else{

    // }
  }, []);

  useEffect(() => {
    console.log(roleListings);
  }, [roleListings]);

  // Datagrid columns:
  const columns = [
    {
      field: "role_name",
      headerName: "Role",
      flex: 2,
      editable: false,
      // renderCell: (params) => {
      //   return (
      //     // <Link
      //     //   underline="none"
      //     //   href={"/RoleListing?role=" + params.value}
      //     //   color={"tertiary.main"}
      //     // >

      //     // </Link>
      //   );
      // },
    },

    {
      field: "skills",
      headerName: "Skills Required",
      flex: 4,
      editable: false,
      renderCell: (params) => {
        var skillList = [];
        for (var skill of params.value) {
          var component = (
            <Box marginRight={0.4} key={skill}>
              <Chip label={skill} />
            </Box>
          );
          skillList.push(component);
        }
        return (
          <Box
            sx={{
              display: "flex",
              overflowX: "auto",
              maxWidth: "100%",
              whiteSpace: "nowrap",
            }}
          >
            {skillList}
          </Box>
        );
      },
    },

    {
      field: "department",
      headerName: "Department",
      flex: 2,
      editable: false,
    },

    {
      field: "country",
      headerName: "Country",
      flex: 2,
      editable: false,
    },

    {
      field: "status",
      headerName: "Status",
      flex: 1,
      editable: false,
      renderCell: (params) => {
        if (params.row.status === 0) {
          return <span style={{ color: "#00FF00" }}>Open</span>;
        } else if (params.row.status === 1) {
          return <span style={{ color: "red" }}>Closed</span>;
        }
        return null;
      },
    },

    {
      field: "application_start",
      headerName: "Start Date",
      flex: 2,
      editable: false,
      renderCell: (params) => {
        return dayjs(params.row.application_start).format("DD/MM/YYYY");
      },
    },

    {
      field: "application_deadline",
      headerName: "Application Deadline",
      flex: 2,
      editable: false,
      renderCell: (params) => {
        return dayjs(params.row.application_deadline).format("DD/MM/YYYY");
      },
    },
  ];

  return (
    <>
      <AuthGuard />
      <Box marginLeft={10} marginTop={15}>
        <Box width={"90%"} marginX={"auto"}>
          {/* DatGrid */}
          <DataGrid
            rows={roleListings}
            columns={columns}
            sx={{
              "& .MuiDataGrid-columnHeader, & .MuiDataGrid-columnHeaderTitle": {
                backgroundColor: "secondary.main",
                color: "white",
                fontWeight: "bold",
              },
            }}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 10,
                },
              },
            }}
            pageSizeOptions={[10]}
            onRowClick={handleClick}
          />
        </Box>
      </Box>
    </>
  );
};

export default AllRoleListings;
