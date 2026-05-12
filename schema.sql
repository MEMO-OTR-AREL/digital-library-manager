CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT,
    status TEXT,
    rating INTEGER,
    favorite INTEGER DEFAULT 0,
    access_until TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);