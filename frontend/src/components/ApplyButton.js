// ----------------------------------------------------------------
// Author: 2023-10-02/KM

// Description: component to render apply button

// Variables:
// Hook/ open: boolean on whether dialog should be opened or closed
// Hook/ message: string to store the message to the hiring manager
// Function/ handleSubmit: to submit application
// Function/ handleTextChange: to update message
// Function/ handleClickOpen: to open dialog box
// Function/ handleClose: to close dialog box

// Last Modified: 2023-10-19/KM
// ----------------------------------------------------------------
// Modification history:
// - 2023-10-02/KM: Created component
// - 2023-10-03/KM: Added apply role listing controller to interact with backend
// - 2023-10-19/KM: Removed hardcoded role listing id


import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { applyRoleListingController } from '../services/service';

const FormDialog = (props) => {
    const {roleListingId,roleName, staffID, isApplied, setIsApplied, snackOpen, setSnackOpen} = props
    const [open, setOpen] = React.useState(false);
    const [message, setMessage] = React.useState('');

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        setSnackOpen(false);
    };

    const handleSubmit = () => {
        // write to database here need staff id and role id and brief message
        var payload = {
            "Role_Listing_ID": roleListingId,
            "brief_message": message,
            "Staff_ID": staffID
        }
        console.log(payload);
        applyRoleListingController(payload).then((response) => {
            if (response != 500) {
              setOpen(false);
              setMessage('');
              setIsApplied(true);
              setSnackOpen(true);

            }else{
              setOpen(false);
              setMessage('');
              setSnackOpen(true);
            }
           
        })

        if (props.onSubmissionSuccess) {
            props.onSubmissionSuccess();
        }

    }

    const handleTextChange = (event) => {
        setMessage(event.target.value);
    }

  return (
    <div>
      <Button variant="contained" size="medium" onClick={handleClickOpen} color='primary'>
        Apply
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Apply for {roleName} Role</DialogTitle>
        <DialogContent>
          <DialogContentText>
            You can choose to add an additional note to the hiring manager here in the text box below.
          </DialogContentText>
            <TextField
            id="standard-multiline-static"
            label="Message to the hiring manager"
            multiline
            rows={4}
            variant="standard"
            fullWidth
            value={message}
            onChange={handleTextChange}
            />
        </DialogContent>
        <DialogActions>
            <Button onClick={handleClose} variant='contained'>Cancel</Button>
            <Button onClick={handleSubmit} variant='contained'>Submit Application</Button>
        </DialogActions>
      </Dialog>
     
    </div>
  );
}




export default FormDialog;