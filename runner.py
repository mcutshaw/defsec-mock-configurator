from ssh import ssh
from db import database
import os

class module:
    def __init__(self, db, rowid, username='root', password='Password1!'):
        self.rowid = rowid 
        self.db = db
        self.createFromRowID()
        self.username = username
        self.ip = self.db.getHostIP(self.host)
        self.password = password
        self.ssh = ssh(self.username, self.ip, self.password)

    def createFromRowID(self):
        self.host, self.name, self.state, self.operands, self.stdin, self.stdout, self.stderr = self.db.getModuleAll(self.rowid)

    def run(self):
        os.chdir('modules')
        self.ssh.put_folder(self.name)
        os.chdir('..')
        self.ssh.chdir(self.name)
        self.writeVars()
        self.ssh.make_executable('./main')
        self.stdout = self.ssh.send_cmd('./main')
        self.ssh.chdir('..')
        self.ssh.remove_folder(self.name)
        self.ssh.close()

    def writeVars(self):
        self.ssh.write('vars', self.operands)


class runner:

    def __init__(self, db):
        self.db = db
        self.hosts = self.getHosts()

    def run(self):
        for host in self.hosts:
            self.moveCommon(host, self.db.getHostIP(host))
            modules = self.db.getModulesFromHost(host)
            for m in modules:
                m = module(self.db, m)
                m.run()
            self.removeCommon(host, self.db.getHostIP(host))

    def getHosts(self):
        return self.db.getHosts()

    def getModules(self):
        return self.db.getModules()

    def moveCommon(self, host, address, username='root', password='Password1!'):
        s = ssh(username, address, password)
        s.put_folder('common')
        s.close()

    def removeCommon(self, host, address, username='root', password='Password1!'):
        s = ssh(username, address, password)
        s.remove_folder('common')
        s.close()