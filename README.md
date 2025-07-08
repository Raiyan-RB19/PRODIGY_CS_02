# 🔐 Image Encryptor GUI

A desktop application to encrypt and decrypt images using pixel shuffling and XOR operations. Built with Python, Pillow, and ttkbootstrap.

##  Features

- Encrypt & decrypt any image using a numeric key
- Pixel shuffling with deterministic randomness
- Visual preview before/after encryption
- Modern dark-themed GUI (resizable)
- Clean layout with status reporting

##  Requirements

- Python 3.8+

##  Run the App

     python main.py

## 📷 Supported Formats

   - .png, .jpg, .jpeg, .bmp

 ## How It Works

   - Pixel positions are shuffled using a key-based random seed

   - Each pixel’s RGB values are XORed using portions of the key

   - Decryption reverses the process using the same key 
