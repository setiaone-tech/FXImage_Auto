import tkinter as tk
from tkinter import ttk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import datetime  # Import untuk membandingkan tanggal
import os
import sys

# Pastikan PyInstaller dapat menemukan tkcalendar
if getattr(sys, 'frozen', False):  # Jika aplikasi berjalan dalam mode .exe
    os.environ['PYTHONPATH'] = sys._MEIPASS

# Fungsi untuk mengenkripsi pesan
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    return base64.b64encode(cipher.iv + ciphertext).decode()

# Fungsi untuk enkripsi ROT13
def rot13(text):
    result = []
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            shifted = (ord(char) - base + 13) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)

# Kunci AES (16 byte untuk AES-128)
key = b'test_test_123_12'

# Fungsi untuk memproses tanggal yang dipilih
def process_date():
    # Ambil nilai dari combobox
    selected_year = year_combobox.get()
    selected_month = month_combobox.get()
    selected_day = day_combobox.get()

    # Gabungkan menjadi format tanggal
    selected_date_str = f"{selected_year}-{selected_month}-{selected_day}"

    today = datetime.date.today()  # Ambil tanggal hari ini

    # Validasi: Tidak boleh memilih tanggal sebelum hari ini
    try:
        selected_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        if selected_date < today:
            result_label.config(text="❌ Error: Tanggal sudah lewat!", foreground="red")
            return  # Stop proses enkripsi jika tanggal sudah lewat
        
        # Format tanggal ke string YYYYMMDD
        formatted_date = selected_date.strftime("%Y%m%d")

        # Enkripsi tanggal
        encrypted_message = encrypt_message(key, formatted_date)  # Enkripsi AES
        encrypted_rot13 = rot13(encrypted_message)  # Enkripsi ROT13

        # Tampilkan hasil dengan interaksi klik
        result_label.config(text=f"License: {encrypted_rot13}", foreground="blue", cursor="hand2")
        result_label.license_text = encrypted_rot13  # Simpan teks untuk clipboard
    except ValueError:
        result_label.config(text="❌ Format tanggal salah!", foreground="red")


# Fungsi untuk menyalin teks ke clipboard saat label diklik
def copy_to_clipboard(event):
    license_text = result_label.license_text
    if license_text:
        root.clipboard_clear()
        root.clipboard_append(license_text)
        root.update()
        result_label.config(text="✅ Copied!", foreground="green")
        root.after(1000, lambda: result_label.config(text=f"License: {license_text}", foreground="blue"))  # Kembali ke teks asli


# Inisialisasi Tkinter
root = tk.Tk()
root.geometry("600x400")
root.title("License Generator ImageFX Automation")

# Label
ttk.Label(root, text="Pilih Tanggal:").pack(pady=5)

# Frame untuk input tanggal (menggunakan pack dengan side="left")
date_frame = ttk.Frame(root)
date_frame.pack(pady=5)

# Combobox untuk memilih tahun
year_combobox = ttk.Combobox(date_frame, values=[str(year) for year in range(2000, 2031)], width=10)
year_combobox.set(str(datetime.datetime.now().year))  # Set default year to the current year
year_combobox.pack(side="left", padx=5)

# Combobox untuk memilih bulan
month_combobox = ttk.Combobox(date_frame, values=[f"{month:02d}" for month in range(1, 13)], width=5)
month_combobox.set(f"{datetime.datetime.now().month:02d}")  # Set default month to current month
month_combobox.pack(side="left", padx=5)

# Combobox untuk memilih hari
day_combobox = ttk.Combobox(date_frame, values=[f"{day:02d}" for day in range(1, 32)], width=5)
day_combobox.set(f"{datetime.datetime.now().day:02d}")  # Set default day to the current day
day_combobox.pack(side="left", padx=5)

# Tombol untuk memproses
encrypt_button = ttk.Button(root, text="Generate", command=process_date)
encrypt_button.pack(pady=5)

# Label hasil (bisa diklik untuk salin)
result_label = ttk.Label(root, text="License: -", foreground="black", cursor="hand2")
result_label.pack(pady=10)

# Tambahkan event listener untuk klik (agar hasil bisa disalin ke clipboard)
result_label.bind("<Button-1>", copy_to_clipboard)

# Jalankan aplikasi Tkinter
root.mainloop()
