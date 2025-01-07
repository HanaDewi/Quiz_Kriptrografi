import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class VigenereCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Vigenere Cipher")
        self.root.geometry("800x600")
        self.root.configure(bg='#ADD8E6')
        self.input_text = tk.StringVar()
        self.key = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        ttk.Label(input_frame, text="Masukkan Teks:").grid(row=0, column=0, sticky="w")
        self.text_input = ttk.Entry(input_frame, textvariable=self.input_text, width=50)
        self.text_input.grid(row=1, column=0, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Upload File", command=self.upload_file).grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Kunci (min. 12 karakter):").grid(row=2, column=0, sticky="w")
        self.key_input = ttk.Entry(input_frame, textvariable=self.key, width=50)
        self.key_input.grid(row=3, column=0, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Enkripsi", command=self.encrypt).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Dekripsi", command=self.decrypt).grid(row=0, column=1, padx=5)
        
        result_frame = ttk.LabelFrame(self.root, text="Hasil", padding="10")
        result_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        
        self.result_text = tk.Text(result_frame, height=10, width=60)
        self.result_text.grid(row=0, column=0, padx=5, pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.input_text.set(file.read())

    def vigenere_cipher(self, text, key, encrypt=True):
        """
        Implementasi algoritma Vigenere Cipher.
        """
        result = []
        key = key.upper()
        text = text.upper()
        key_length = len(key)
        key_as_int = [ord(i) - 65 for i in key]  # Ubah kunci ke angka (0-25)

        for i, char in enumerate(text):
            if char.isalpha():  # Hanya proses huruf
                text_int = ord(char) - 65  # Ubah huruf ke angka (0-25)
                if encrypt:
                    value = (text_int + key_as_int[i % key_length]) % 26
                else:
                    value = (text_int - key_as_int[i % key_length]) % 26
                result.append(chr(value + 65))  # Kembalikan angka ke huruf
            else:
                result.append(char)  # Biarkan karakter non-huruf

        return ''.join(result)

    def validate_input(self):
        """
        Validasi input: teks harus diisi, kunci minimal 12 karakter.
        """
        if len(self.key.get()) < 12:
            messagebox.showerror("Error", "Kunci harus minimal 12 karakter!")
            return False
        if not self.input_text.get():
            messagebox.showerror("Error", "Masukkan teks yang akan diproses!")
            return False
        return True

    def encrypt(self):
        """
        Proses enkripsi teks menggunakan kunci.
        """
        if not self.validate_input():
            return

        text = self.input_text.get()
        key = self.key.get()

        try:
            result = self.vigenere_cipher(text, key, True)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def decrypt(self):
        """
        Proses dekripsi teks menggunakan kunci.
        """
        if not self.validate_input():
            return

        text = self.input_text.get()
        key = self.key.get()

        try:
            result = self.vigenere_cipher(text, key, False)
            
            # Validasi: jika hasil dekripsi tidak masuk akal, beri pesan error
            if not any(char.isalpha() for char in result):  # Cek apakah hasil valid
                raise ValueError("Kunci salah atau teks terenkripsi tidak valid.")

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereCipherApp(root)
    root.mainloop()
