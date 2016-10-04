CREATE TABLE IF NOT EXISTS module (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    url TEXT
);

CREATE TABLE IF NOT EXISTS request (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL UNIQUE,
    module_id INTEGER NOT NULL,
    input TEXT,
    output TEXT,
    FOREIGN KEY (module_id) REFERENCES module(id)
);
