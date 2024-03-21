# Setup Instructions
GIT Clone this repository or download the source code as a .zip file and extract it.
Instal MySQL
`sudo apt install mysql-server`
https://dev.mysql.com/downloads/installer/

Get connected to the SQL Server you are hosting via command line and run the following commands to create the database and privileged user.
```
CREATE DATABASE debianem;
CREATE USER 'bartsimpson'@'localhost' IDENTIFIED BY 'duffdrinker';
GRANT ALL PRIVILEGES ON debianem.* TO 'bartsimpson'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

You can connect to the `debianem` database and paste the content of `debianem.sql` if you wish but I do it as follows (works on linux...):
`mysql -u bartsimpson -p debianem < debianem.sql`

Once the Database is set up you need to sort the Python dependencies.

Linux:
Run the first line as well or `mysqlclient` will fail to install from pip.
```
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
python3 -m ensurepip
pip install -r requirements.txt
```

Do not forget to install QRcode:
```
pip3 install qrcode
```

Windows:
```
python3 -m ensurepip
pip install -r requirements.txt
```

Launch the server via `python3 server.py` and visit `localhost:5000` to see the webpage.
Live instance available @ http://atuproject.tech/
