// Author: 2023-09-23/RP

// Description: main FE app to render all the different screens for the different routes.

// Last Modified: 2023-10-14/ZL
// ----------------------------------------------------------------
// Modification history:
// - 2023-09-23/RP: Created main FE App.
// - 2023-09-29/KM: Modified route for individual role listing to include dynamic parameter
// - 2023-10-09/RP: Added NavBar component
// - 2023-10-11/RP: Added login component
// - 2023-10-14/ZL: Added create role listing route

import { React } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { createTheme, ThemeProvider } from "@mui/material";
import AllRoleListings from "./pages/AllRoleListings.js";
import RoleListingIndiv from "./pages/RoleListingIndiv.js";
import CreateRoleListing from "./pages/CreateRoleListing";

import * as LINKS from "./constants/Links";
import Navbar from "./components/NavBar.js";
import Login from "./pages/Login.js";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Navbar />
        <Routes>
          <Route path={LINKS.ALL_ROLE_LISTINGS} element={<AllRoleListings />} />
          <Route
            path={LINKS.INDIVIDUAL_ROLE_LISTING}
            element={<RoleListingIndiv />}
          />
          <Route path={LINKS.LOGIN} element={<Login />} />
          <Route
            path={LINKS.CREATE_ROLE_LISTING}
            element={<CreateRoleListing />}
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

const theme = createTheme({
  // typography: {
  //   fontFamily: 'Your-Selected-Font, sans-serif', // Replace 'Your-Selected-Font' with your font name
  // },

  palette: {
    primary: {
      light: "#E0E0E0",
      main: "#E2D579",
      contrastText: "#040404",
    },
    secondary: {
      light: "#DE8C9D",
      main: "#47A8BD",
      contrastText: "#FDFDFD",
    },
    tertiary: {
      light: "#2af0ea",
      main: "#1E3888",
      contrastText: "#FDFDFD",
    },
    green: {
      main: "#2A9134",
      contrastText: "#FDFDFD",
    },
    red: {
      main: "#C33149",
      contrastText: "#FDFDFD",
    },
    orange: {
      main: "#A36A00",
      contrastText: "#FDFDFD",
    },
    contrastThreshold: 3,
    tonalOffset: 0.2,
  },
});

export default App;
