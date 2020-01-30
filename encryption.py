from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

from secret_config import app_secret


def enc(message, password=app_secret):
    """
    encrypt a message to a decrypted one

    :param message: the message to decrypt
    :param password: the secret key to use

    :return: the encrypted string
    :rtype: str
    """
    cipher_suite = Fernet(password)
    cipher_text = cipher_suite.encrypt(bytes(message, "UTF-8"))
    return b64encode(cipher_text)


def dec(message, password=app_secret):
    """
    decrypt a message string to the actual plain text

    :param message: the message to decrypt
    :param password: the secret key

    :return: the actual message
    :rtype: str
    """
    cipher = b64decode(message)
    cipher_suite = Fernet(password)
    cipher_text = cipher_suite.decrypt(cipher)
    return cipher_text.decode("utf-8")
