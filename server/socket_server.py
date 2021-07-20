import hashlib
import socket 
import sys
import threading
import signal
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome import Random
import key_server
from Cryptodome.Cipher import PKCS1_OAEP
import ast
import config

host =''
port = 2000
CONNECTION_LIST=[]
YES='1'
NO='2'

AESKey = key_server.AESKey
public = key_server.public
private = key_server.private
hash_public_key = key_server.hash_public_key
eight_byte_key = key_server.eight_byte_key
session = key_server.session


FLAG_READY = 'ready'


def padding(s):
    return s + ((16 - len(s) % 16) * '`')

def remove_padding(s):
    return s.replace('`','')

def handshake(client: socket.socket):

    client_key_hash = client.recv(2048)
    split = client_key_hash.split(':'.encode())
    client_key = split[0]
    client_hash = split[1]

    tmpHash = hashlib.md5(client_key)
    tmpHash = tmpHash.hexdigest()

    if tmpHash == client_hash.decode()  :

        # sending public key,encrypted eight byte ,hash of eight byte and server public key hash
        client_public = RSA.importKey(client_key)
        f_send = eight_byte_key + (':'+ session + ':' + hash_public_key).encode()
        encryptor = PKCS1_OAEP.new(client_public)
        f_send = encryptor.encrypt(f_send)
        client.send( f_send+':'.encode()+public )
        client_key_hash = client.recv(2048)

        if client_key_hash !=''.encode() :

            decryptor = PKCS1_OAEP.new(RSA.importKey(private))            
            client_key_hash = decryptor.decrypt(ast.literal_eval(str(client_key_hash)))

            if client_key_hash == eight_byte_key :
                client.send(encrypt_data(data=FLAG_READY))
                return True
            
            else:
                print('*****Session keys mismatch*****')

        else :
            print('*****keys mismatch*****')
            client.close()
            return False
    else :
        print('*****keys mismatch*****')
        client.close()
        return False


def connection_setup(server):
    while True:
        client, address = server.accept()
        client.setblocking(True)
        print('accepting clients')
    
        done = handshake(client)
        if done :
            send(client=client)

def decrypt_data(data, key=eight_byte_key):
        # creating 128 bits key with 16 bytes
    key_128 = eight_byte_key + eight_byte_key [:: -1]
    AESKey = AES.new(key_128, AES.MODE_CBC, IV=key_128)
    data =AESKey.decrypt(data)
    data = remove_padding(data )
    return data


def encrypt_data(data=FLAG_READY, key=eight_byte_key):
        # creating 128 bits key with 16 bytes
    key_128 = eight_byte_key + eight_byte_key[::-1]
    AESKey = AES.new(key_128, AES.MODE_CBC, IV=key_128)
    client_msg = padding(data).encode()    
    client_msg= AESKey.encrypt(padding(data).encode())
    return client_msg

def send(client,data=config.server):
    server_info = str()
    for key, value in data.items():
        server_info = server_info+ ':' + value 
    server_info = server_info.lstrip(server_info[0])
    print(server_info)
    encrypted_server_info = encrypt_data(data=server_info)
    client.send(encrypted_server_info)

def send_server_info():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    threading_accept = threading.Thread(target=connection_setup, args=[server])
    threading_accept.start()


def exit_on_quit():
    while True:
        cmd = input('>')
        if cmd == 'quit':
            sys.exit()

if __name__ == '__main__':
    send_server_info_thread = threading.Thread(target=send_server_info)
    send_server_info_thread.daemon = True
    send_server_info_thread.start()
    while True:
        cmd = input('>')
        if cmd == 'quit':
            sys.exit()
