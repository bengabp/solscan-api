import { Box, Container } from "@mui/material";
import Drawer from "@mui/material/Drawer";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import List from "@mui/material/List";
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import HomeIcon from "@mui/icons-material/Home";
import BookmarkAddIcon from "@mui/icons-material/BookmarkAdd";

const SideNav = (props) => {
  const DRAWER_WIDTH = 210;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: DRAWER_WIDTH,
          boxSizing: "border-box",
        },
      }}
    >
      <Box sx={{ overflow: "auto", marginTop: "75px" }}>
        <List role="nav" sx={{ paddingLeft: "10px" }}>
          <ListItem key="Home" disablePadding>
            <ListItemButton>
              <ListItemIcon sx={{ minWidth: "40px" }}>
                <HomeIcon></HomeIcon>
              </ListItemIcon>
              <ListItemText primary="Home" sx={{ padding: 0 }} />
            </ListItemButton>
          </ListItem>
          <ListItem key="Watchlist" disablePadding>
            <ListItemButton>
              <ListItemIcon sx={{ minWidth: "40px" }}>
                <BookmarkAddIcon></BookmarkAddIcon>
              </ListItemIcon>
              <ListItemText primary="Watchlist" sx={{ padding: 0 }} />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default SideNav;
