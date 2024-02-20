import SideNav from "../components/SideNav";

import * as React from "react";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Stack from "@mui/material/Stack";
import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CustomSearchBar from "../components/SearchBar";
import ClickableWalletCard from "../components/walletCard";

const Home = () => {
  // Generate wallet data for 100 users
  const users = Array.from({ length: 100 }, (_, index) => ({
    id: index + 1,
    name: `User ${index + 1}`,
    balance: Math.floor(Math.random() * 1000) + 100, // Generating random balance between 100 and 1099
  }));

  return (
    <Box sx={{ display: "flex" }}>
      <SideNav></SideNav>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Stack direction="row" spacing={3} height={"40px"}>
          <CustomSearchBar placeholder="Search wallets"></CustomSearchBar>
          <Button variant="contained" endIcon={<AddIcon></AddIcon>}>
            Add wallet
          </Button>
        </Stack>
        <Box
          sx={{
            height: "100vh",
            overflowY: "auto",
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, min-max(200px, 1fr))",
            gap: "20px",
            width: "100%",
          }}
        >
          {users.map((user, index) => (
            // <tr key={user.id}>
            // <td>{user.id}</td>
            // <td>{user.name}</td>
            // <td>${user.balance}</td>
            // </tr>
            <ClickableWalletCard key={index} balance={user.balance} />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Home;
