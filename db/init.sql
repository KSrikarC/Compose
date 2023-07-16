CREATE DATABASE IF NOT EXISTS bank;


CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        dob DATE NOT NULL,
        mobile VARCHAR(20) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL
    );

CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        transaction_type VARCHAR(255) NOT NULL,
        amount VARCHAR(255) NOT NULL,
        transaction_date DATETIME NOT NULL,
        balance VARCHAR(255) NOT NULL,
        user VARCHAR(255) NOT NULL
    );
