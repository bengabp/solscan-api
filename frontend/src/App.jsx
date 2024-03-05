import { useState } from "react";
import "./App.css";
import "./styles/Main.css";
import { createTheme, ThemeProvider, Stack, Box } from "@mui/material";
import HomeAppBar from "./components/HomeAppBar";
import SideNav from "./components/SideNav";
import Home from "./pages/Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CssBaseline from "@mui/material/CssBaseline";
import DetailedPage from "./pages/Details";

const theme = createTheme({
  typography: {
    fontSize: 12,
  },
});

const App = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState("home");

  // const pageNavigation

  return (
    <BrowserRouter>
      <CssBaseline />
      <Stack
        direction="column"
        sx={{
          width: "100%",
        }}
      >
        <HomeAppBar />
        <Routes>
          <Route index element={<Home />} />
          <Route path="/accounts/:id" Component={DetailedPage} />
        </Routes>
      </Stack>
    </BrowserRouter>
  );
};

export default App;
