const express = require('express');
const mysql = require("mysql2");
const crypto = require('crypto'); // For MD5 hashing
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static('public'));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "john",
    password: process.env.DB_PASSWORD || "secureandunpredictablepassword",
    database: process.env.DB_NAME || "db_landing",
});

db.connect(err => {
    if (err) throw err;
    console.log('Connected to MySQL');
});

const md5Hash = (password) => crypto.createHash('md5').update(password).digest('hex');

// Ensure a default user exists
db.query('SELECT COUNT(*) AS count FROM users', async (err, results) => {
    if (err) throw err;
    if (results[0].count === 0) {
        const hashedPassword = md5Hash('banana'); // Default password: "banana"
        db.query('INSERT INTO users (username, password) VALUES (?, ?)', ['admin', hashedPassword], (err) => {
            if (err) throw err;
            console.log('Default admin user created');
        });
    }
});

// Secret key for JWT
const SECRET_KEY = 'your_secret_key';

// Middleware to check authentication
const verifyToken = (req, res, next) => {
    const token = req.cookies.token;
    if (!token) return res.redirect('/login');

    jwt.verify(token, SECRET_KEY, (err, decoded) => {
        if (err) return res.redirect('/login');
        req.userId = decoded.id;
        next();
    });
};

// Login Page
app.get('/login', (req, res) => {
    res.render('login', { query: req.query });
});

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Allow only 5 attempts per window
    message: "Too many failed login attempts. Try again later.",
    headers: true,
});

// Handle Login
app.post('/login', loginLimiter, (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = md5Hash(password);

    db.query('SELECT * FROM users WHERE username = ? AND password = ?', [username, hashedPassword], (err, results) => {
        if (err) throw err;

        if (results.length === 0) {
            return res.redirect('/login?error=1');
        }

        // Generate JWT
        const token = jwt.sign({ id: results[0].id }, SECRET_KEY, { expiresIn: '1h' });
        res.cookie('token', token, { httpOnly: true });
        return res.redirect('/');
    });
});

// Logout
app.get('/logout', (req, res) => {
    res.clearCookie('token');
    res.redirect('/login');
});

// Dashboard
app.get('/', verifyToken, (req, res) => {
    db.query('SELECT * FROM pages', (err, results) => {
        if (err) throw err;
        res.render('dashboard', { pages: results });
    });
});

// Create Page
app.post('/pages', verifyToken, (req, res) => {
    const { title, content } = req.body;
    if (!title || !content) return res.redirect('/?error=missing');

    db.query('INSERT INTO pages (title, content) VALUES (?, ?)', [title, content], (err) => {
        if (err) throw err;
        res.redirect('/');
    });
});

// Edit Page View
app.get('/pages/edit/:id', verifyToken, (req, res) => {
    db.query('SELECT * FROM pages WHERE id = ?', [req.params.id], (err, results) => {
        if (err) throw err;
        if (results.length === 0) return res.status(404).send('Page not found');
        res.render('edit', { page: results[0] });
    });
});

// Update Page
app.post('/pages/update/:id', verifyToken, (req, res) => {
    const { title, content } = req.body;
    db.query('UPDATE pages SET title = ?, content = ? WHERE id = ?', [title, content, req.params.id], (err) => {
        if (err) throw err;
        res.redirect('/');
    });
});

// Delete Page
app.get('/pages/delete/:id', verifyToken, (req, res) => {
    db.query('DELETE FROM pages WHERE id = ?', [req.params.id], (err) => {
        if (err) throw err;
        res.redirect('/');
    });
});

// Start the server
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
