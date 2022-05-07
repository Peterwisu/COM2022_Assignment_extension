# COM2022 Computer Networking Assignment (individual extension part)
## About this project

This is an COM2022 Computer Networking Assignment 2021/2022 by Wish Suharitdamrong in Group 19.

# Real time Video Broadcasting (RTVB)

RTVB is a protocol created on top of User Datagram protocol on Application layers.

## Requirement 
- Python version 3
- Source of Video 
  - WebCam
  - MP4 file
- MySql Database server

 

## Installation

To run a this script 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install numpy
pip install opencv-python
pip install imutils
pip install python-dotenv
pip install mysql-connector-python
```

## For MacOS 
To maximize a buffer size of UDP in MacOs 
```bash
sudo sysctl -w net.inet.udp.maxdgram=65535
```

## Usage

### Database connection

Use environment file to connect Mysql database by 
- Create .env file  and copy everything from .env.example
```env
HOST='localhost'
DATABASE='DATABASE'
USERNAME='USERNAME'
PASSWORD='PASSWORD'
```
- Replace a database credentials in a .env file

#### OR

connect to Mysql database without .env file replace os.getenv() with database credentials in UDPServer.py
```python 
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
```

### Database migration

open the mysql terminal and run a command
```mysql
mysql> source db.sql
```

### Start a Server and Client

To run a Server
```bash
python3 UDPServer.py 
```

To run a Client
```bash
python3 UDPClient.py 
```


## Acknowledgement




## License
Wish Suharitdamrong 
