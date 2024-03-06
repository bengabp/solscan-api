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
import { withTheme } from "@emotion/react";
import TransactionHistoryTable from '../components/TransactionHistoryTable';
import Divider from '@mui/material/Divider';

function formatValue(input) {
  if (input === null) {
    return '-';
  }
  if (typeof input === 'string') {
    input = parseFloat(input);
  }
  if (isNaN(input)) {
    return input.toString();
  }
  const suffixes = ['', 'K', 'M', 'B', 'T'];
  let suffixIndex = 0;
  while (input >= 1000 && suffixIndex < suffixes.length - 1) {
    input /= 1000;
    suffixIndex++;
  }
  input = Math.round(input * 10) / 10;
  return input.toString() + suffixes[suffixIndex];
}



export default function DetailedPage(props) {
  // Page ID
  const { id } = useParams();
  const navigation = useNavigate();
  const [data, setData] = React.useState({});

  const attributes = [
    "symbol",
    "buys",
    "sells",
    "volumeUsdSell",
    "volumeUsdBuy",
    "balanceAmount",
    "amountSell",
    "amountBuy",
    "balancePercentage"
  ]

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
          variant="h5"
          fontWeight="bold"
          style={{
            color: "grey"
          }}
        >Wallet</Typography>
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
                <div className={currentToken?.symbol === tokenTradeData.symbol && 
                    "tokenActive"}>
                  <Avatar
                    alt={tokenTradeData.symbol}
                    src={tokenTradeData.logo}
                    style={{ width: '50px', height: '50px', cursor: 'pointer' }}
                    onClick={() => {
                      console.log(tokenTradeData)
                      setCurrentToken(tokenTradeData)
                    }}
                  />
                </div>
              </Tooltip>
            ))}
          </Stack>
          {
            currentToken?.logo 
            ? 
              <Stack direction="column" spacing={0.5} padding={2} sx={{
                height:"100%",
                overflowY:"auto",
                width: "100%"
              }}>
                <Stack direction="row" alignItems="center" spacing={3}>
                  <Typography color={"#1976d2eb"} fontWeight={"bold"} >Address</Typography>
                  <Stack direction="row" alignItems="center" spacing={1} paddingTop={1}>
                    <Typography
                      component="span"
                      variant="body1"
                      fontStyle="italic"
                      style={{
                        color: "grey",
                        fontSize: "16px",
                      }}
                    >{currentToken.address}</Typography>
                    <IconButton onClick={() => {navigator.clipboard.writeText(currentToken.address);}}>
                      <ContentCopyIcon></ContentCopyIcon>
                    </IconButton>
                  </Stack>
                </Stack>
                <Box
                  sx={{
                    display:"flex",
                    flexWrap:"wrap",
                    columnGap: "15px",
                    rowGap:"5px"
                  }}
                >
                  {attributes.map(attribute => (
                    <Stack direction="row" spacing={1}
                      sx={{
                        padding: "3px 8px",
                        borderRadius: "5px",
                        backgroundColor: "#009aff1c",
                        // border:"1px solid #2135470d"
                      }}
                    >
                      <Typography color={"#1976d2eb"}>{attribute}</Typography>
                      <Typography
                        component="span"
                        variant="body1"
                        style={{
                          fontSize: "15px"
                        }}
                      >{attribute === "symbol" ? currentToken[attribute] : formatValue(currentToken[attribute])}</Typography>
                    </Stack>
                  ))}
                </Box>
                <Stack paddingTop={2} spacing={1}>
                  <Stack direction="row" spacing={1}>
                    <Typography 
                      align="left" 
                      variant="h5"
                      fontWeight={"bold"}
                    >{currentToken.transactionLogs.length}</Typography>
                    <Typography align="left" variant="h6">{currentToken.transactionLogs.length === 1 ? "transaction in the last 7 days" : "transactions in the last 7 days"}</Typography>
                  </Stack>
                  <TransactionHistoryTable pair={currentToken.symbol} transactionLogs={currentToken.transactionLogs}></TransactionHistoryTable>
                </Stack>
              </Stack> 
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
                {
                  data.tokensTradedList.length > 0 ?
                  <Typography align="center" variant="h6">Click on a token to view details</Typography>:
                  <Typography align="center" variant="h6">No trade data is available for this wallet currently ...</Typography>
                }
              </Box>
          }
        </Stack>}
      </Stack>
    </Container>
  );
}
