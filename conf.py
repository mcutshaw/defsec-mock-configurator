from db import database
import configparser

class config:

    def __init__(self, db, config):
        self.config = config
        self.db = database(self.config)

    def loadConfig(self):
        self.db.clearDB()
        self.inherit_all()
        self.loadHosts()
        self.loadModules()

    def genOperands(self, key):
        string = ''
        for item in self.config[key]:
            if item != 'base' and item != 'module':
                string += item + '=' + self.config[key][item] + '\n'
        return string

    def loadHosts(self):
        for key in self.config['Hosts']:
            host = self.config['Hosts'][key]

            ip = self.config[host]['ip']
            if len(ip.split('.')) == 1:
                if len(self.config[host]['subnet'].split('.')) == 3:
                    ip = self.config[host]['subnet'] + '.' + ip
                else:
                    ip = self.config[host]['subnet'][:-1] + ip
            print(ip)
            self.db.insertHost(host, ip)

    def loadModules(self):
        for host in self.db.getHosts():
            for module in self.config[host]['modules'].split(','):
                operands = self.genOperands(module)
                self.db.insertModule(host, self.config[module]['module'], operands=operands)

    def inherit_all(self):
        for section in self.config:
            for key in self.config[section]:
                if key == 'base':
                    self._inherit(section, self.config[section]['base'])

    def _inherit(self, child, parent):
        for key in self.config[parent]:
            if key not in self.config[child]:
                self.config.set(child, key, self.config[parent][key])