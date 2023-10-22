// ----------------------------------------------------------------
// Author: 2023-10-20/ZL
//
// Description: Role application datagrid for HR
//
// Variables:
//
// Last Modified: 2023-10-20/ZL
// ----------------------------------------------------------------
// Modification history:
// -2023-10-20/ZL: created Role application datagrid for HR

import React from 'react';
import { DataGrid } from "@mui/x-data-grid";
import { Box,Button, Card } from '@mui/material';
import { useNavigate } from "react-router-dom";
import * as LINKS from "./../constants/Links";
function RoleApplications(props) {
    const navigate = useNavigate();
    const handleClick = (params) => {
        navigate(LINKS.STAFF_PROFILE.slice(0,-3)  + params.row.staff_id);
      };

    const columns = [
        {
            field:'name',
            headerName:'Name',
            flex: 1,
            editable: false,
            renderCell: (params) => (
                <Box overflow={"auto"}>
                    {params.row.name}
                </Box>
            ),
            
        },
        {
            field:'department',
            headerName:'Department',
            flex: 1,
            editable: false,
            renderCell: (params) => (
                <Box overflow={"auto"}>
                    {params.row.department}
                </Box>
            ),
            
        },
        {
            field:'country',
            headerName:'Country',
            flex: 1,
            editable: false,
            
        },
        //current role?
        {
            field:'email',
            headerName:'Email',
            flex: 1,
            editable: false,
            renderCell: (params) => (
                <Box overflow={"auto"}>
                    {params.row.email}
                </Box>
            ),
            
        },
        {
            field:'brief_description',
            headerName:'Brief Description',
            flex: 1,
            editable: false,
            renderCell: (params) => (
                <Box overflow={"auto"}>
                    {params.row.brief_description}
                </Box>
            ),
            
        },
        {
            field:'skillsMatch',
            headerName:'Percentage Match',
            flex: 1,
            editable: false,
            renderCell:(params)=>{
                return(
                    <Box overflow={"auto"}>
                        <strong>
                            {params.row.skillsMatch}%
                        </strong>
                    </Box>
                )
            }
            
        },
        {
            field:'AcceptRejectButton',
            headerName:'Accept/Reject',
            flex: 1,
            editable: false,
            renderCell:(params)=>{
                return(
                    <Box overflow="auto">
                        <Button variant="contained"
                                        size="small"
                                        style={{ marginLeft: 16, backgroundColor: 'green' }}
                                        >
                                    Accept
                        </Button>
                        <Button variant="contained"
                                        size="small"
                                        style={{ marginLeft: 16, backgroundColor: 'red' }}
                                        >
                                    Reject
                        </Button>
                    </Box>
                )
            }
            
        },
        {
            field:'status',
            headerName:'Status',
            flex: 1,
            editable: false,
            renderCell:(params)=>{
                let AcceptedStatus;
                if (params.row.offer_reviewed === 0) {
                    AcceptedStatus = "Pending";
                } else if (params.row.offer_reviewed === 1 && params.row.offer_given === 1) {
                    AcceptedStatus = "Accepted";
                } else {
                    AcceptedStatus = "Rejected";
                }
                return (
                    //to do accept/reject in another user story
                    <Box overflow="auto">
                        <span>
                            Current Status: <strong>{AcceptedStatus}</strong>
                        </span>
                    </Box>
                );
        
        
            
                }
        },
    ]
    return (
        <Box overflow="auto">
            <DataGrid
                rows={props.rows}
                columns={columns}
                disableSelectionOnClick
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
    );
}

export default RoleApplications;