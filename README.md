# Setup Instructions

Git clone or download src as zip and extract.

Install MySQL. Can be MariaDB / MySQL it should not matter.
```
CREATE DATABASE debianem;
CREATE USER 'bartsimpson'@'localhost' IDENTIFIED BY 'duffdrinker';
GRANT ALL PRIVILEGES ON debianem.* TO 'bartsimpson'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

In MySQL run the above to create the database and then paste the sql commands on database `debianem` or run
`mysql -u bartsimpson -p debianem < debianem.sql`

Once Database is created and populated, run `python3 -m pip install -r requirements.txt` or just `pip install -r requirements.txt`.

Run with `python3 server.py` and visit `http://localhost:5000`
