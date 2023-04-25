How to run program:
-to run server you have to navigate your self into src folder as: cd src
-and if you're in the src folder you can run main.py as: python main.py (if this not work try: python3 main.py)
-then for example with the program putty you can connect into this server with raw connection
    -as a ip address use ip address you have in you config.json and as a port use port you have in config.json
-when you are connected you can use these commands to communicate with server:
TRANSLATEPING"" -> TRANSLATEPONG"{name of the server from config.json}"
-example:
TRANSLATEPING"NoVAK Translator 1.0"
TRANSLATEPONG"...name of your server..."

TRANSLATELOCL"{english word that you want to translate}" -> you can get one of these responses:TRANSLATEDSUC"{translation of the given word}"/TRANSLATEDERR"{it don't have translation in dictionary.json}"
-example:
TRANSLATELOCL"plane"
TRANSLATEDSUC"letadlo"

TRANSLATELOCL"sing"
TRANSLATEDERR"...error message..."

TRANSLATESCAN"{english word that server will find in other server it's translation}" -> same as TRANSLATELOCL but from different server
-example:
TRANSLATESCAN"house"
10.0.0.1:65430-> TRANSLATELOCL"plane"
10.0.0.1:65430<- TRANSLATEDERR"letadlo"
10.0.0.2:65430-> TRANSLATELOCL"plane"
10.0.0.2:65430<- TRANSLATEDERR"...error message..."

Config:
    config/config.json
    -example of configuration set up
    {
        "server":{
            "address":"localhost",
            "port":65430,
            "connection_timeout":0.5,
            "response_timeout":1,
            "client_timeout":30,
            "name":"Name if the server",
            "error":"some error text that is show when word is not in dictionary"
        },
        "scan":{
            "address":[
                ["127.0.0.1"],
                ["127.0.0.2","127.0.0.5"]
            ],
            "port":[
                [65430,65431],
                [65432]
            ]
        }
    }
    -server part - holds all important information about server configuration
        -address can be as a localhost as you can see in the example or it could be normal ipv4 address(four number split by '.' character in the range of 0-255)
            -the best way how to chose ip address is to go into command prompt on windows or linux and type ipconfig(windows) or ifconfig(linux) and use ipv4 address your pc already have assigned
        -port specify on which port would server run the best option chose from range 1024-65535, it have to be integer
            -be aware on your network could be some port blocked so do some research and find allowed ports and use them
        -connection_timeout decide how long in seconds would program wait when user use 'TRANSLATESCAN' command for each server to connect, has to be decimal bigger than zero
        -response_timeout decide how long in seconds would program wait when user use 'TRANSLATESCAN' command for each server response, has to be decimal bigger than zero
        -client_timeout decide how long can be user connected and not responding in seconds, has to be decimal bigger than zero
        -name can be any non empty string that is show as name of the server when someone ping on your server
        -error can be any non empty string is show as error message when you don't have translation of asked word in server dictionary
    -scan part - holds all important information about address and port range where would program be searching when it will ask other servers to find translation
        -address range is field of fields
            -every one field in the main filed has one or two ip address
            -one ip address is used when we want server to search on one specific ip address
            -two ip addresses is used when we want server to search in ip address rang from first ip address to second ip address both included
        -port range is field of fields
            -every one field in the main filed has one or two ports that have to be integers
            -one port is used when we want server to search on one specific port for each ip address
            -two port is used when we want server to search from port range from first port to second port both included for each ip address
        -in both main fields can be more then on sub filed as you can see in the example

    config/dictionary.json
    -example of dictionary
    {
        "dictionary":[
            ["hemisphere","polokoule"],
            ["explode","explodovat"],
            ["fight","boj"],
            ["tie","kravata"],
            ["restaurant","restaurace"]
        ]
    }
    -in the dictionary filed have to exist exactly five subfield(translations) no less no more
        -each subfield have to have exactly two word
            -first word is english version of the second word
            -second word is translation of the first word into czech language

How to run tests:
- go into test folder: cd test
- run test.py: python test.py (if you have older versions of python: python3 tets.py)

Creation of deamon:
- Use this command to create service:
sudo nano /etc/systemd/system/alfa4.service
- Into the service insert this set up:
[Unit]
Description=Dictionary P2P python service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=2
WorkingDirectory=/home/pi/alfa4/src/
ExecStart=/usr/bin/python3 /home/pi/alfa4/src/main.py
KillMode=process
[Install]
WantedBy=multi-user.target
- make sure that WorkingDirectory nad ExecStart is correct on your device (it could be different)
    - WorkingDirectory is absolute path to the directory where is main.py
    - ExecStart is absolute path to the main.py with absolute path to the python3 or just python if you have newer python installed
- use these command in  correct order
sudo systemctl daemon-reload
sudo systemctl enable alfa4
sudo systemctl start alfa4
- with these command you can check if the service is running
sudo systemctl status alfa4
sudo netstat -tunlp

