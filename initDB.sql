-- Create the database
CREATE DATABASE IF NOT EXISTS mtxgame;

-- Use the database
USE mtxgame;

-- Create the table 'Games'
CREATE TABLE IF NOT EXISTS Games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matrix VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    moves VARCHAR(255) NOT NULL,
    times VARCHAR(255) NOT NULL
);