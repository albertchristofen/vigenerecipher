import os
import random
import string
import tkinter as tk
from tkinter import filedialog

def add_padding_to_word(word, padding_length):
    """Menambahkan padding ke setiap kata dengan karakter acak."""
    padding = ''.join(random.choices(string.ascii_uppercase, k=padding_length))
    return word + padding

def remove_padding_from_word(word, padding_length):
    """Menghapus padding dari setiap kata."""
    return word[:-padding_length] if padding_length > 0 else word

def vigenere_cipher(text, key, mode='encrypt', padding_length=0):
    """Enkripsi atau dekripsi dengan cipher Vigenere dan menambahkan/ mengurangi padding."""
    result = []
    key = key.upper()
    text = text.upper()
    key_index = 0

    words = text.split()

    for word in words:
        if mode == 'decrypt':
            # Hapus padding terlebih dahulu pada dekripsi
            word = remove_padding_from_word(word, padding_length)
        
        word_result = []
        for char in word:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')

                if mode == 'decrypt':
                    shift = -shift

                new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                word_result.append(new_char)
                key_index += 1
            else:
                word_result.append(char)  # Non-alphabetical characters are not encrypted/decrypted

        word_result = ''.join(word_result)

        if mode == 'encrypt':
            word_result = add_padding_to_word(word_result, padding_length)

        result.append(word_result)

    return ' '.join(result)

def encrypt_decrypt_file(file_path, key, mode, padding_length=0):
    """Proses enkripsi/dekripsi untuk file"""
    # Membaca file dan mengenkripsi/dekripsi seluruh isinya
    with open(file_path, 'r') as file:
        text = file.read()

    # Proses cipher
    result = vigenere_cipher(text, key, mode, padding_length)

    # Menentukan lokasi file output (menggunakan direktori yang sama dengan file input)
    output_file = os.path.join(os.path.dirname(file_path), f"output_{mode}_{os.path.basename(file_path)}")

    # Menyimpan hasil ke file output
    with open(output_file, 'w') as file:
        file.write(result)

    print(f"Hasil {mode} disimpan dalam file: {output_file}")

def open_file_dialog():
    """Membuka dialog file untuk memilih file"""
    root = tk.Tk()
    root.withdraw()  # Menyembunyikan jendela utama tkinter
    file_path = filedialog.askopenfilename(title="Pilih File untuk Enkripsi/Dekripsi")
    return file_path

def main():
    title = "[VIGENERE CIPHER]"
    print(title)
    print("-" * len(title))  # Garis sepanjang panjang title

    while True:
        # Menanyakan apakah input manual atau file
        input_type = input("Masukkan Pilihan Anda\n[Manual] | [File]: ").strip().lower()

        # Validasi input
        while input_type not in ['manual', 'file']:
            input_type = input("Input Anda Salah. Masukkan pilihan [Manual] atau [File]: ").strip().lower()

        # Pilih mode encrypt atau decrypt
        mode = input("Masukkan Pilihan Anda\n[1] Encrypt | [2] Decrypt: ").strip()

        # Validasi mode
        while mode not in ['1', '2']:
            mode = input("Input Anda Salah. Masukkan pilihan [1] untuk Encrypt atau [2] untuk Decrypt: ").strip()

        # Menentukan mode berdasarkan input
        if mode == '1':
            mode = 'encrypt'
            print("\n*Encrypting ...\n")
        else:
            mode = 'decrypt'
            print("\n*Decrypting\n")

        if input_type == 'manual':
            # Masukkan jumlah kali enkripsi/dekripsi
            times = int(input("Mau melakukan manual input berapa kali? "))

            for i in range(times):
                # Berikan jarak newline dan judul untuk setiap iterasi
                if i > 0:
                    print("\n" + "*" * 15)  # Cetak garis pemisah
                    print(f"* Iterasi {i+1} {mode.capitalize()}ing ...\n")

                # Masukkan teks dan kunci secara manual
                if mode == 'encrypt':
                    text_prompt = "Masukkan Plaintext: "
                else:
                    text_prompt = "Masukkan Ciphertext: "

                text = input(text_prompt)
                key = input("Masukkan Key: ")

                # Menanyakan panjang padding
                padding_length = int(input("Masukkan panjang padding yang diinginkan untuk setiap kata: ")) if mode == 'encrypt' else 0

                print("\n")

                # Proses cipher
                result = vigenere_cipher(text, key, mode, padding_length)

                # Menampilkan hasil
                if mode == 'encrypt':
                    subtitle = "[ENCRYPTED USING VIGENERE CIPHER]"
                    print("-" * len(subtitle))
                    print(subtitle)
                    print("-" * len(subtitle))
                    print(f"#plaintext: {text}")
                    print(f"#key: {key}")
                    print("[CIPHER CREATED!]")

                    print(f"#Result: {text} -> {result}")
                else:
                    subtitle = "[DECRYPTED USING VIGENERE CIPHER]"
                    print("-" * len(subtitle))
                    print(subtitle)
                    print("-" * len(subtitle))
                    print(f"#ciphertext: {text}")
                    print(f"#key: {key}")

                    # Tanyakan jumlah padding yang harus dihapus
                    padding_input = int(input("Masukkan panjang padding yang harus dihapus dari setiap kata: "))


                    print("[PLAINTEXT FOUND!]")
                    
                    # Proses dekripsi dengan menghapus padding terlebih dahulu
                    result = vigenere_cipher(text, key, mode, padding_input)

                    print(f"#Result: {text} -> {result}")

        elif input_type == 'file':
            # Membuka file dialog untuk memilih file
            file_path = open_file_dialog()

            if not file_path:
                print("Tidak ada file yang dipilih. Program dihentikan.")
                break

            # Masukkan key untuk enkripsi/dekripsi
            key = input("Masukkan Key: ")

            # Menanyakan panjang padding
            padding_length = int(input("Masukkan panjang padding yang diinginkan untuk setiap kata (0 jika dekripsi): "))

            # Proses file (enkripsi/dekripsi)
            encrypt_decrypt_file(file_path, key, mode, padding_length)

        # Tanyakan apakah ingin mengulang
        restart = input("\nRestart? [Ya | Tidak]: ").strip().lower()

        if restart != 'ya':
            print("Terima Kasih, Sampai Jumpa!")
            break

if __name__ == '__main__':
    main()
