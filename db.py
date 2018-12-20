#!/usr/bin/python3
import hashlib
import configparser
import sqlite3

class database:

    def __init__(self,config):
        try:
            self.db = config['Main']['Database']
        except Exception as e:
            print("Config Error!")
            print(e)
            exit()
        try:    
            self.connect()
        except:
            print("Database Error!")
        tables = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
         
        # if(('ialab',) not in tables): 
        #     self.execute('''CREATE TABLE ialab
        #                     (username TEXT PRIMARY KEY,
        #                     href TEXT NOT NULL,
        #                     full_name TEXT NOT NULL);''')



     

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def execute(self,command):
        self.connect()
        self.cur.execute(command)
        self.conn.commit()
        text_return = self.cur.fetchall()
        self.close()
        return text_return

    def executevar(self,command,operands):
        self.connect()
        self.cur.execute(command,operands)
        self.conn.commit()
        text_return = self.cur.fetchall()
        self.close()
        return text_return

    # def insertLdapUser(self,username, email):
    #     self.executevar('INSERT INTO ldap VALUES(?,?)', (username, email))

    # def insertIalabUser(self,username,href,full_name):
    #     self.executevar('INSERT INTO ialab VALUES(?,?,?)', (username, href, full_name))
    
    # def checkIalabUserExists(self,username):
    #     count = self.executevar('SELECT COUNT(username) FROM ialab WHERE username=?', (username,))
    #     if(int(count[0][0])) > 0:
    #         return True
    #     else:
    #         return False
    
    # def checkLdapUserExists(self,username):
    #     count = self.executevar('SELECT COUNT(username) FROM ldap WHERE username=?', (username,))
    #     if(int(count[0][0])) > 0:
    #         return True
    #     else:
    #         return False
    
