# 🔐 Image Encryptor Tool

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

## Supported Formats

   - .png, .jpg, .jpeg, .bmp

 ## How It Works

   - Pixel positions are shuffled using a key-based random seed

   - Each pixel’s RGB values are XORed using portions of the key

   - Decryption reverses the process using the same key
## APP PREVIEW 
![App Preview](https://github.com/Raiyan-RB19/PRODIGY_CS_02/blob/569500c9d3dbbe51159e72f7070a5021dac8e048/Screenshot.png)                         ![App Preview](https://github.com/Raiyan-RB19/PRODIGY_CS_02/blob/7e38e255ac7fdcd3b87f679650e167b323e906ea/Encryption.png)![App Preview](https://github.com/Raiyan-RB19/PRODIGY_CS_02/blob/7e38e255ac7fdcd3b87f679650e167b323e906ea/Decryption.png)
