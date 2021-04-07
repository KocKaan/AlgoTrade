const axios = require('axios');

const TICKER = 'AAPL'; // enter stock ticker here
const SMA_LENGTH = 25; // number of elements used to calculate SMA

const API_KEY = 'K83K1D6UT8N973SA'

let stockValue = 0;
let usdValue = 10000;
let startingAmount = usdValue;

let orderSize = 1; // for example purposes this is a constant. in a proper system, this should be calculated using kelly criterion

const buy = (price) => {
    if (price*orderSize < usdValue) { // if you have enough money to buy...
        usdValue-=price*orderSize;
        stockValue+=orderSize;
    }
}

const sell = (price) => {
    if (stockValue>0) { // if there are stocks to sell...
        usdValue+=price*orderSize;
        stockValue-=orderSize;
    }
}
const calculateSMA = (data) => {
    let sum = 0;
    for (let i = 0; i < data.length; i++) {
        sum += data[i].close;
    }
    return sum/data.length;
}

const backtest = (response) => {
    const data = Object.entries(response.data['Time Series (Daily)']); // get time series data from response

    // format into an array of objects that is easier to work with
    let candles = [];
    for (let i = 0; i < data.length; i++) {
        candles.push({
            // open: Number(data[i][1]['1. open']),
            // high: Number(data[i][1]['2. high']),
            // low: Number(data[i][1]['3. low']),
            close: Number(data[i][1]['4. close']), // only need close for SMA
            // volume: Number(data[i][1]['5. volume']),
        });
    }

    candles = candles.reverse() // reverse array so it goes from oldest -> newest

    for (let i = 0; i<candles.length; i++) {
        // need to take into account SMA length
        if (i >= SMA_LENGTH) {
            let sma = calculateSMA(candles.slice(i-SMA_LENGTH,i)); // pass the last n candles to calculate SMA
            // buy sell logic
            // console.log(sma, candles[i].close-1, candles[i].close+1);
            if (sma <= candles[i].close-1) {
                buy(candles[i].close);
            } else if (sma >= candles[i].close+1) {
                sell(candles[i].close);
            }
        }
    }

    // log results
    let endBalance = usdValue+stockValue*candles[candles.length-1].close;
    let percentageDiff = Math.round((endBalance-startingAmount)/startingAmount*100);
    console.log(`starting amount:$${startingAmount} end balance:$${endBalance.toFixed(2)}`);
    let buyHoldReturn = Math.round((candles[candles.length-1].close-candles[0].open)/candles[0].open*100);
    console.log(`strategy return: ${percentageDiff}% buy & hold return:${buyHoldReturn}%`);
}

const getDailyCandles = (ticker) => {
    const url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=API_KEY'
    axios.get(url).then(response => backtest(response));
}

getDailyCandles(TICKER)
