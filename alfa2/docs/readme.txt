For run the program is important to do two things:
    1. set up the config.json in config folder
    2. execute file KadrmasAlfa.py with on of the three parameters
        1. --decode to call function that take car about decoding
        2. --encode to call function that take car about encoding
        3. --logs to manage saved logs results
    (if you want to record result of program into xml file use --debug as a second option parameter 
    otherwise nothing will be stored every time you run the program)
    => example of executing KadrmasAlfa.py is: python src/KadrmasAlfa.py --decode --debug

param --logs explanation:
    you have to call program with parameter --debug to have some logs
    you can not use --debug when you using parameter --logs
    you can call param --logs with one other param:
        1. --between_date is called with tow other parameters
            => use parameter date in shape of year-month-day (python src/KadrmasAlfa.py --logs between_date 2023-1-5 2023-3-5)
            => use parameter date in shape of year-month-day_hour:minute:second (python src/KadrmasAlfa.py --logs between_date 2023-1-5_:30:30 2023-3-5_22:20:20)
        2. --mode is called with one other parameter
            => use parameter 'encode' to filter only encode logs (python src/KadrmasAlfa.py --logs encode)
            => use parameter 'decode' to filter only decode logs (python src/KadrmasAlfa.py --logs decode)
        3. --status is called with one other parameter
            => use parameter 'success' to filter only success logs (python src/KadrmasAlfa.py --logs success)
            => use parameter 'error' to filter only error logs (python src/KadrmasAlfa.py --logs error)
        4. without parameter you will get all data (python src/KadrmasAlfa.py --logs)

config.json explanation:
    base structure of the config.json in config folder is:
    {
        "config":{
            "fromFile":"path",
            "toFile":"path",
            "overwrite":boolean,
        }
    }
    - parameter fromFile is path from config.json to the file that would be encoded or decoded('./data/forEncode/example.txt')
    - parameter toFile is path from config.json to the place where would be finally encoded or decoded result stored('./data/forDecode/example.txt')
        - is important to add the file name at the end if the file with this name does not exist is created else it is overwrite or exception occurs
    - parameter overwrite decide if program can rewrite file in toFile path (true=>can rewrite, false=>error occurs)
    both path in fromFile and toFile have to exists only in toFile parameter the file at the end does not have to exists

tests can by executing file text.py in test folder

if you want try this program use example files in data folder:
    encode:
        {
            "config":{
                "fromFile":"./data/forEncode/example.txt",
                "toFile":"./data/forDecode/example.txt",
                "overwrite":true
            }
        }
        and then run python src/KadrmasAlfa.py --encode
    decode:
        {
            "config":{
                "fromFile":"./data/forDecode/example.txt",
                "toFile":"./data/forEncode/example.txt",
                "overwrite":true
            }
        }
        and then run python src/KadrmasAlfa.py --decode