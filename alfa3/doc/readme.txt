Alfa 3
name:Antonín Kadrmas
mail:kadrmas@spsejecna.cz
date:1.30.2023
school:Secondary Technical School of Electrical Engineering Jecna 30, Prague, Czech Republic
school project

used external library's:
- mysql-connector-python => https://pypi.org/project/mysql-connector-python/
- prettytable => https://pypi.org/project/prettytable/

Run:
- run main.py in src folder as
    - python src/main.py
- login with name
    -use admin to login as administrator
    -use some different name to login as a user
        -if this name does not exists you will create new user

Config:
-config has two main part 
    -database mandatory part
    -import optional part (without import config data can not be imported)
-config has to by in config.json file in config folder
-example of config:
{
    "db_config":{
       "address":"ip_address",
       "database":"db_name"
    },
    "import":{
        "file":"absolute_file_path",
        "delimiter":";"
    }
}
-database configuration has address and database parameters
    -address is ip address of database (it could be a localhost)
    -database parameter is name of the database which we will working with 
-import configuration has file and delimiter parameters
    -file parameter is absolute path to imported csv file
    -delimiter is optional parameter and it is one character that divides values in csv (; by default)
        -with out delimiter data from absolute path file can be still imported

Import:
-example imported files is in data import folder
-all imported files has to be of type csv
-delimiter is in default ; but in config.json can be changed
-if there is some error in import config to see the changes you have to restart the program
-import into brand, csv file is composed of two values
    -brand name this value has to be unique
    -residence of the brand like New York or Prague
    -for example:
        -Samsung;Thailand
        -Apple;Washington
            -Apple is brand name
            -Washington is residence of the Apple
-import into product, csv file is composed of four values
    -product name
    -weight in kg can be hav to be number can be decimal
    -price have to be a number can be decimal
    -brand id as
        -number integer has to exist in brand table
        -string brand name has to exist in brand table
    -for example:
        -shoes;0.02;49.99;1 (the 1 is id of the specific brand)
        -phone;0.05;249.49;Samsung
            -phone is name of the product
            -0.05 is weight in kilograms of the phone
            -49.99 is price for the phone
            -Samsung is a brand which the phone belongs to 
