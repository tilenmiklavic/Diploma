const { readFileSync, writeFileSync, fstat } = require('fs');

const express = require('express');
const cors = require('cors')
const path = require('path')
const url = require('url')
const fs = require('fs')
const app = express();
const port = process.env.PORT || 5000
const router = express.Router()

app.use(cors())

app.get('/', index)
app.get('/login', login)

function index(req, res) {
    console.log("Index")
    res.send({"greeting": "Hello world-"})
} 

function login(req, res) {
    console.log("Login")
}

// app.get('/', (req, res) => {
//     console.log("Coins data")
//     fs.readFile('coin_data.json', function(err, data) {
//         fs.readFile('results.json', function(err, results) {
//             let coin_data = JSON.parse(data)
//             let results_data = JSON.parse(results)

//             results_data.tweets.forEach(function(el1, ind1) {
//                 coin_data.coins.forEach(function(el2, ind2) {
//                     str1 = el1.name.toLowerCase().replace(/\s/g, '')
//                     str2 = el2.coin.toLowerCase().replace(/\s/g, '')

//                     if (str1 == str2) {
//                         coin_data.coins[ind2].today = el1.tweet
//                     }
//                 })
//             })
//             res.send(coin_data)
//         })
//     })
// });

// app.get('/coins', (req, res) => {
//     console.log("Index")

//     res.send("Hello world")
// })

app.listen(port);
console.log('Server is up and running on port:', port)
console.log('http://localhost:' + port)
