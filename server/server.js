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

// reading coins.json
// function readCoinsData() {
//     return new Promise((resolve, reject) => {
//         fs.readFile('coins.json', (err, data) => {
//             if (err) throw err;
//             let coins = JSON.parse(data);
//             resolve(coins)
//         }); 
//     });
// }

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
            console.log(response)
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
            console.log(result)
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

app.listen(config.PORT, config.HOST, () => {
    console.log(`APP LISTENING ON http://${config.HOST}:${config.PORT}`);
})
