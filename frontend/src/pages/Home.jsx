import SideNav from "../components/SideNav";
import "../esin.css";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CustomSearchBar from "../components/SearchBar";
import ClickableWalletCard from "../components/walletCard";

function Home() {
  // Generate wallet data for 100 users
  const users = Array.from({ length: 100 }, (_, index) => ({
    id: index + 1,
    name: `User ${index + 1}`,
    balance: Math.floor(Math.random() * 1000) + 100, // Generating random balance between 100 and 1099
  }));

  return (
    <Box
      sx={{
        display: "flex",
        overflow: "scroll",
        backgroundColor: "whitesmoke",
      }}
    >
      <SideNav />
      <div
        className="container padding-x-1"
        style={{
          marginTop: "75px",
        }}
      >
        <Stack direction="row" spacing={3} height={"40px"}>
          <CustomSearchBar placeholder="Search wallets" />
          <Button variant="contained" endIcon={<AddIcon />}>
            Add wallet
          </Button>
        </Stack>
        <div className="grid padding-y-1">
          {users.map((user, index) => (
            <ClickableWalletCard
              key={index}
              balance={user.balance}
              id={index.toString()}
            />
          ))}
        </div>
      </div>
    </Box>
  );
}

export default Home;
