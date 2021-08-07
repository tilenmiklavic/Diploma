const { readFileSync, writeFileSync, fstat } = require('fs');

const express = require('express');
const path = require('path')
const url = require('url')
const fs = require('fs')
const app = express();
const handlebars = require('express-handlebars')
const port = process.env.PORT || 4000

app.engine('hbs', handlebars({
    defaultLayout: 'main',
    extname: '.hbs'
}))
app.set('view engine', 'hbs');
app.use(express.static(__dirname + '/views'))

app.get('/', (req, res) => {
    fs.readFile('coin_data.json', function(err, data) {
        fs.readFile('results.json', function(err, results) {
            let coin_data = JSON.parse(data)
            let results_data = JSON.parse(results)

            results_data.tweets.forEach(function(el1, ind1) {
                coin_data.coins.forEach(function(el2, ind2) {
                    str1 = el1.name.toLowerCase().replace(/\s/g, '')
                    str2 = el2.coin.toLowerCase().replace(/\s/g, '')

                    if (str1 == str2) {
                        coin_data.coins[ind2].today = el1.tweet
                    }
                })
            })
            console.log(coin_data)
            res.render('home', {
                title: "Diploma",
                coins: coin_data.coins
            });
        })
    })
});

app.listen(port);
console.log('Server is up and running on port:', port)
console.log('http://localhost:' + port)