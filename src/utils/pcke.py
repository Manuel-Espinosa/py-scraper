import os
import hashlib
import base64

code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').replace('=', '')

sha256_of_verifier = hashlib.sha256(code_verifier.encode('utf-8')).digest()
code_challenge = base64.urlsafe_b64encode(sha256_of_verifier).decode('utf-8').replace('=', '')

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")
