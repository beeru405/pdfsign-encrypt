from base64 import b64decode
from pypdf import PdfReader, PdfWriter
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5


key_f = "pubkey1.out"
data_f = "test23.pdf"
sig_f = "signature123.sign"

with open(key_f, 'rb') as f: key_pub = f.read()
with open(data_f, 'rb') as f: data = f.read()
 
def verify_signature(key, data, sig_f):
   print("Verifying Signature")
   h = SHA256.new(data)
   rsa = RSA.importKey(key)
   signer = PKCS1_v1_5.new(rsa)
   with open(sig_f, 'rb') as f: signature = f.read()
   if (signer.verify(h, signature)):
    print("Verification Success") 
        
verify_signature(key_pub, data, sig_f)
