import os
from dataclasses import dataclass, asdict
from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.fernet import Fernet
import boto3


client: any = boto3.client('kms')
key_id: str = os.environ.get('KMS_KEY_ID')
text: str = os.environ.get('PLAINTEXT')
encrypted_data_key_path: str = "./encrypted_data_key.txt"

@dataclass
class Response():
    plaintext: str
    decrypted_text: str

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


def decrypt(data_key: bytes, encrypted_data) -> bytes:
    f = Fernet(urlsafe_b64encode(data_key))

    return f.decrypt(encrypted_data)


def decrypt_data_key(ciphertext: bytes) -> bytes:
    try:
        response: dict = client.decrypt(
            KeyId=key_id,
            CiphertextBlob=ciphertext,
            EncryptionAlgorithm='SYMMETRIC_DEFAULT',
        )

        return response['Plaintext']

    except Exception as e:
        raise e


# Encryption
## 1. Execute GenerateDataKey to create CDK using CMK
data_key, encrypted_data_key = generate_data_key()

## 2. Encrypt plaintext using data key
encrypted_data: bytes = encrypt(data_key)

## 3. Store encrypted data key
with open(encrypted_data_key_path, "w") as fp:
    fp.write(urlsafe_b64encode(encrypted_data_key).decode(encoding='utf-8'))

## 4. Delete data key
del data_key


# Decryption
# 0. read encrypted data key
with open(encrypted_data_key_path, "r") as fp:
    encrypted_data_key = urlsafe_b64decode(fp.read())

# 1. Decrypt the encrypted data key
data_key_for_decrypt: bytes = decrypt_data_key(ciphertext=encrypted_data_key)

# 2. Decrypt the encrypted data using data key
decrypted_data: bytes = decrypt(data_key=data_key_for_decrypt, encrypted_data=encrypted_data)
decrypted_text: str = decrypted_data.decode()

# 3. Delete data key
del data_key_for_decrypt


response = Response(
    plaintext=text,
    decrypted_text=decrypted_text,
)

print((asdict(response)))
# -> {'plaintext': 'enokawa', 'decrypted_text': 'enokawa'}
