import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";
import PropTypes from "prop-types";

export default function ClickableWalletCard({ id, balance }) {
  return (
    <a
      href={`/accounts/${id}`}
      style={{
        color: "black",
      }}
    >
      <div className="container-card shadow-md">
        <CardActionArea className="padding-1">
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              Lizard
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Lizards are a widespread group of squamate reptiles, with over
              6,000 species, ranging across all continents except Antarctica
            </Typography>
          </CardContent>
        </CardActionArea>
      </div>
    </a>
  );
}

ClickableWalletCard.propTypes = {
  id: PropTypes.string.isRequired,
  balance: PropTypes.number.isRequired,
};
