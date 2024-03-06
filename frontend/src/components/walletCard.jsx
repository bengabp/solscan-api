import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";
import PropTypes from "prop-types";

export default function ClickableWalletCard(props) {
  // Ensure the text is long enough to apply the truncation logic
  const text = props.account.walletId;
  const truncatedText = text.length > 7 ? `${text.slice(0, 6)} . . . ${text.slice(-5)}` : text;

  // Function to handle text copy
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    // Optionally, provide user feedback that text has been copied
  };

  return (
    // <a
    //   href={`/accounts/${props.id}`}
    //   style={{
    //     color: "#979797",
    //   }}
    // >
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
          <a href={`/accounts/${props.id}`}>
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
          <div sx={{
            display: "flex",
            flexDirection: "row"
          }}>
            <Typography className="label text-small">Tokens traded last 7 days</Typography>
            <Typography className="text-small">{props.account.tokensTradedList.length}</Typography>
          </div>
        </CardContent>
      </CardActionArea>
    </div>
    // </a>
  );
}
