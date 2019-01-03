import configparser
from ssh import ssh
from db import database
from conf import config

config_file = configparser.ConfigParser()
config_file.read('example.conf')
db = database(config_file)

config = config(db, config_file)
config.loadConfig()
