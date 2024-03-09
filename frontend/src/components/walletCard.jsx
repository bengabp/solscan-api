import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Stack from '@mui/material/Stack';
import { CardActionArea } from "@mui/material";
import TokenIcon from '@mui/icons-material/Token';
import PropTypes from "prop-types";

export default function ClickableWalletCard(props) {
  // Ensure the text is long enough to apply the truncation logic
  const text = props.account.walletId;
  const truncatedText = text.length > 7 ? `${text.slice(0, 6)} . . . ${text.slice(-5)}` : text;
  const statusColors = {
    queued: ['#555', '#eee'],        // Greyish text on Light Grey background
    running: ['#FFD700', '#FFFFE0'], // Yellow text on Light Yellow background
    completed: ['#008000', '#F0FFF0'], // Green text on Honeydew background
  };
  // Function to handle text copy
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    // Optionally, provide user feedback that text has been copied
  };

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
              className={props.account.status === "running" && "flashingBorder"}
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
          {/* <Stack direction="row">
            <Stack direction={'row'} spacing={0.5} paddingRight={1}>
              <TokenIcon htmlColor={"#1976d2b8"}></TokenIcon>
              <Typography className="textSmall" color={"#1976d2b8"}>{props.account.tokensTradedList.length}</Typography>
            </Stack>
          </Stack> */}
        </CardContent>
      </CardActionArea>
    </div>
    // </a>f
  );
}
