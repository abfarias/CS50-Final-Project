CREATE TABLE users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    m_hash TEXT NOT NULL,
    salt BLOB NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE passwords (
    id INTEGER NOT NULL,
    user_id INTEGER,
    domain TEXT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);