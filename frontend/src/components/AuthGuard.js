// ----------------------------------------------------------------
// Author: 2023-10-21/RP

// Description: AuthGuard component that returns null. Checks if user is logged in.

// Variables:
// Function/ useEffect: To check if user is logged in

// Last Modified: 2023-10-21/RP
// ----------------------------------------------------------------
// Modification history:
// - 2023-10-21/RP: Created AuthGuard component

import { useEffect } from "react";

const AuthGuard = () => {
  useEffect(() => {
    if (!localStorage.getItem("accessGroup")) {
      window.location.href = "/login";
    }
  });

  return null;
};

export default AuthGuard;
