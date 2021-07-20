from client import RemoteClient
import config
import os 

client = RemoteClient(config.server)
src =input('File to upload : ')
print(src)
if os.path.exists(src) :
    if os.path.isfile(src) :
        client.upload(src_path=src)
    else :
        client.upload_dir(src_path=src)
