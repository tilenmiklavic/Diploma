const express = require('express');
const config =  require('./config.js');
const fs = require('fs');
const cors = require('cors')
const app = express();
const PythonShell = require('python-shell').PythonShell;
const port = process.env.PORT || 3000
const axios = require('axios');

app.use(cors())

// ============ ROUTES ======================
app.get('/', index)
app.get('/get', getCoinsData)
app.get('/scrape', scrape)
// ==========================================

function index(req, res) {
    console.log("Index")
    res.send({"greeting": "Hello world-"})
} 

var readCoinsData = new Promise((resolve, reject) => {
    fs.readFile('results.json', (err, data) => {
        if (err) throw err;
        let student = JSON.parse(data);
        resolve(student)
    }); 
})

// API call for crypto prices
function readCoinsPrice(symbols) {
    return new Promise((resolve, reject) => {
        axios.get('https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest', {
            headers: {
                'X-CMC_PRO_API_KEY': 'd1d493de-64d8-4aa1-8373-0e7155b638a1',
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
    readCoinsData
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
        res.send(readCoinsData)
    });
}

app.listen(config.PORT, config.HOST, () => {
    console.log(`APP LISTENING ON http://${config.HOST}:${config.PORT}`);
})
