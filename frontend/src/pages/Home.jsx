import HomeAppBar from '../components/HomeAppBar';
import SideNav from '../components/SideNav';

import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import Stack from '@mui/material/Stack';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Button, TextField } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CustomSearchBar from '../components/SearchBar';
import ClickableWalletCard from '../components/walletCard';


const Home = () => {
    // Generate wallet data for 100 users
    const users = Array.from({ length: 100 }, (_, index) => ({
        id: index + 1,
        name: `User ${index + 1}`,
        balance: Math.floor(Math.random() * 1000) + 100 // Generating random balance between 100 and 1099
    }));

    return (
        <Box sx={{ display: 'flex' }}>
            
            <SideNav></SideNav>
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Toolbar />
                <Stack direction="row" spacing={3} height={"40px"}>
                    <CustomSearchBar placeholder="Search wallets"></CustomSearchBar>
                    <Button variant='contained' endIcon={<AddIcon></AddIcon>}>Add wallet</Button>
                </Stack>
                <Box sx={{
                    height:"100vh",
                    overflowY:"auto",
                    display: "grid",
                    gridTemplateColumns:"repeat(auto-fill, min-max(200px, 1fr))",
                    gap:"20px",
                    width:"100%"
                }}>
                    {users.map(user => (
                        // <tr key={user.id}>
                        // <td>{user.id}</td>
                        // <td>{user.name}</td>
                        // <td>${user.balance}</td>
                        // </tr>
                        <ClickableWalletCard 
                            balance={user.balance}
                        />
                    ))}
                </Box>
            </Box>
        </Box>
    );
}


export default Home;
