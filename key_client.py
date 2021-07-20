from Cryptodome import Random
import Cryptodome.Cipher.AES as AES
from Cryptodome.PublicKey import RSA
import hashlib

AESKey =''
random = Random.new().read
RSAKey = RSA.generate(1024, random)
public = RSAKey.publickey().exportKey()
private = RSAKey.exportKey()

tmpPub = hashlib.md5(public)
hash_public_key = tmpPub.hexdigest()

#print(f'{public} \n {private}')

