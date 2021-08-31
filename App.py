import tkinter as tk
from tkinter import filedialog, Text
import Main

# Welcome to ENIGMA
# Run this App to start


def load_text():
    root.text = secret_message.get()


def load_image():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=[('image files', ('.png', '.jpg', '.jpeg'))])


def run_encrypt():
    Main.Encrypt(root.text, root.filename)


def run_extract():
    text = Main.Extract(root.filename)
    tk.Label(frame, text="Here is your Secret:", bg="white", font=(None, 10)).grid(row=7)
    # Show secret message
    tk.Label(frame, text=text, font=(None, 15)).grid(row=8, pady=10)


root = tk.Tk()
root.geometry("410x720")
root.title("ENIGMA")
root['bg'] = '#2f4f4f'

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


tk.Label(frame, text="Welcome to ENIGMA\n"
                     "The new creative way to encrypt secret messages in an image").grid(row=0)

# Upload cove image
tk.Button(frame, text='Upload Cover Image', command=load_image,
          padx=10, pady=10, fg="white", bg="#2f6f6f").grid(row=1, pady=25)
# Enter secret string
secret_message = tk.Entry(frame, text='Enter secret message')
secret_message.grid(row=2, padx=10, pady=0, sticky="nsew")
tk.Button(frame, text='Enter Secret Message', command=load_text,
          fg="white", bg="#2f6f6f").grid(row=3)

# Encrypt
tk.Button(frame, text='Start Encryption', command=run_encrypt,
          height=2, width=15, font=("Arial Black", 10)).grid(row=4, pady=50)

# Upload hidden image
tk.Button(frame, text='Upload the Encrypted image', command=load_image,
          padx=10, pady=10, fg="white", bg="#2f6f6f").grid(row=5)

# Extract
tk.Button(frame, text='Extract', command=run_extract,
          height=2, width=15, font=("Arial Black", 10)).grid(row=6, pady=20)

# Quit
tk.Button(frame, text='Quit', command=root.quit).grid(row=9)

root.mainloop()
