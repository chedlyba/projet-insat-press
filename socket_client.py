from types import FrameType
import key_client
import socket
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import hashlib
from Crypto.PublicKey import RSA
import ast

FLAG_READY = 'ready'
AESKey = key_client.AESKey
public = key_client.public
private = key_client.private
hash_public_key = key_client.hash_public_key
eight_byte_key = bytes()

host = '192.168.56.102'
port = 2000
check = False


def padding(s):
    return s + ((16 - len(s) % 16) * '`'.encode())

def remove_padding(s):
    return s.replace('`'.encode(),''.encode())


def handshake(s:socket.socket):
    s.setblocking(True)
    s.send(public +':'.encode()+hash_public_key.encode())


    #receive server public key, eight byte key and hash of eight byte key
    f_get = s.recv(4072)
    lst = f_get.split(':'.encode())
    to_decrypt = lst[0]
    server_public = lst[1]

    decryptor = PKCS1_OAEP.new(RSA.importKey(private))
    try:
        decrypted = decryptor.decrypt(ast.literal_eval(str(to_decrypt)))
    except:
        return False, None

    splitted_decrypt = decrypted.split(':'.encode())
    eight_byte_key= splitted_decrypt[0]
    hash_of_eight_byte_key = splitted_decrypt[1]
    hash_of_public_key = splitted_decrypt [2]


    # hashing for checking
    sess = hashlib.md5(eight_byte_key)
    session = sess.hexdigest()
    hashObj = hashlib.md5(server_public)
    server_public_hash = hashObj.hexdigest()

    print('----Matching server\'s public key and eight byte key')
    if server_public_hash.encode() == hash_of_public_key and session.encode() == hash_of_eight_byte_key :
        # ecrypt eight byte key with server key and send it
        encryptor = PKCS1_OAEP.new(RSA.importKey(server_public))
        server_public =encryptor.encrypt(eight_byte_key)

        s.send(server_public)

        # receiving ready
        server_msg = s.recv(2048)
        server_msg = decrypt_data(server_msg, eight_byte_key)
        
        if server_msg == FLAG_READY.encode() :
            print(f'----Beginning communication \n')
            return True, eight_byte_key
        else :
            return False, None

def encrypt_data(data, key=eight_byte_key):
        # creating 128 bits key with 16 bytes
    key_128 = key + key[::-1]
    AESKey = AES.new(key_128, AES.MODE_CBC, IV=key_128)
    client_msg = padding(data)   
    client_msg= AESKey.encrypt(client_msg)
    return client_msg

def decrypt_data(data, key=eight_byte_key):
        # creating 128 bits key with 16 bytes
    key_128 = key + key [:: -1]
    AESKey = AES.new(key_128, AES.MODE_CBC, IV=key_128)
    data =AESKey.decrypt(data)
    data = remove_padding(data )
    return data



def connect_to_server(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(True)
        s.connect((host, port))
        check = True
        print('----Connected')
    except BaseException as x:
        print(x)
        print('----Unable to conncect')
        check = False

    return s, check

def read_server_info(server, key=eight_byte_key):
    s = server
    encrypted_server_info=s.recv(2048)
    server_info = decrypt_data(
        data=encrypted_server_info,
        key=key).decode()

    print(server_info)

    server_info_dict={
        'host' : server_info.split(':')[0],
        'user' : server_info.split(':')[1],
        'password' : server_info.split(':')[2],
        'path' : server_info.split(':')[3]
    }
    return server_info_dict

def retrieve_server_info():
    server_info = None  
    while server_info == None:   
        s, check = connect_to_server(host=host, port=port)  
        if check is True :
            done, eight_byte_key = handshake(s)
            if done :
                server_info = read_server_info(server=s, key=eight_byte_key)
            else :
                print('*****Keys mismatch*****') 
    return server_info 

if __name__ == '__main__':
    retrieve_server_info()

