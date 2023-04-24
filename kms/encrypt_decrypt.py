import os
from dataclasses import dataclass, asdict

import boto3

client: any = boto3.client('kms')
key_id: str = os.environ.get('KMS_KEY_ID')
text: str = os.environ.get('PLAINTEXT')


@dataclass
class Response():
    text: str
    ciphertext_blob: bytes
    decrypted_text: str


def encrypt(text: str) -> bytes:
    try:
        plaintext: bytes = text.encode(encoding='utf-8')
        response: dict = client.encrypt(
            KeyId=key_id,
            Plaintext=plaintext,
            EncryptionAlgorithm='SYMMETRIC_DEFAULT',
        )

        return response['CiphertextBlob']

    except Exception as e:
        raise e


def decrypt(ciphertext: bytes) -> bytes:
    try:
        response: dict = client.decrypt(
            KeyId=key_id,
            CiphertextBlob=ciphertext,
            EncryptionAlgorithm='SYMMETRIC_DEFAULT',
        )

        return response['Plaintext'].decode('utf-8')

    except Exception as e:
        raise e


ciphertext_blob: bytes = encrypt(text)
decrypted_text: str = decrypt(ciphertext_blob)

response = Response(
    text=text,
    ciphertext_blob=ciphertext_blob,
    decrypted_text=decrypted_text
)

print((asdict(response)))
