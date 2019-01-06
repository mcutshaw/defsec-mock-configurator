import paramiko
import os
import stat

class ssh:

    def __init__(self, username, address, password, key=None):
        self.con = paramiko.SSHClient()
        self.con.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.con.connect(address,username=username, password=password)
        self.sftp = None
        self.dir = self.con.exec_command('pwd')[1].read().rstrip().decode('utf-8') + '/'
    
    def _cmd(self, command):
        (self.stdin, self.stdout, self.stderr) = self.con.exec_command('cd ' + self.dir + '; ' + command)
        print(self.stderr.read().rstrip().decode('utf-8'),end='')
    def send_cmd(self, command):
        self._cmd(command)
        return self.stdout.read().rstrip().decode('utf-8')

    def close(self):
        self.con.close()

    def close_sftp(self):
        if self.sftp == None:
            return None
        self.sftp.close()

    def invoke_sftp(self):
        self.sftp = self.con.open_sftp()

    def mkdir(self, name):
        if self.sftp == None:
            self.invoke_sftp()
        self.sftp.mkdir(name)

    def chdir(self, name):
        if self.sftp == None:
            self.invoke_sftp()

        self.sftp.chdir(name)

        if name[-1:] != '/':
            name += '/'
        self.send_cmd('cd ' + name)
        self.dir += name

    def put(self, local, remote):
        if self.sftp == None:
            self.invoke_sftp()
        self.sftp.put(local, remote)

    def put_here(self, name):
        if self.sftp == None:
            self.invoke_sftp()
        self.sftp.put(name, name)

    def rm(self, name):
        if self.sftp == None:
            self.invoke_sftp()
        self.sftp.remove(name)
        
    def check_file_exists(self, name):
        if self.sftp == None:
            self.invoke_sftp()
        try:
            self.sftp.stat(name)
            return True
        except FileNotFoundError:
            return False

    def put_folder(self, name):
        if self.sftp == None:
            self.invoke_sftp()
        if not self.check_file_exists(name):
            self.mkdir(name)
        dir = os.listdir(name)
        os.chdir(name)
        self.chdir(name)
        for item in dir:
            if os.path.isfile(item):
                if not self.check_file_exists(item):
                    self.put_here(item)
            else:
                self.put_folder(item)
        os.chdir('..')
        self.chdir('..')

    def remove_folder(self, name):
        if self.sftp == None:
            self.invoke_sftp()

        dir = self.sftp.listdir(name)
        self.chdir(name)
        for item in dir:
            stats = self.sftp.stat(item)
            if stat.S_ISDIR(stats.st_mode):
                self.remove_folder(item)
            else:
                self.rm(item)
        self.chdir('..')
        self.sftp.rmdir(name)

    def write(self, file_path, content):
        if self.sftp == None:
            self.invoke_sftp()

        f = self.sftp.file(file_path, 'w')
        f.write(content)
        f.close()
    
    def make_executable(self, file_path):
        if self.sftp == None:
            self.invoke_sftp()

        self.sftp.chmod(file_path, 755)

    