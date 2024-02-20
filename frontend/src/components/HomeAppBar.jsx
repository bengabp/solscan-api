import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  LinearProgress,
} from "@mui/material";

const HomeAppBar = (props) => {
  return (
    <Box>
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Solana Scan
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default HomeAppBar;
