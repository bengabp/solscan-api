import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';

function convertUTCtoLocal(timestamp) {
  const utcDate = new Date(timestamp);
  const offset = utcDate.getTimezoneOffset();
  const localDate = new Date(utcDate.getTime() - (offset * 60 * 1000));

  // Define months as abbreviations
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  // Format the local date-time string
  const month = months[localDate.getMonth()];
  const day = localDate.getDate();
  const year = localDate.getFullYear();
  const hours = String(localDate.getHours()).padStart(2, '0');
  const minutes = String(localDate.getMinutes()).padStart(2, '0');
  const seconds = String(localDate.getSeconds()).padStart(2, '0');

  return `${month} ${day}, ${year} ${hours}:${minutes}:${seconds}`;
}



export default function TransactionHistoryTable(props) {
  const columns = [
    { id: 'blockTimestamp', label: 'DATE', minWidth: 100 },
    {
      id: 'logType',
      label: 'TYPE',
      minWidth: 170,
      align: 'right'
    },
    {
      id: 'amount0',
      label: props.pair.toUpperCase(),
      minWidth: 170,
      align: 'right',
    },
    {
      id: 'amount1',
      label: "SOL",
      minWidth: 170,
      align: 'right',
    },
    {
      id: 'volumeUsd',
      label: "USD",
      minWidth: 170,
      align: 'right',
    },
    {
      id: 'priceUsd',
      label: "PRICE",
      minWidth: 170,
      align: 'right',
      suffix:"$"
    },
  ];

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{
                    minWidth:"100px",
                    maxWidth:"200px"
                  }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {props.transactionLogs
              .map((row) => {
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={row._id}>
                    {columns.map((column) => {
                      const value = row[column.id];
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.id === "blockTimestamp" ? convertUTCtoLocal(value) : value}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}