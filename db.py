#!/usr/bin/python3
import hashlib
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
        self.createTables()

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

    def insertHost(self,name, ip):
        self.executevar('INSERT INTO hosts VALUES(?,?)', (name, ip))

    def getHosts(self):
        return [item[0] for item in self.execute('SELECT name from hosts')]

    def getModules(self):
        return [item[0] for item in self.execute('SELECT name from modules')]

    def getModulesFromHost(self, host):
        return [item[0] for item in self.execute("SELECT rowid from modules WHERE host='{host}'".format(host=host))]

    def getModuleAll(self, rowid):
        return self.execute("SELECT host,name,state,operands,stdin,stdout,stderr from modules WHERE rowid='{rowid}'".format(rowid=rowid))[0]

    def getHostAll(self, host):
        return self.execute("SELECT name,ip from hosts WHERE name='{name}'".format(name=host))[0]

    def getHostIP(self, host):
        return self.execute("SELECT ip from hosts WHERE name='{name}'".format(name=host))[0][0]

    def insertModule(self, host, name, state="unstarted", operands=None, stdin=None, stdout=None, stderr=None):
        self.executevar('INSERT INTO modules VALUES(?,?,?,?,?,?,?)', (host, name, state, operands, stdin, stdout, stderr))

    def createTables(self):
        tables = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if(('hosts',) not in tables): 
            self.execute('''CREATE TABLE hosts
                            (name TEXT PRIMARY KEY,
                            ip TEXT NOT NULL);''')
        if(('modules',) not in tables): 
            self.execute('''CREATE TABLE modules
                            (host TEXT,
                            name TEXT NOT NULL,
                            state TEXT NOT NULL,
                            operands TEXT,
                            stdin TEXT,
                            stdout TEXT,
                            stderr TEXT,
                            FOREIGN KEY (host) REFERENCES hosts(name));''')
    def clearDB(self):
        tables = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in tables:
            self.execute('DROP TABLE {arg}'.format(arg=table[0]))
        self.createTables()
    
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