// ----------------------------------------------------------------
// Author: 2023-10-09/RP
//
// Description: Navbar component (with role access)
//
// Variables:
//
// Last Modified: 2023-10-21/RP
// ----------------------------------------------------------------
// Modification history:
// -2023-10-09/RP: created NavBar component
// -2023-10-21/RP: added access control and create role listing page

import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import MuiDrawer from "@mui/material/Drawer";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import CottageIcon from "@mui/icons-material/Cottage";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import DashboardIcon from "@mui/icons-material/Dashboard";
import SpeakerNotesIcon from "@mui/icons-material/SpeakerNotes";
import DescriptionIcon from "@mui/icons-material/Description";
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import LogoutIcon from "@mui/icons-material/Logout";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import LibraryAddIcon from "@mui/icons-material/LibraryAdd";
import Tooltip from "@mui/material/Tooltip";
import WorkIcon from "@mui/icons-material/Work";
import Person4Icon from "@mui/icons-material/Person4";
import { Link } from "react-router-dom";
import BadgeIcon from "@mui/icons-material/Badge";
import CreateIcon from "@mui/icons-material/Create";
import LoginIcon from "@mui/icons-material/Login";

// imports for controlling the drawer according to the user authencation
// import { getCurrentUser, authLogOut } from "../../services/AuthService";
// import EventBus from "../../common/EventBus";
import AccountBoxIcon from "@mui/icons-material/AccountBox";
import Create from "@mui/icons-material/Create";
import * as LINKS from "../constants/Links";

// sample code from mui
const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": closedMixin(theme),
  }),
}));

