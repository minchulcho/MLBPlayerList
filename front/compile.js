let fetch = require('node-fetch');
let express = require('express');
let fs = require('fs');

const app = express()


// http://address/name2id?id=33
app.get('/name2id', function (req, res) {
    // let conext; 
    fs.readFile('./data.json', function (err, data) {
        if (data) {
            function valuedFormat(inputValue) {
                inputValue = inputValue.toLowerCase();
                inputValue = inputValue.replace(" ", "");
                return inputValue;
            }
            function getID(playerName, _data) {
                if (playerName === "") {
                    return -3;
                }
                let _id;
                // console.log(playerName);
                for (let i = 0; i < _data.length; i++) {
                    // console.log(valuedFormat(_data[i]["name"]));
                    if (valuedFormat(_data[i]["name"]) === playerName) {
                        _id = _data[i]["id"]
                        return _id;
                    }
                }
                return -1;
            }
            let playerName = valuedFormat(req.query.name);
            let _data = JSON.parse(data.toString())
            res.send({id:getID(playerName, _data)})
        }
    });
    // res.send(req.query.name);
    // console.log(req.query.name );
})


app.get('/listTotal', function (req, res) {
    // let conext; 
    fs.readFile('./data.json', function (err, data) {
        if (data) {

            let _data = JSON.parse(data.toString())
            let totalLength = _data.length
            
            res.send({totalLength: totalLength })
        }
    });
    
})


app.get('/index.js', function (req, res) {
    // let conext; 
    res.setHeader('Content-Type', 'application/js');
    fs.readFile("./mlbWEB/index.js", function (aa, bb) {
        if (aa === null) {
            res.send(bb.toString())
        }
    });
})

app.get('/index.css', async function (req, res) {
    res.setHeader('Content-Type', 'text/css');

    let data = await new Promise(function (resolve, reject) {
        fs.readFile("mlbWEB/index.css", function (error, _data) {
            resolve(_data);
        });
    });

    res.send((data).toString())
})

app.get('/', function (req, res) {
    res.send(fs.readFileSync("mlbWEB/index.html").toString());
})

app.listen(3000)
