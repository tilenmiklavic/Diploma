const { readFileSync, writeFileSync } = require('fs');

const express = require('express');
const path = require('path')
const app = express();
const port = process.env.PORT || 4000

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/homepage.html'))
});

app.listen(port);
console.log('Server is up and running on port:', port)
console.log('http://localhost:' + port)