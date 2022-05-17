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
app.get('/getTweets', getTweetsData)
app.get('/scrape', scrape)
app.get('/append', append)
app.get('/normalize', normalize)
// ==========================================

function index(req, res) {
    res.send({"greeting": "Hello world"})
} 

// ============ FILE HANDLING ============ // 

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

// adds todays coin prices to the file 
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

// ============ END FILE HANDLING ============ // 

// ============ API COMMUNICATION ============ // 

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

// scrape internet for number of tweets today
function scrape() {
    return new Promise((resolve, reject) => {
        console.log("Scraping")
    
        PythonShell.run('../scraper/scraper.py', null, function (err, results) {
            if (err) reject();   
            resolve(true)
        });
    })
}

// normalizes data from prices and tweets
function normalize(req, res) {
    return new Promise((resolve, reject) => {
        console.log("Normalizing")
    
        PythonShell.run('../normalizer/normalizer.py', null, function (err, results) {
            if (err) reject();   
            resolve(true)
        });
    })
}

// ============ END API COMMUNICATION ============ // 

// ============ HTTP ENDPOINTS ============ // 

// get all info about coins 
// that includes prices and tweets
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
        .finally(() => {
            append();
        })
}

function getTweetsData(req, res) {
    readTweetsData()
        .then(odgovor => {

            console.log(odgovor)
            console.log(todayDate())

            if (odgovor.date === todayDate()) {
                res.send(odgovor)
            } else {
                scrape()
                    .then(odgovor => {
                        readTweetsData()
                            .then(data => {
                                res.send(data)
                            })
                    })
            }
        })
}

// function for appending data
function append() {
    readTweetsData()
        .then((result, reject) => {
            readCoinsPrice(result.tweets.map(x => x.symbol))
                .then(coinsPrices => {
                    return(appendCoinPrices(coinsPrices.data))
                })
        })
        .catch((error) => {
            console.error(error)
            res.send(false)
        })
}

// ============ END HTTP ENDPOINTS ============ // 

// ============ UTILITIED ============ // 

function todayDate() {
    let date = new Date();
    let day = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate()
    let month = date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1
    let rezultatDate = `${date.getFullYear()}/${month}/${day}`

    return rezultatDate
}
// ============ END UTILITIES ============ // 


app.listen(config.PORT, config.HOST, () => {
    console.log(`APP LISTENING ON http://${config.HOST}:${config.PORT}`);
})
