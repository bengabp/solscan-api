import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Card from '@mui/material/Card'
import CardActionArea from '@mui/material/CardActionArea';
import List from '@mui/material/List'
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Tooltip from '@mui/material/Tooltip';
import Avatar from '@mui/material/Avatar';
import {getTradeAmountColor, formatCurrency} from '../utils';


export default function TokenChangeTable(props) {
  return (
    <TableContainer component={Paper}>
        <Table sx={{overflowX:"auto" }} aria-label="simple table" component="div">
            <TableHead component="div">
                <TableRow component={"div"}>
                    <TableCell align="left" component="div">Token</TableCell>
                    <TableCell align="right" component="div">Balance Change</TableCell>
                    <TableCell align="right" component="div">Price</TableCell>
                    <TableCell align="right" component="div">Value</TableCell>
                </TableRow>
            </TableHead>
            <TableBody component="div">
                {props.rows.map((row, index) => (
                    <TableRow key={index} component="div" className="tokenTableRow" onClick={() => {
                        console.log(props.currentTokenData)
                        props.setCurrentTokenData(props.tokens[row.mint] || {})
                    }}>
                        <TableCell scope="row" align="left" component="div">
                            <Stack direction="row" spacing={1}>
                                <Tooltip placement="right" title={row.symbol}>
                                    <Avatar
                                        alt={row.symbol}
                                        src={row.icon}
                                        style={{ width: '20px', height: '20px', cursor: 'pointer' }}
                                    />
                                </Tooltip>
                                <a className="textButton" target='_blank' href={`https://birdeye.so/token/${row.mint}`}>{row.symbol}</a>
                            </Stack>
                        </TableCell>
                        <TableCell component="div" align="right" sx={{color:getTradeAmountColor(row.uiAmount)}}>{(row.uiAmount)}</TableCell>
                        <TableCell component="div" align="right">${row.price}</TableCell>
                        <TableCell component="div" align="right" sx={{color:getTradeAmountColor(row.value)}}>{formatCurrency(row.value)}</TableCell>
                    </TableRow>
                ))}
            </TableBody>
      </Table>
    </TableContainer>
  );
}