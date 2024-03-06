import React from "react";
import "../esin.css";
import { useNavigate, useNavigation, useParams } from "react-router-dom";
import { KeyboardArrowLeft as BackIcon } from "@mui/icons-material";
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import IconButton from "@mui/material/IconButton";
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import {API_URI} from "./Home";
import Avatar from '@mui/material/Avatar';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import Tooltip from '@mui/material/Tooltip';

export default function DetailedPage(props) {
  // Page ID
  const { id } = useParams();
  const navigation = useNavigate();
  const [data, setData] = React.useState({});

  function goback() {
    navigation(-1);
  }

  const [currentToken, setCurrentToken] = React.useState({})

  React.useEffect(() => {
    props.setIsLoading(true)
    fetch(`${API_URI}/wallets/${id}`)
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

  const viewTokenInfo = () => {
    
  }

  return (
    <Container className="bg-white mt-4"
      sx={{
        heigth:"100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        overflowY:"hidden"
      }}
    >
      <Stack width="100%" padding={2} direction="row" spacing={2} alignItems={"center"}>
        <IconButton onClick={goback}>
          <ChevronLeftIcon></ChevronLeftIcon>
        </IconButton>
        
        <Typography
          gutterBottom
          component="div"
          variant="body1"
          fontWeight="bold"
          style={{
            color: "grey",
            fontSize: "16px",
          }}
        >{id}</Typography>
        <IconButton onClick={() => {navigator.clipboard.writeText(id);}}>
          <ContentCopyIcon></ContentCopyIcon>
        </IconButton>

      </Stack>
      <Stack
        direction="column"
        spacing={1}
        sx={{
          overflow:"hidden",
          height: "100%",
          width: "100%",
        }}
      >
        
        {data?.tokensTradedData && 
        <Stack direction="row" sx={{
          height:"100%",
        }} padding={1}>
          <Stack spacing={1} padding={1}
            sx={{
              height:"100%",
              overflowY:"auto",
              overflowX:"hidden"
            }}
          >
            {data.tokensTradedData.map((tokenTradeData, index) => (
              <Tooltip placement="right" title={tokenTradeData.symbol}>
                <Avatar
                  alt={tokenTradeData.symbol}
                  src={tokenTradeData.logo}
                  style={{ width: '50px', height: '50px', cursor: 'pointer' }}
                  onClick={() => {
                    console.log(tokenTradeData)
                    setCurrentToken(tokenTradeData)
                  }}
                />
              </Tooltip>
            ))}
          </Stack>
          {
            currentToken?.logo 
            ? 
              <Stack>Something</Stack> 
            : 
              <Box
                sx={{
                  display:"flex",
                  flexDirection:"column",
                  width:"100%",
                  alignItems:"center",
                  justifyContent:"center"
                }}
              >
                <Typography align="center" variant="h6">Click on a token to view details</Typography>
              </Box>
          }
        </Stack>}
      </Stack>
    </Container>
  );
}
