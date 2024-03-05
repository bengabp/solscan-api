import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";
import PropTypes from "prop-types";

export default function ClickableWalletCard(props) {
  // Ensure the text is long enough to apply the truncation logic
  const text = props.account.walletId;
  const truncatedText = text.length > 7 ? `${text.slice(0, 3)}...${text.slice(-4)}` : text;

  // Function to handle text copy
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    // Optionally, provide user feedback that text has been copied
  };

  return (
    <a
      href={`/accounts/${props.id}`}
      style={{
        color: "black",
      }}
    >
      <div className="container-card shadow-md">
        <CardActionArea className="padding-1">
          <CardContent>
            <Typography 
              gutterBottom
              component="div"
              onClick={handleCopy}
              variant="body1"
              style={{
                wordWrap: 'break-word',
                whiteSpace: 'pre-wrap',
                cursor: 'pointer',
                userSelect: 'none',
                fontWeight: 'bold',
              }}
            >
              {truncatedText}
            </Typography>
          </CardContent>
        </CardActionArea>
      </div>
    </a>
  );
}
