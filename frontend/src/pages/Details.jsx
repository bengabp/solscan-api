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
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from "@mui/material/Button";
import Paper from '@mui/material/Paper';
import TokenChangeTable from '../components/TokenChangeTable';
import LoopIcon from '@mui/icons-material/Loop';
import LoadingButton from '@mui/lab/LoadingButton';
import AccessTime from '@mui/icons-material/AccessTimeFilled';
import { statusColors } from "../utils";
import { getTradeAmountColor, formatCurrency } from "../utils";




function formatNumberWithCommas(number) {
  // Format the number with commas for thousands separators
  if (number === undefined || number  === null){
    return "-"
  }
  const formattedNumber = Number(number).toLocaleString('en-US');
  return formattedNumber;
}

export default function DetailedPage(props) {
  // Page ID
  const { id } = useParams();
  const navigation = useNavigate();
  const overviewLabelMappings = {
    "Yesterday":"tradeYesterday",
    "Today":"tradeToday",
    "1W":"trade7d",
    "1M":"trade30d",
    "2M":"trade60d",
    "3M":"trade90d"
  }
  const [data, setData] = React.useState({});
  const [currentTokenData, setCurrentTokenData] = React.useState({})
  const [currentOverviewLabel, setCurrentOverviewLabel] = React.useState("Today")
  const [currentOverviewData, setCurrentOverviewData] = React.useState(data[overviewLabelMappings[currentOverviewLabel]]);
  const [isSendingReanalyseRequest, setIsSendingReanalyseRequest] = React.useState(false);
  
  function goback() {
    navigation(-1);
  }


  React.useEffect(() => {
    props.setIsLoading(true)
    updateWalletData()
  }, []);

  const updateWalletData = () => {
    fetch(`${API_URI}/wallets/${id}`)
      .then(response => response.json())
      .then(data => {
        setData(data);
        setCurrentOverviewData(data[overviewLabelMappings[currentOverviewLabel]])
      })
      .catch(error => {
      })
      .finally( ()=>{
        props.setIsLoading(false);
      })
  }
  const reAnalyse = (walletId) => {
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

    setIsSendingReanalyseRequest(true)
    fetch(`${API_URI}/track`, requestOptions)
      .then(response => response.json())
      .then(result => {
        setIsSendingReanalyseRequest(false)
        updateWalletData()
      })
      .catch(error => {
        setAddingNewWallet(false)
      });
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
      {data.status !== undefined && <Stack width="100%" padding={2} direction="row" spacing={2} alignItems={"center"}>
        <IconButton onClick={goback}>
          <ChevronLeftIcon></ChevronLeftIcon>
        </IconButton>
        <Typography
            gutterBottom
            component="div"
            variant="h4"
            align="left"
            style={{
              color: "grey"
            }}
        >Overview</Typography>
        <LoadingButton
          size="small"
          onClick={() => {reAnalyse(data.walletId)}}
          loading={isSendingReanalyseRequest}
          loadingPosition="end"
          endIcon={<LoopIcon/>}
          variant="contained"
        >
          <span>Re-analyse</span>
        </LoadingButton>
        <Typography
          gutterBottom
          component="div"
          className={data.status === "running" ? "flashingBorder" : ""}
          variant="body1"
          style={{
            color: statusColors[data.status][0],
            fontSize: "12px",
            backgroundColor: statusColors[data.status][1],
            padding: "0px 3px",
            borderRadius: "5px",
            textAlign:"center"
          }}
        >{data.status.toUpperCase()}</Typography>
      </Stack>}
      {data.status !== undefined && <Stack width="100%" padding={2} direction="row" spacing={2} alignItems={"center"}>
        <Typography
          gutterBottom
          component="div"
          variant="h5"
          style={{
            color: "grey"
          }}
        >Wallet</Typography>
        <Typography
          gutterBottom
          component="span"
          variant="body1"
          fontStyle={"italic"}
          style={{
            color: "grey",
            fontSize: "16px",
          }}
        >{id}</Typography>
        <IconButton onClick={() => {navigator.clipboard.writeText(id);}}>
          <ContentCopyIcon></ContentCopyIcon>
        </IconButton>
      </Stack>}
      {data.status !== undefined && <Stack direction="row" justifyContent={"flex-end"}>
        <ButtonGroup variant="outlined" aria-label="overviewSwitch">
          {
            Object.keys(overviewLabelMappings).map((item, index) => <Button sx={{
              textTransform:"none"
              }} variant={currentOverviewLabel == item ? "contained": "outlined"}
              key={index}
              onClick={() => {
                console.log(currentOverviewData)
                setCurrentOverviewLabel(item);
                setCurrentOverviewData(data[overviewLabelMappings[item]])
              }}
            >{item}</Button>)
          }
        </ButtonGroup>
      </Stack>}
      {currentOverviewData !== undefined && <Stack
        direction="column"
        spacing={1}
        sx={{
          overflow:"hidden",
          height: "100%",
          width: "100%",
        }}
      >
        <Stack direction="row" width="max-content" padding={2} spacing={3}
          sx={{
            backgroundColor:"#80808026",
            paddingX:"30px"
          }}
        >
          <Stack direction="column" className="overviewInfo">
            <Typography variant="span">{currentOverviewLabel} PnL</Typography>
            <Typography variant="span" color={getTradeAmountColor(formatCurrency(currentOverviewData.pnl))}>{formatCurrency(currentOverviewData.pnl)}</Typography>
          </Stack>
          <Stack direction="column" className="overviewInfo">
            <Typography variant="span">{currentOverviewLabel} volume</Typography>
            <Typography variant="span" color={getTradeAmountColor(formatCurrency(currentOverviewData.volume))}>{formatCurrency(currentOverviewData.volume)}</Typography>
          </Stack>
          <Stack direction="column" className="overviewInfo">
            <Typography variant="span">{currentOverviewLabel} trades</Typography>
            <Typography variant="span" fontWeight={"bold"} color="#555353">{formatNumberWithCommas(currentOverviewData.tradeCount)}</Typography>
          </Stack>
        </Stack>
        <Stack direction="row" width="100%" overflow="hidden">
          <Stack direction="column" sx={{
            height:"100%",
            width:"50%",
            overflowY:"auto"
          }}>
            <TokenChangeTable 
              rows={currentOverviewData.tokenChange}
              tokens={data.tokensDexData || {}}
              setCurrentTokenData={setCurrentTokenData}
              currentTokenData={currentTokenData}
            ></TokenChangeTable>
          </Stack>
          <Stack direction="column" sx={{
            height:"100%",
            width:"50%",
            overflowY:"auto"
          }}>
            {Object.keys(currentTokenData).length > 1 && 
              <Stack direction="row" width="100%" className="tokenFieldsCnt" padding={1} flexWrap={"wrap"} spacing={1} rowGap={1}>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">PNL</Typography>
                  <Typography variant="body1">{currentTokenData.pnl}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Bought Coin</Typography>
                  <Typography variant="body1">{currentTokenData.amountBuy}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Sold Coin</Typography>
                  <Typography variant="body1">{currentTokenData.amountSell}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Sold USD</Typography>
                  <Typography variant="body1">${formatNumberWithCommas(currentTokenData.volumeUsdSell)}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Bought USD</Typography>
                  <Typography variant="body1">${formatNumberWithCommas(currentTokenData.volumeUsdBuy)}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">TNX Sell</Typography>
                  <Typography variant="body1">{currentTokenData.sells}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">TNX Buy</Typography>
                  <Typography variant="body1">{currentTokenData.buys}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Unrealized PnL</Typography>
                  <Typography variant="body1">{currentTokenData.balanceAmount}</Typography>
                </Stack>
                <Stack className="tokenFieldCnt">
                  <Typography variant="body1">Balance Percentage</Typography>
                  <Typography variant="body1">{currentTokenData.balancePercentage}</Typography>
                </Stack>
              </Stack>
            }
          </Stack>
        </Stack>
      </Stack>}
    </Container>
  );
}
