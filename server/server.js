const express = require('express');
const config =  require('./config.js');
const fs = require('fs');
const cors = require('cors')
const app = express();
const PythonShell = require('python-shell').PythonShell;
const port = process.env.PORT || 3000
const axios = require('axios');
const moment = require('moment')

app.use(cors())

// ============ ROUTES ======================
app.get('/', index)
app.get('/get', getCoinsData)
app.get('/scrape', scrape)
app.get('/append', append)
// ==========================================

function index(req, res) {
    res.send({"greeting": "Hello world"})
} 

// reading results.json
function readTweetsData() {
    return new Promise((resolve, reject) => {
        fs.readFile('../scraper/results.json', (err, data) => {
            if (err) throw err;
            let student = JSON.parse(data);
            resolve(student)
        }); 
    });
}

// API call for crypto prices
function readCoinsPrice(symbols) {
    return new Promise((resolve, reject) => {
        axios.get(process.env.CMC_URL + 'v2/cryptocurrency/quotes/latest', {
            headers: {
                'X-CMC_PRO_API_KEY': process.env.CMC_API_KEY,
            },
            params: {
                'symbol': symbols.toString()
            }
        })
        .then(response => {
            resolve(response)
        })
        .catch(error => {
            console.error(error.message);
        });
    })
}

function getCoinsData(req, res) {
    readTweetsData()
        .then((result, reject) => {
            readCoinsPrice(result.tweets.map(x => x.symbol))
                .then(coinsPrices => {
                    res.send(coinsPrices.data)
                })
        })
        .catch((error) => {
            console.error(error)
            res.send(false)
        })
}

function scrape(req, res) {
    console.log("Scraping")

    PythonShell.run('../scraper/scraper.py', null, function (err, results) {
        if (err) throw err;   
        res.send(readTweetsData())
    });
}

function appendCoinPrices(prices) {
    let coins = prices.data
    for (const coin in coins) {

        let coin_data = coins[coin][0]
        let data_to_append = {
            "Currency": coin,
            "date": moment().format("YYYY/MM/DD"),
            "price": coin_data.quote.USD.price
        }

        let prices = fs.readFileSync(`../price_data/json_files/price-${coin.toLowerCase()}.json`, {encoding:'utf8', flag:'r'})

        prices = JSON.parse(prices);

        // only write to file if this is the first run today 
        let first_run_today = true;
        for (let price of prices.prices) {
            if (price.date === moment().format("YYYY/MM/DD")) {
                first_run_today = false;
                break;
            }
        }

        if (first_run_today) {
            prices.prices.push(data_to_append)
    
            fs.writeFile(`../price_data/json_files/price-${coin.toLowerCase()}.json`, JSON.stringify(prices), (err) => {
                if (err) {
                    throw err;
                }
                console.log("JSON data is saved.");
            });
        } else {
            console.log("This was not the first run of the day!")
        }
    }

    return(true)
}

function append(req, res) {
    readTweetsData()
        .then((result, reject) => {
            readCoinsPrice(result.tweets.map(x => x.symbol))
                .then(coinsPrices => {
                    res.send(appendCoinPrices(coinsPrices.data))
                })
        })
        .catch((error) => {
            console.error(error)
            res.send(false)
        })
}

function todayDate() {

}

app.listen(config.PORT, config.HOST, () => {
    console.log(`APP LISTENING ON http://${config.HOST}:${config.PORT}`);
})
