
export default function formatDuration(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    let result = '';
    if (days > 0) {
        result = days + 'd';
    } else if (hours > 0) {
        result = hours + 'h';
    } else if (minutes > 0) {
        result = minutes + 'm';
    } else {
        result = (seconds % 60).toFixed(1) + 's'; // If seconds is the highest duration unit, round to one decimal point
    }

    return result;
}

export const statusColors = {
    queued: ['#555', '#eee'],        // Greyish text on Light Grey background
    running: ['#FFD700', '#FFFFE0'], // Yellow text on Light Yellow background
    completed: ['#008000', '#F0FFF0'], // Green text on Honeydew background
    failed: ["red", "#bc202036"]
};

export const delayedCall = async (func, delay) => {
    await sleep(delay); // Sleep for 2 seconds
    func();
  };

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export function getTradeAmountColor(value) {
    if (value === null || value === '-' || value === undefined) {
      return 'gray';
    } else if (value.toString().startsWith('-')) {
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
  const negativeSign = number < 0 ? '-' : '';
  const currencyString = `${negativeSign}$${formattedNumber}`;
  return currencyString;
}

