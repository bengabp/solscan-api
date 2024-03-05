import SideNav from "../components/SideNav";
import "../esin.css";
import React from 'react';
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CustomSearchBar from "../components/SearchBar";
import ClickableWalletCard from "../components/walletCard";

function Home(props) {
  // Generate wallet data for 100 users

  const [data, setData] = React.useState([]);
  const API_URI = "http://localhost:8070";
  const [inputWalletAddress, setInputWalletAddress] = React.useState("");
  const [addingNewWallet, setAddingNewWallet] = React.useState(false);

  React.useEffect(() => {
    fetch(`${API_URI}/wallets`)
      .then(response => response.json())
      .then(data => {
        setData(data);
        props.setIsLoading(false);
        console.log(data);
      })
      .catch(error => {
        props.setIsLoading(false);
      });
  }, []);

  const create_task = (walletId) => {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      "walletId": walletId
    });

    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    setAddingNewWallet(true)
    fetch(`${API_URI}/track`, requestOptions)
      .then(response => response.json())
      .then(result => {
        setAddingNewWallet(false)
        console.log(result)
      })
      .catch(error => {
        setAddingNewWallet(false)
      });
  }

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
          <CustomSearchBar 
            placeholder="Search wallets" 
            onChange={(newVal) => {setInputWalletAddress(newVal)}} 
            addingNewWallet={addingNewWallet}
            setAddingNewWallet={setAddingNewWallet}
          />
          <Button 
            variant="contained" 
            endIcon={!addingNewWallet && <AddIcon />}
            disabled={addingNewWallet ? true : false}
            onClick={() => {
              create_task(inputWalletAddress)
            }}
          >
            {addingNewWallet ? "Adding ..." : "Add wallet"}
          </Button>
        </Stack>
        <div className="grid padding-y-1">
          {data.map((account, index) => (
            <ClickableWalletCard
              key={index}
              balance={account.walletId}
              id={account.walletId}
              account={account}
            />
          ))}
        </div>
      </div>
    </Box>
  );
}

export default Home;
