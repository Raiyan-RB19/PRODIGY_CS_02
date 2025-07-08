import os
import random
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
def generate_shuffle_order(width, height, key):
    random.seed(key)
    indices = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(indices)
    return indices

def encrypt_image(input_path, output_path, key):
    try:
        img = Image.open(input_path).convert("RGB")
        width, height = img.size
        pixels = img.load()

        shuffle_order = generate_shuffle_order(width, height, key)

        encrypted_img = Image.new("RGB", (width, height))
        encrypted_pixels = encrypted_img.load()

        for original_index, shuffled_index in enumerate(shuffle_order):
            x, y = shuffled_index
            orig_x = original_index % width
            orig_y = original_index // width

            r, g, b = pixels[orig_x, orig_y]
            encrypted_pixels[x, y] = (
                r ^ (key & 0xFF),
                g ^ ((key >> 8) & 0xFF),
                b ^ ((key >> 16) & 0xFF)
            )

        encrypted_img.save(output_path)
        return True

    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return False

def decrypt_image(input_path, output_path, key):
    try:
        img = Image.open(input_path).convert("RGB")
        width, height = img.size
        pixels = img.load()

        shuffle_order = generate_shuffle_order(width, height, key)
        shuffled_indices = {idx: i for i, idx in enumerate(shuffle_order)}

        decrypted_img = Image.new("RGB", (width, height))
        decrypted_pixels = decrypted_img.load()

        for x in range(width):
            for y in range(height):
                orig_pos = shuffled_indices[(x, y)]
                orig_x = orig_pos % width
                orig_y = orig_pos // width

                r, g, b = pixels[x, y]
                decrypted_pixels[orig_x, orig_y] = (
                    r ^ (key & 0xFF),
                    g ^ ((key >> 8) & 0xFF),
                    b ^ ((key >> 16) & 0xFF)
                )

        decrypted_img.save(output_path)
        return True

    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return False
class ImageEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🔐 Advanced Image Encryptor")
        self.master.geometry("750x600")
        self.master.resizable(True, True)

        self.key = ttk.StringVar(value="123456")
        self.input_path = ""
        self.preview_image = None

        self.create_widgets()

    def create_widgets(self): 
        ttk.Label(self.master, text="Encryption Key (0 - 16777215):", font=("Segoe UI", 10)).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        ttk.Entry(self.master, textvariable=self.key, width=25).grid(
            row=0, column=1, padx=10, pady=10, sticky="w"
        )
        ttk.Button(self.master, text="📁 Select Image", command=self.load_image, bootstyle=PRIMARY).grid(
            row=1, column=0, columnspan=2, pady=5
        )
        preview_frame = ttk.LabelFrame(self.master, text="🖼 Image Preview", padding=10)
        preview_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(padx=5, pady=5)

        btn_frame = ttk.Frame(self.master)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Encrypt", command=self.encrypt, bootstyle=SUCCESS, width=15).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Decrypt", command=self.decrypt, bootstyle=INFO, width=15).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Clear", command=self.clear, bootstyle=SECONDARY, width=15).grid(row=0, column=2, padx=10)

        self.status = ttk.Label(self.master, text="No image selected", anchor="w", relief="sunken", font=("Segoe UI", 9))
        self.status.grid(row=4, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.input_path = path
            self.show_preview(path)
            self.status.config(text=f"Loaded: {os.path.basename(path)}")

    def show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((300, 300))
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.preview_image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load preview: {str(e)}")

    def validate_key(self):
        try:
            val = int(self.key.get())
            if 0 <= val <= 0xFFFFFF:
                return val
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Key", "Please enter a valid key between 0 and 16777215.")
            return None

    def encrypt(self):
        key = self.validate_key()
        if not key or not self.input_path:
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")], title="Save Encrypted Image"
        )

        if output_path:
            if encrypt_image(self.input_path, output_path, key):
                self.status.config(text="✅ Image encrypted successfully.")
                self.show_preview(output_path)
                messagebox.showinfo("Success", "Image encrypted successfully!")
            else:
                messagebox.showerror("Error", "Failed to encrypt image")

    def decrypt(self):
        key = self.validate_key()
        if not key or not self.input_path:
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")], title="Save Decrypted Image"
        )

        if output_path:
            if decrypt_image(self.input_path, output_path, key):
                self.status.config(text="✅ Image decrypted successfully.")
                self.show_preview(output_path)
                messagebox.showinfo("Success", "Image decrypted successfully!")
            else:
                messagebox.showerror("Error", "Failed to decrypt image. Check the key.")

    def clear(self):
        self.input_path = ""
        self.preview_label.config(image="")
        self.status.config(text="Cleared. No image selected.")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ImageEncryptorApp(root)
    root.mainloop()
