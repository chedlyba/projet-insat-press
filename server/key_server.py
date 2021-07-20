from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome import Random
import hashlib
import os

AESKey = ""

random = Random.new().read
RSAkey = RSA.generate(1024, random)
public = RSAkey.publickey().exportKey()
private = RSAkey.exportKey()

tmpPub = hashlib.md5(public)
hash_public_key  = tmpPub.hexdigest()
eight_byte_key = os.urandom(8)
sess = hashlib.md5(eight_byte_key )
session = sess.hexdigest()