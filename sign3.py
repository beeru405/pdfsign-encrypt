from base64 import b64decode
from pypdf import PdfReader, PdfWriter
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

key_f = "privkey1.out"
data_f = "test23.pdf"
sig_f = "signature123.sign"

with open(key_f, 'rb') as f: key_pr = f.read()
with open(data_f, 'rb') as f: data = f.read()

def generate_signature(key, data, sig_f):
    print("Generating Signature")
    h = SHA256.new(data)
    rsa = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsa)
    signature = signer.sign(h)
    with open(sig_f, 'wb') as f: f.write(signature)
    print("Signing success")
        
generate_signature(key_pr, data, sig_f)
