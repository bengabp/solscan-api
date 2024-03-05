import * as React from "react";
import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import SearchIcon from "@mui/icons-material/Search";
import DirectionsIcon from "@mui/icons-material/Directions";

export default function CustomSearchBar(props) {
  return (
    <Paper
      component="form"
      elevation={1}
      sx={{ p: "2px 4px", display: "flex", alignItems: "center", width: 400 }}
    >
      <InputBase
        sx={{ ml: 1, flex: 1 }}
        placeholder={props.placeholder}
        inputProps={{ "aria-label": "search-bar-search" }}
        onChange={(event) => {props.onChange(event.target.value)}}
      />
      <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
      <IconButton
        type="button"
        sx={{ p: "10px" }}
        aria-label="search"
        disableFocusRipple={true}
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}