export default function Navbar({ children }) {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  // const [page, setPage] = React.useState("Dashboard")
  const [page, setPage] = React.useState("All-in-One");
  const [isLoggedIn, setIsLoggedIn] = React.useState(
    localStorage.getItem("accessGroup") != null
  );

  // Template for the pages and widgets for easier reference

  const pages = ["Role Listings", "Create Role Listing", "Staff"];
  // const widgets = ['Account','Logout']
  const iconsPrimary = [<WorkIcon />, <Create />, <Person4Icon />];
  // const iconsSecondary = [
  //   <AccountCircleIcon/>,
  //   <LogoutIcon/>,
  // ]

  // Template for the pages and widgets for easier reference

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleLogout = () => {
    localStorage.clear();
    setIsLoggedIn(false);
  };

  return (
    <Box sx={{ display: "flex" }}>
      {/* Appbar to be present in all pages */}
      <AppBar position="fixed" open={open}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{
              marginRight: 5,
              ...(open && { display: "none" }),
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            {page}
          </Typography>
        </Toolbar>
      </AppBar>
      {/* drawer component to replace the navbar component eventually */}
      <Drawer variant="permanent" open={open}>
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {isLoggedIn && (
            <>
              <ListItem
                key="Role Listings"
                disablePadding
                sx={{ display: "block" }}
                onClick={() => setPage("Role Listings")}
              >
                <Link
                  to={LINKS.ALL_ROLE_LISTINGS}
                  style={{
                    textDecoration: "none",
                    textTransform: "capitalize",
                    color: "#636466",
                  }}
                >
                  <ListItemButton
                    sx={{
                      minHeight: 48,
                      justifyContent: open ? "initial" : "center",
                      px: 2.5,
                    }}
                  >
                    <Tooltip title="Role Listings" placement="right-start">
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: open ? 3 : "auto",
                          justifyContent: "center",
                        }}
                      >
                        <WorkIcon />
                      </ListItemIcon>
                    </Tooltip>
                    <ListItemText
                      secondary={"Role Listings"}
                      disableTypography={true}
                      sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                    />
                  </ListItemButton>
                </Link>
              </ListItem>

              {localStorage.getItem("accessGroup") !== "User" && isLoggedIn && (
                <>
                  <ListItem
                    key="Create Role Listings"
                    disablePadding
                    sx={{ display: "block" }}
                    onClick={() => setPage("Staff")}
                  >
                    <Link
                      // change the bottom line to route create role listing
                      to={LINKS.CREATE_ROLE_LISTING}
                      style={{
                        textDecoration: "none",
                        textTransform: "capitalize",
                        color: "#636466",
                      }}
                    >
                      <ListItemButton
                        sx={{
                          minHeight: 48,
                          justifyContent: open ? "initial" : "center",
                          px: 2.5,
                        }}
                      >
                        <Tooltip
                          title="Create Role Listing"
                          placement="right-start"
                        >
                          <ListItemIcon
                            sx={{
                              minWidth: 0,
                              mr: open ? 3 : "auto",
                              justifyContent: "center",
                            }}
                          >
                            <CreateIcon />
                          </ListItemIcon>
                        </Tooltip>
                        <ListItemText
                          secondary={"Create Role Listing"}
                          disableTypography={true}
                          sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem
                    key="Staff"
                    disablePadding
                    sx={{ display: "block" }}
                    onClick={() => setPage("Staff")}
                  >
                    <Link
                      // change the bottom to route view all staffs
                      // to={"/Staff"}
                      style={{
                        textDecoration: "none",
                        textTransform: "capitalize",
                        color: "#636466",
                      }}
                    >
                      <ListItemButton
                        sx={{
                          minHeight: 48,
                          justifyContent: open ? "initial" : "center",
                          px: 2.5,
                        }}
                      >
                        <Tooltip title="Staff" placement="right-start">
                          <ListItemIcon
                            sx={{
                              minWidth: 0,
                              mr: open ? 3 : "auto",
                              justifyContent: "center",
                            }}
                          >
                            <Person4Icon />
                          </ListItemIcon>
                        </Tooltip>
                        <ListItemText
                          secondary={"Staff"}
                          disableTypography={true}
                          sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                </>
              )}
              <ListItem
                key="My Profile"
                disablePadding
                sx={{ display: "block" }}
                onClick={() => setPage("My Profile")}
              >
                <Link
                  // change the bottom to route view personal profile
                  // to={"/StaffProfile"}
                  style={{
                    textDecoration: "none",
                    textTransform: "capitalize",
                    color: "#636466",
                  }}
                >
                  <ListItemButton
                    sx={{
                      minHeight: 48,
                      justifyContent: open ? "initial" : "center",
                      px: 2.5,
                    }}
                  >
                    <Tooltip title="My Profile" placement="right-start">
                      <ListItemIcon
                        sx={{
                          minWidth: 0,
                          mr: open ? 3 : "auto",
                          justifyContent: "center",
                        }}
                      >
                        <BadgeIcon />
                      </ListItemIcon>
                    </Tooltip>
                    <ListItemText
                      secondary={"My Profile"}
                      disableTypography={true}
                      sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                    />
                  </ListItemButton>
                </Link>
              </ListItem>
              <Divider />
            </>
          )}
        </List>

        {isLoggedIn ? (
          <ListItem
            key="Logout"
            disablePadding
            sx={{ display: "block" }}
            onClick={() => handleLogout()}
          >
            <Link
              // change the bottom to route to login page
              to={LINKS.LOGIN}
              style={{
                textDecoration: "none",
                textTransform: "capitalize",
                color: "#636466",
              }}
            >
              <ListItemButton
                sx={{
                  minHeight: 48,
                  justifyContent: open ? "initial" : "center",
                  px: 2.5,
                }}
              >
                <Tooltip title="Logout" placement="right-start">
                  <ListItemIcon
                    sx={{
                      minWidth: 0,
                      mr: open ? 3 : "auto",
                      justifyContent: "center",
                    }}
                  >
                    <LogoutIcon />
                  </ListItemIcon>
                </Tooltip>
                <ListItemText
                  secondary={"Logout"}
                  disableTypography={true}
                  sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                />
              </ListItemButton>
            </Link>
          </ListItem>
        ) : (
          <ListItem
            key="Login"
            disablePadding
            sx={{ display: "block" }}
            // onClick={() => handleLogout()}
          >
            <Link
              // change the bottom to route to login page
              to={LINKS.LOGIN}
              style={{
                textDecoration: "none",
                textTransform: "capitalize",
                color: "#636466",
              }}
            >
              <ListItemButton
                sx={{
                  minHeight: 48,
                  justifyContent: open ? "initial" : "center",
                  px: 2.5,
                }}
              >
                <Tooltip title="Login" placement="right-start">
                  <ListItemIcon
                    sx={{
                      minWidth: 0,
                      mr: open ? 3 : "auto",
                      justifyContent: "center",
                    }}
                  >
                    <LoginIcon />
                  </ListItemIcon>
                </Tooltip>
                <ListItemText
                  secondary={"Login"}
                  disableTypography={true}
                  sx={{ opacity: open ? 1 : 0, fontSize: 16 }}
                />
              </ListItemButton>
            </Link>
          </ListItem>
        )}
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, my: "40px" }}>
        {children}
      </Box>
    </Box>
  );
}
