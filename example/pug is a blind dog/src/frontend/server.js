const express = require("express");
const mysql = require("mysql2");
const pug = require("pug");

const app = express();

// Set Pug as the template engine
app.set("view engine", "pug");

// MySQL Database Connection
const db = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    user: process.env.DB_USER || "john",
    password: process.env.DB_PASSWORD || "secureandunpredictablepassword",
    database: process.env.DB_NAME || "db_landing",
});

db.connect((err) => {
    if (err) {
        console.error("Database connection failed:", err);
    } else {
        console.log("Connected to MySQL database");
    }
});

app.get("/", (req, res) => {
    let { page: page = 'dashboard' } = req.query;
    
    const blacklist = ["SELECT", "UNION", "AND", "OR", "FROM", ";", "#"];
    blacklist.forEach(word => {
        const regex = new RegExp(word, "g");
        page = page.replace(regex, "");
    });

    page = page.replace(/\s+/g, "");

    db.query("SELECT * FROM pages WHERE title = '" + page + "'", (err, results) => {
        if (err || results.length === 0) {
            console.error(err);

            return res.status(404).render("404");
        }
        try {
            const html = pug.render(results[0].content);
            res.send(html);
        } catch (err) {
            console.error(err);
            return res.status(404).render("404");
        }
    });
});

const port = 80;
app.listen(port, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${port}`);
});
