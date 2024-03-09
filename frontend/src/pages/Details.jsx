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

export function getTradeAmountColor(value) {
  if (value === null || value === '-') {
    return 'gray';
  } else if (value.startsWith('-')) {
    return 'red';
  } else {
    return 'green';
  }
}


export function formatCurrency(number) {
  // Convert the number to a string with 2 decimal places and add commas for thousands separators
  const formattedNumber = Math.abs(number).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });

  // Prepend a negative sign if the number is negative
  const negativeSign = number < 0 ? '-' : '';

  // Format the number as a currency string with the dollar sign
  const currencyString = `${negativeSign}$${formattedNumber}`;

  return currencyString;
}



function formatNumberWithCommas(number) {
  // Format the number with commas for thousands separators
  const formattedNumber = Number(number).toLocaleString('en-US');
  return formattedNumber;
}

export default function DetailedPage(props) {
  // Page ID
  const { id } = useParams();
  const navigation = useNavigate();
  const [data, setData] = React.useState({});

  const overviewLabelMappings = {
    "Yesterday":"tradeYesterday",
    "Today":"tradeToday",
    "1W":"trade7d",
    "1M":"trade30d",
    "2M":"trade60d",
    "3M":"trade90d"
  }
  
  
  const [currentOverviewLabel, setCurrentOverviewLabel] = React.useState("Today")
  const [currentOverviewData, setCurrentOverviewData] = React.useState(data[overviewLabelMappings[currentOverviewLabel]]);

  function goback() {
    navigation(-1);
  }

  const [currentTokenData, setCurrentTokenData] = React.useState({})

  React.useEffect(() => {
    props.setIsLoading(true)
    fetch(`${API_URI}/wallets/${id}`)
      .then(response => response.json())
      .then(data => {
        setData(data);
        props.setIsLoading(false);
        setCurrentOverviewData(data[overviewLabelMappings[currentOverviewLabel]])
      })
      .catch(error => {
        props.setIsLoading(false);
      });
  }, []);

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
            variant="h4"
            align="left"
            style={{
              color: "grey"
            }}
          >Overview</Typography>
      </Stack>
      <Stack width="100%" padding={2} direction="row" spacing={2} alignItems={"center"}>
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
      </Stack>
      <Stack direction="row" justifyContent={"flex-end"}>
        <ButtonGroup variant="outlined" aria-label="overviewSwitch">
          {
            Object.keys(overviewLabelMappings).map((item, index) => <Button sx={{
              textTransform:"none"
              }} variant={currentOverviewLabel == item ? "contained": "outlined"}
              onClick={() => {
                console.log(currentOverviewData)
                setCurrentOverviewLabel(item);
                setCurrentOverviewData(data[overviewLabelMappings[item]])
              }}
            >{item}</Button>)
          }
        </ButtonGroup>
      </Stack>
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
            {currentTokenData && 
              <Stack direction="column">
                <Typography
                  gutterBottom
                  component="div"
                  variant="h4"
                  align="left"
                  style={{
                    color: "grey"
                  }}
                >{currentTokenData.name}</Typography>
              </Stack>
            }
          </Stack>
        </Stack>
      </Stack>}
    </Container>
  );
}
