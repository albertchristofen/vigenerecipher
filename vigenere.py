import os
import random
import string
import tkinter as tk
from tkinter import filedialog

def add_padding_to_word(word, padding_length):
    """Menambahkan padding ke setiap kata dengan karakter acak."""
    padding = ''.join(random.choices(string.ascii_lowercase, k=padding_length)) 
    return word + padding

def remove_padding_from_word(word, padding_length):
    """Menghapus padding dari setiap kata."""
    return word[:-padding_length] if padding_length > 0 else word

def vigenere_cipher(text, key, mode='encrypt', padding_length=0):
    """Enkripsi atau dekripsi dengan cipher Vigenere, menyisipkan karakter '0', dan menambahkan/mengurangi padding."""
    result = []
    key = key.upper()  # Kunci tetap dalam huruf besar
    key_index = 0

    if mode == 'encrypt':
        # Gantikan setiap spasi dengan karakter '0'
        text = text.replace(' ', '0')
        words = text.split('0')  # Pisahkan berdasarkan '0'
        for word in words:
            word_result = []
            for char in word:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)]) - ord('A')  # Hitung pergeseran dari kunci

                    # Karakter baru tetap mengikuti case huruf asli (lower atau upper)
                    if char.islower():
                        new_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
                    else:
                        new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))

                    word_result.append(new_char)
                    key_index += 1
                else:
                    word_result.append(char)  # Karakter non-alphabet tidak diubah

            word_result = ''.join(word_result)

            if mode == 'encrypt':
                word_result = add_padding_to_word(word_result, padding_length)

            result.append(word_result)

        # Gabungkan kembali hasilnya menjadi satu string setelah enkripsi
        result_text = '0'.join(result)

    elif mode == 'decrypt':
        # Pisahkan berdasarkan '0' untuk pemrosesan blok
        words = text.split('0')  # Pisahkan berdasarkan '0' (yang menggantikan spasi)
        
        for word in words:
            if word:
                # Hapus padding terlebih dahulu pada dekripsi
                word = remove_padding_from_word(word, padding_length)
                word_result = []
                for char in word:
                    if char.isalpha():
                        shift = ord(key[key_index % len(key)]) - ord('A')  # Hitung pergeseran dari kunci

                        if mode == 'decrypt':
                            shift = -shift  # Balik pergeseran untuk dekripsi

                        # Karakter baru tetap mengikuti case huruf asli (lower atau upper)
                        if char.islower():
                            new_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
                        else:
                            new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))

                        word_result.append(new_char)
                        key_index += 1
                    else:
                        word_result.append(char)  # Karakter non-alphabet tidak diubah
                result.append(''.join(word_result))
        
        # Gabungkan kembali hasilnya menjadi satu string setelah dekripsi
        result_text = ' '.join(result)

    return result_text

def encrypt_decrypt_file(file_path, key, mode, padding_length=0):
    """Proses enkripsi/dekripsi untuk file."""
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
    """Membuka dialog file untuk memilih file."""
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
        input_type = input("Masukkan Pilihan Anda\n[1] Manual | [2] File: ").strip().lower()

        # Validasi input
        while input_type not in ['1', '2']:
            input_type = input("Input Anda Salah. Masukkan pilihan [1] Manual atau [2] File: ").strip().lower()

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
            print("\n*Decrypting ...\n")

        if input_type == '1':
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

                # Menentukan panjang padding otomatis
                padding_length = len(key) - 2

                # Proses cipher
                result = vigenere_cipher(text, key, mode, padding_length)

                # Menampilkan hasil
                if mode == 'encrypt':
                    print(f"\nHasil Encrypt: {result}")
                else:
                    print(f"\nHasil Decrypt: {result}")

        elif input_type == '2':
            # Membuka file dialog untuk memilih file
            file_path = open_file_dialog()

            if not file_path:
                print("Tidak ada file yang dipilih. Program dihentikan.")
                break

            # Masukkan key untuk enkripsi/dekripsi
            key = input("Masukkan Key: ")

            # Menentukan panjang padding otomatis
            padding_length = len(key) - 2
            print(f"Panjang padding otomatis dihitung: {padding_length}")

            # Proses file (enkripsi/dekripsi)
            encrypt_decrypt_file(file_path, key, mode, padding_length)

        # Tanyakan apakah ingin mengulang
        restart = input("\nRestart? [1] Ya | [2] Tidak: ").strip().lower()

        while restart not in ['1', '2']:
            restart = input("Input Anda Salah. Masukkan pilihan [1] untuk Ya atau [2] untuk Tidak: ").strip().lower()

        if restart == '2':
            print("Terima Kasih, Sampai Jumpa!")
            break

if __name__ == '__main__':
    main()
