import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Stack from '@mui/material/Stack';
import { CardActionArea } from "@mui/material";
import TokenIcon from '@mui/icons-material/Token';
import PropTypes from "prop-types";
import formatDuration from '../utils';
import React from "react";
import { statusColors } from "../utils";
import { AccessTime } from "@mui/icons-material";
import { API_URI } from "../pages/Home";
import LoadingButton from '@mui/lab/LoadingButton';
import LoopIcon from '@mui/icons-material/Loop';
import { getTradeAmountColor, formatCurrency } from "../utils";


export default function ClickableWalletCard(props) {
  // Ensure the text is long enough to apply the truncation logic
  const text = props.account.walletId;
  const truncatedText = text.length > 7 ? `${text.slice(0, 6)} . . . ${text.slice(-5)}` : text;
  const [isSendingReanalyseRequest, setIsSendingReanalyseRequest] = React.useState(false);

  // Function to handle text copy
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    // Optionally, provide user feedback that text has been copied
  };

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
        console.log(result)
      })
      .catch(error => {
        setAddingNewWallet(false)
      });
  }

  return (
    <div className="container-card shadow-md">
      <CardActionArea className="padding-0" disableRipple={true} style={{
        cursor: "default"
      }}>
        <CardContent
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: "3",
            padding: "5px",
            alignItems: "flex-start"
          }}
        >
          <Stack
            direction={'row'}
            justifyContent={'space-between'}
            alignItems={"center"}
            width={"100%"}
          >
            <a href={`/accounts/${props.account.walletId}`}>
              <Typography 
                gutterBottom
                component="div"
                onClick={handleCopy}
                className={"walletId"}
                variant="body1"
                style={{
                  wordWrap: 'break-word',
                  whiteSpace: 'pre-wrap',
                  cursor: 'pointer',
                  userSelect: 'none',
                  color: "#979797",
                  fontSize: "14px",
                  fontWeight:"bold",
                  backgroundColor: "#80808026",
                  padding: "2px 7px",
                  borderRadius: "6px"
                }}
              >
                {truncatedText}
              </Typography>
            </a>
            <Typography
              gutterBottom
              component="div"
              onClick={handleCopy}
              className={props.account.status === "running" ? "flashingBorder" : ""}
              variant="body1"
              style={{
                color: statusColors[props.account.status][0],
                fontSize: "12px",
                backgroundColor: statusColors[props.account.status][1],
                padding: "0px 3px",
                borderRadius: "5px",
                textAlign:"center"
              }}
            >{props.account.status.toUpperCase()}</Typography>
          </Stack>
          <Stack direction="row" alignItems="space-between">
            <LoadingButton
              size="small"
              onClick={() => {reAnalyse(props.account.walletId)}}
              loading={isSendingReanalyseRequest}
              loadingPosition="end"
              endIcon={<LoopIcon/>}
            >
              <span>Re-analyse</span>
            </LoadingButton>
            <Stack direction="row" spacing={0.2} alignItems={"flex-start"}>
              <AccessTime sx={{color:"grey", height:"20px"}}/>
              <Typography
                gutterBottom
                component="span"
                variant="body1"
                color="grey"
              >{formatDuration(props.account.duration)}</Typography>
            </Stack>
          </Stack>
          <Stack direction="column" className="overviewInfo">
            <Typography variant="span">3M PnL</Typography>
            {props.account.pnl90days === null ? <Typography>-</Typography> : <Typography variant="span" color={getTradeAmountColor(formatCurrency(props.account.pnl90days))}>{formatCurrency(props.account.pnl90days)}</Typography>}
          </Stack>
        </CardContent>
      </CardActionArea>
    </div>
    // </a>f
  );
}
