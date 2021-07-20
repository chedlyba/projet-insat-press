from client import RemoteClient
import socket_client
import os 

server_info = socket_client.retrieve_server_info()
client = RemoteClient(server_info)


src =input('File to upload : ')
print(src)


if os.path.exists(src) :
    if os.path.isfile(src) :
        client.upload(src_path=src, server=server_info)
    else :
        client.upload_dir(src_path=src)
