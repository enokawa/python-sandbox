import os
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet
import boto3

client: any = boto3.client('kms')
key_id: str = os.environ.get('KMS_KEY_ID')
text: str = os.environ.get('PLAINTEXT')
encrypted_data_key_path: str = "./encrypted_data_key.txt"

def generate_data_key() -> tuple[bytes, bytes]:
    try:
        response = client.generate_data_key(
            KeyId=key_id,
            KeySpec='AES_256',
        )

        data_key: bytes = response["Plaintext"]
        encrypted_data_key: bytes = response["CiphertextBlob"]

        return data_key, encrypted_data_key

    except Exception as e:
        raise e

def encrypt(data_key: bytes) -> bytes:
    plaintext: bytes = text.encode(encoding='utf-8')
    f = Fernet(urlsafe_b64encode(data_key))
    
    return f.encrypt(plaintext)

# 1. Execute GenerateDataKey to create CDK using CMK
data_key, encrypted_data_key = generate_data_key()

# 2. Encrypt plaintext using data key
encrypted_data: bytes = encrypt(data_key)

# 3. Store encrypted data key
with open(encrypted_data_key_path, "w") as fp:
    fp.write(urlsafe_b64encode(encrypted_data_key).decode())

# 4. Delete data key
del data_key
