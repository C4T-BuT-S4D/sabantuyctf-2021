const express = require('express'); // ^4.17.1"
const Sequelize = require('sequelize'); // ^4.6.5
const crypto = require("crypto"); //
const session = require('express-session'); // ^1.17.2
const bodyParser = require('body-parser') // ^1.19.0
const jsonParser = bodyParser.json()

const connection = new Sequelize('sqlite:///storage.db');

const Employee = connection.define('employees', {
    username: Sequelize.STRING,
    password: Sequelize.STRING,
    email: Sequelize.STRING,
    isVaccinated: Sequelize.BOOLEAN,
}, {
    timestamps: false,
});

connection.sync().then(() => {
    console.log("SYNCED");
})

const app = express();

app.use(session({
    resave: false, // don't save session if unmodified
    saveUninitialized: false, // don't create session until something stored
    secret: '********************' // secret removed
}));

app.use(express.static('public'));

app.get('/api/captcha', (req, res) => {
    let prefix = crypto.randomBytes(4).toString("hex");
    if (req.session.captcha) {
        prefix = req.session.captcha;
    }
    req.session.captcha = prefix;
    res.json({prefix: prefix});
});

app.post('/api/captcha', jsonParser, (req, res) => {
    if (req.session.captcha) {
        let hash = crypto.createHash('md5').update(req.session.captcha + req.body.answer).digest('hex');
        if (hash.startsWith('0000')) {
            req.session.captchaSolved = true;
            res.json({solved: true});
        } else {
            res.json({solved: false});
        }
    } else {
        res.status(400).send('no captcha found, go get /api/captcha')
    }
});

app.get('/api/employees', (req, res) => {
    if (req.session.captchaSolved !== true) {
        res.status(401).send('no solved captcha found, go solve /api/captcha')
        return;
    }
    Employee.findAll({
        where: req.query,
        attributes: {exclude: ['password']},
    }).then((employees) => {
        res.json(employees);
    }).catch((e) => {
        console.log(e);
        res.status(500).send('error');
    });
});

app.listen(40004, '0.0.0.0', () => {
    console.log(`Example app listening at 0.0.0.0:40004`)
});

