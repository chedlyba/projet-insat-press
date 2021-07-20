from sys import stdout
from paramiko import SSHClient, AutoAddPolicy, Transport, SFTPClient
import os
import time

#from paramiko.channel import ChannelFile, ChannelStderrFile, ChannelStdinFile, Channel

class RemoteClient :
    server= dict()

    def __init__(self, server) :
        self.server = server
    
    def ssh_connect(self) : 
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=self.server['host'], 
            username=self.server['user'], 
            password=self.server['password']
            )
        self.client= client


    def ssh_command(self,command=None, mode=0) :
        stdin, stdout, stderr = self.client.exec_command('echo $USER:$PWD')
        cwd=stdout.read().decode().replace('\n','')
        stdout.flush()
        if mode == 0 :
            if command == None :
                command = input(f'{cwd}> ')
            stdin, stdout, stderr = self.client.exec_command(command)
            time.sleep(0.1)
            print(f'{stdout.read().decode()}')
            print(f'{stderr.read().decode()}')
        elif mode == 1 :
            while True :
                command = input(f'{cwd}> ')
                if command == 'exit' :
                    break
                stdin, stdout, stderr = self.client.exec_command(command)
                time.sleep(0.1)
                print(f'{stdout.read().decode()}')
                print(f'{stderr.read().decode()}')

    def upload_dir(self,src_path):
        server = self.server
        transport = Transport((server['host'],22))
        transport.connect(None, username=server['user'], password=server['password'])
        sftp = MySFTPClient.from_transport(transport)
        new_dir=os.path.join(server['path'],os.path.basename(src_path))
        sftp.mkdir(new_dir,ignore_existing=True)
        print(new_dir)
        sftp.put_dir(src_path,new_dir)
        sftp.close()

    def upload(self, src_path, server=server ) :
        print(server)
        transport = Transport((server['host'],22))
        transport.connect(None, username=server['user'], password=server['password'])
        stfp_client = SFTPClient.from_transport(transport)
        file_name=os.path.basename(src_path)
        dest_path= os.path.join(server['path'],file_name)
        stfp_client.put(src_path, dest_path)
        stfp_client.close()


class MySFTPClient(SFTPClient):

    def mkdir(self,path,mode =511, ignore_existing=False):
        try:
            super(MySFTPClient,self).mkdir(path,mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise
    def put_dir(self,source,target):
        for item in os.listdir(source):
            print(f'{item} {os.path.isfile(os.path.join(source,item))}')
            if os.path.isfile(os.path.join(source,item)):
                new_file =os.path.join(target,item)
                print(new_file)
                self.put(os.path.join(source,item), '%s/%s' % (target,item))
            else :
                new_dir = '%s/%s' % (target, item)
                print(new_dir)
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source,item),'%s/%s' % (target, item))

    

        
