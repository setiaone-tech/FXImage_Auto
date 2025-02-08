import tkinter as tk
from tkinter import Frame, Label, Entry, Button, filedialog, Text, messagebox, ttk
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import shutil
import time
import sys
from win32com.client import Dispatch
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import threading  # Import threading module
from PIL import Image, ImageTk

# Fungsi untuk memastikan path yang benar
def resource_path(relative_path):
    """ Dapatkan path absolut untuk file eksternal, mendukung mode .exe dan skrip biasa """
    if getattr(sys, 'frozen', False):  # Jika berjalan dalam mode PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Fungsi untuk enkripsi/dekripsi ROT13
def rot13(text):
    result = []
    for char in text:
        if char.isalpha():  # Hanya huruf yang diubah
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            shifted = (ord(char) - base + 13) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    
    return ''.join(result)

# Fungsi untuk mendekripsi pesan
def decrypt_message(key, encrypted_message):
    encrypted_data = base64.b64decode(encrypted_message)
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return decrypted_message

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageFX Automation")
        self.root.geometry("800x600")
        logo_path = resource_path("logo.png")
        icon = tk.PhotoImage(file=logo_path)
        self.root.iconphoto(True, icon)
        
        # Warna untuk menu aktif dan tidak aktif
        self.active_color = "#007ACC"
        self.inactive_color = "#CCCCCC"
        
        # Frame untuk menu bar
        self.menu_frame = tk.Frame(self.root, bg=self.inactive_color, height=40)
        self.menu_frame.pack(fill=tk.X)
        
        # Membuat menu bar
        self.menus = {}
        menu_items = ["ImageFX", "Chrome Profile", "License"]
        
        for menu in menu_items:
            label = tk.Label(self.menu_frame, text=menu, padx=20, pady=10, bg=self.inactive_color, fg="white", cursor="hand2")
            if menu == 'ImageFX':
                label.bind("<Button-1>", lambda e, page=menu: self.dummy_function(e))  # Placeholder, akan diaktifkan nanti
            else:
                label.bind("<Button-1>", lambda e, page=menu: self.show_page(page))
            label.pack(side=tk.LEFT, fill=tk.Y)
            self.menus[menu] = label
        
        # Frame untuk konten
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill=tk.BOTH)
        
        # Dictionary untuk halaman
        self.pages = {}
        
        # Membuat halaman-halaman
        self.create_imagefx_page()
        self.create_chrome_profile_page()
        self.create_license_page()
        
        # Cek apakah file .license ada dan update status ImageFX
        self.check_license()
        
        # Tampilkan halaman pertama berdasarkan status lisensi
        self.show_page("ImageFX" if self.license_exists else "License")
    
    def dummy_function(self, e):
        pass  # Tidak melakukan apa-apa, digunakan untuk ImageFX yang tidak aktif
    
    def create_page(self, name, text):
        page = Frame(self.content_frame)
        label = Label(page, text=text, font=("Arial", 14))
        label.pack(pady=20)
        self.pages[name] = page
    
    def disable_all(self):
        self.chrome_profile.config(state="disabled")
        self.download_location.config(state="disabled")
        self.jumlah_pict.config(state="disabled")
        self.headless_checkbox.config(state="disabled")
        self.profile_button.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.prompt_text.config(state="disabled")
        self.generate_button.config(state="disabled")
    
    def enable_all(self):
        self.chrome_profile.config(state="normal")
        self.download_location.config(state="normal")
        self.jumlah_pict.config(state="readonly")
        self.headless_checkbox.config(state="normal")
        self.profile_button.config(state="normal")
        self.browse_button.config(state="normal")
        self.prompt_text.config(state="normal")
        self.generate_button.config(state="normal")
    
    def create_imagefx_page(self):
        page = Frame(self.content_frame)
        Label(page, text="Pilih Chrome Profile (Directory):").pack(anchor='w', padx=10, pady=2)
        self.chrome_profile = Entry(page)
        self.chrome_profile.pack(fill='x', padx=10, pady=2)
        self.profile_button = Button(page, text="Browse", command=self.browse_chrome_profile)
        self.profile_button.pack(padx=10, pady=2)
        Label(page, text="Pilih Lokasi Download:").pack(anchor='w', padx=10, pady=2)
        self.download_location = Entry(page)
        self.download_location.pack(fill='x', padx=10, pady=2)
        self.browse_button = Button(page, text="Browse", command=self.browse_location)
        self.browse_button.pack(padx=10, pady=2)
        choices = [1, 2, 3, 4]
        Label(page, text="Jumlah gambar (tiap prompt):").pack(anchor='w', padx=10, pady=2)
        self.jumlah_pict = ttk.Combobox(page, values=choices, state="readonly")  # state="readonly" mencegah pengeditan
        self.jumlah_pict.set(choices[0])  # Set default value
        self.jumlah_pict.pack(anchor='w', padx=10, pady=2)
        Label(page, text="Prompt:").pack(anchor='w', padx=10, pady=2)
        self.prompt_text = Text(page, height=5)
        self.prompt_text.pack(fill='x', padx=10, pady=2)

        # Checkbox untuk "Headless"
        self.headless_var = tk.BooleanVar(value=False)  # Default: False (tidak headless)
        self.headless_checkbox = tk.Checkbutton(page, text="Headless", variable=self.headless_var, anchor='w')
        self.headless_checkbox.pack(fill='x', padx=10, pady=2)
        
        button_frame = Frame(page)
        button_frame.pack(pady=10, fill='x')  # Mengatur fill 'x' untuk memenuhi lebar frame

        # Tombol Generate
        self.generate_button = Button(button_frame, text="Generate", bg="green", fg="white", 
            command=self.run_selenium_thread)
        self.generate_button.pack(side='left', fill='both', expand=True)

        # Tombol Stop
        Button(button_frame, text="Stop", bg="red", fg="white", 
            command=self.stop_selenium).pack(side='left', fill='both', expand=True)
        
        Label(page, text="Status :").pack(anchor='w', padx=10, pady=2)
        self.output_label = Label(page, bg="#F0F0F0", width=10, height=1, anchor='w')
        self.output_label.pack(fill='x', padx=20, pady=5)
        self.output_label.config(text="READY")

        Label(page, text="Output Hasil Gambar:").pack(anchor='w', padx=10, pady=2)
        # Frame utama untuk scrollable area (Canvas)
        self.canvas_frame = tk.Frame(page)
        self.canvas_frame.pack(fill="both", expand=True, pady=10)

        # Canvas untuk menampilkan gambar dengan scrollbars
        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar vertikal
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Frame dalam canvas untuk menampung gambar
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.images = []  # Untuk menyimpan path gambar
        self.image_labels = []  # Untuk menyimpan referensi label gambar
        
        self.pages["ImageFX"] = page

        self.driver = None  # driver untuk menyimpan instance Selenium WebDriver
        self.selenium_thread = None  # thread untuk menjalankan Selenium
        self.stop_event = threading.Event()  # Event untuk menghentikan thread secara eksplisit
    
    def stop_selenium(self):
        self.enable_all()
        self.output_label.config(text="Progress Stop")
        # Set stop_event untuk memberitahu thread Selenium untuk berhenti
        if self.driver:
            self.stop_event.set()  # Set stop_event agar thread Selenium berhenti

        # Hentikan thread Selenium jika berjalan
        if self.selenium_thread and self.selenium_thread.is_alive():
            self.selenium_thread = None  # Nonaktifkan thread agar tidak mengganggu UI Tkinter

        # Pastikan driver ditutup segera
        if self.driver:
            self.driver.quit()
            self.driver = None

        # Reset event setelah penghentian
        self.stop_event.clear()
    
    def run_selenium_thread(self):
        # Menjalankan fungsi Selenium di thread terpisah
        self.disable_all()
        self.selenium_thread = threading.Thread(target=self.run_selenium)
        self.selenium_thread.start()

    def display_images(self):
        # Menampilkan gambar satu per satu dalam 5 kolom
        row = 0
        col = 0
        for image_path in self.images:
            img = Image.open(image_path)

            # Tentukan width baru yang diinginkan
            new_width = 150

            # Hitung rasio aspek
            aspect_ratio = img.width / img.height

            # Hitung height berdasarkan rasio aspek
            new_height = int(new_width / aspect_ratio)

            # Resize gambar dengan width tetap dan height dihitung
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)

            # Membuat label untuk menampilkan gambar
            label = tk.Label(self.image_frame, image=img_tk)
            label.image = img_tk  # Menyimpan referensi gambar agar tidak hilang

            # Tentukan posisi label dalam grid
            label.grid(row=row, column=col, padx=5, pady=5)

            # Simpan referensi label agar bisa dihapus nanti
            self.image_labels.append(label)

            # Update kolom dan baris untuk layout 5 kolom
            col += 1
            if col == 5:  # Jika sudah mencapai 5 kolom, pindah ke baris berikutnya
                col = 0
                row += 1

        # Perbarui ukuran canvas agar sesuai dengan jumlah gambar yang ditampilkan
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Update area scrollable
    
    def run_selenium(self):
        # Ambil input dari pengguna
        profile_dir = self.chrome_profile.get()
        download_dir = self.download_location.get()
        prompt = self.prompt_text.get("1.0", tk.END)
        
        if not profile_dir or not download_dir:
            print("Pastikan semua input diisi")
            return
        
        # Setup opsi Chrome untuk undetected_chromedriver
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={profile_dir}")  # Tentukan profil Chrome
        options.add_argument(f"–-profile-directory=Default")  # Gunakan profil Default (atau sesuaikan jika diperlukan)
        
        # Tentukan lokasi download menggunakan opsi Chrome
        options.add_argument(f"--download.default_directory={download_dir}")

        # Jika checkbox headless dicentang, tambahkan opsi --headless
        if self.headless_var.get():
            options.add_argument("--headless")  # Menjalankan Selenium dalam mode headless
        
        # Jalankan WebDriver menggunakan undetected_chromedriver
        try:
            self.driver = uc.Chrome(options=options)
            
            # Arahkan ke halaman yang diinginkan (Anda dapat mengubah URL sesuai kebutuhan)
            self.output_label.config(text="Progress")
            url = "https://labs.google/fx/tools/image-fx"  # Ganti dengan halaman yang sesuai
            self.driver.get(url)
            
            # Tunggu beberapa detik agar halaman dimuat sepenuhnya (atau sesuaikan dengan kebutuhan)
            time.sleep(5)

            self.output_label.config(text="Opening Browser")
            try:
                # Menunggu elemen dengan XPath pertama untuk muncul dan klik
                xpath1 = "//div[@id='__next']/div/div/div/div[2]/div[2]/div/span/button/span[2]"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath1)))
                
                # Temukan elemen pertama dan klik
                button1 = self.driver.find_element(By.XPATH, xpath1)
                button1.click()
            except:
                pass
            
            try:
                # Tunggu sampai tombol sign-in muncul dan klik tombol tersebut
                xpath2 = "//button[@id='sign-in-now-button']/span"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath2)))
                
                # Temukan tombol sign-in dan klik
                sign_in_button = self.driver.find_element(By.XPATH, xpath2)
                sign_in_button.click()
            except:
                pass

            try:
                # Menunggu sampai elemen div dengan role="textbox" muncul dan klik
                xpath4 = "//div[@role='textbox']"  # XPath untuk mencari div dengan role="textbox"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath4)))
                
                # Temukan elemen div dengan role="textbox" dan klik
                textbox_div = self.driver.find_element(By.XPATH, xpath4)
                textbox_div.click()  # Klik terlebih dahulu
            except:
                pass
            
            self.output_label.config(text="Getting Prompt")
            # Setelah klik, masukkan teks dari prompt ke dalam div yang berperan sebagai textbox
            if prompt:
                prompts = prompt.split('\n')
                for prompt in prompts:
                    if prompt != '':
                        self.output_label.config(text=f"Generate Image '{prompt}'")
                        teks = textbox_div.text
                        if teks:
                            # Mengirimkan backspace untuk menghapus seluruh teks
                            for _ in range(len(teks)):
                                textbox_div.send_keys(Keys.BACKSPACE)
                            time.sleep(1)  # Memberikan waktu sejenak untuk penghapusan
                        textbox_div.send_keys(prompt)  # Kirimkan teks dari promp
                        try:
                            # Cari elemen berdasarkan XPath
                            button_element = self.driver.find_element(By.XPATH, "//div[@id='__next']/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/button/div")

                            # Klik elemen tersebut
                            button_element.click()
                        except:
                            pass

                        # Cari semua tag img yang memiliki class "sc-cfbb9832-1 gMwDLy"
                        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.sc-cfbb9832-1.gMwDLy")))
                        img_elements = self.driver.find_elements(By.CSS_SELECTOR, "img.sc-cfbb9832-1.gMwDLy")


                        # Periksa apakah ada gambar yang ditemukan
                        max = int(self.jumlah_pict.get())
                        loop = 0
                        if img_elements:
                            # Loop untuk memproses setiap gambar
                            for idx, img_element in enumerate(img_elements):
                                if loop == max:
                                    break
                                # Ambil data src yang berisi base64
                                self.output_label.config(text="Showing Image")
                                img_base64 = img_element.get_attribute("src")

                                # Pastikan gambar menggunakan base64 encoding
                                if img_base64.startswith("data:image/jpg;base64,"):
                                    # Hapus prefix data:image/png;base64,
                                    img_base64 = img_base64.split("base64,")[1]

                                    # Dekode base64 menjadi byte data
                                    img_data = base64.b64decode(img_base64)

                                    # Tentukan nama file gambar yang akan disimpan (menambahkan nomor urut untuk file berbeda)
                                    file_path = f"{self.download_location.get()}/{prompt}_{idx + 1}.png"
                                    
                                    # Simpan byte data ke file gambar
                                    with open(file_path, "wb") as f:
                                        f.write(img_data)
                                    self.images.append(file_path)
                                    self.display_images()
                                    loop += 1
                                    
                        else:
                            print("nothing")

                        # Tunggu beberapa detik sebelum menutup browser
                        time.sleep(5)
            
            self.driver.quit()
            
            # Anda bisa menambahkan interaksi dengan halaman web, seperti mengisi formulir, klik tombol, dll.
            # Contoh interaksi:
            # search_box = driver.find_element(By.NAME, "q")
            # search_box.send_keys("query")
            # search_box.submit()
            
            # Menampilkan hasil atau mengambil gambar, misalnya:
            self.output_label.config(text="Success")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.driver.quit()
    
    def browse_chrome_profile(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.chrome_profile.delete(0, tk.END)
            self.chrome_profile.insert(0, folder_selected)
    
    def browse_location(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_location.delete(0, tk.END)
            self.download_location.insert(0, folder_selected)
    
    def create_chrome_profile_page(self):
        page = Frame(self.content_frame)
        Label(page, text="Pilih Folder Penyimpanan Profile:").pack(anchor='w', padx=10, pady=2)
        self.profile_path = Entry(page)
        self.profile_path.pack(fill='x', padx=10, pady=2)
        Button(page, text="Browse", command=self.browse_profile_path).pack(padx=10, pady=2)
        Label(page, text="Nama Profile:").pack(anchor='w', padx=10, pady=2)
        self.profile_name = Entry(page)
        self.profile_name.pack(fill='x', padx=10, pady=2)
        Button(page, text="Create Profile", command=self.create_chrome_profile).pack(pady=10)
        self.pages["Chrome Profile"] = page
    
    def browse_profile_path(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.profile_path.delete(0, tk.END)
            self.profile_path.insert(0, folder_selected)
    
    def create_chrome_profile(self):
        profile_dir = self.profile_path.get()
        profile_name = self.profile_name.get()
        
        if profile_dir and profile_name:
            user_data_dir = os.path.join(profile_dir, profile_name)
            options = uc.ChromeOptions()
            options.add_argument(f"--user-data-dir={user_data_dir}")
            self.driver = uc.Chrome(options=options)
            self.driver.quit()
            # Setelah Chrome driver selesai, buat shortcut
            self.create_shortcut(user_data_dir, profile_name, profile_dir)
    
    def create_shortcut(self, user_data_dir, profile_name, profile_dir):
        # Path ke aplikasi Chrome
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        
        # Jika tidak ditemukan, coba menggunakan path executable yang ada di system PATH
        if not os.path.exists(chrome_path):
            chrome_path = shutil.which("chrome")
        
        if not chrome_path:
            print("Chrome executable tidak ditemukan!")
            return
        
        # Path untuk shortcut yang akan disimpan di direktori profile yang telah ditentukan
        shortcut_path = os.path.join(profile_dir, f"Chrome - {profile_name}.lnk")
        
        # Membuat shortcut menggunakan WScript.Shell
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        
        # Menetapkan properti shortcut
        shortcut.TargetPath = chrome_path
        shortcut.Arguments = f"--user-data-dir=\"{user_data_dir}\" --profile-directory=\"{profile_name}\""
        shortcut.WorkingDirectory = os.path.dirname(chrome_path)  # Tentukan working directory
        shortcut.Save()  # Simpan shortcut

        print(f"Shortcut untuk {profile_name} telah dibuat di {shortcut_path}")
    
    def create_license_page(self):
        page = Frame(self.content_frame)
        Label(page, text="License Program:").pack(anchor='w', padx=10, pady=2)
        self.license_input = Entry(page)
        self.license_input.pack(fill='x', padx=10, pady=2)
        Button(page, text="Send License", command=self.send_license).pack(pady=10)
        self.timer_label = Label(page, text="Waktu Sisa: ", font=("Arial", 14))
        self.timer_label.pack(pady=10)
        self.pages["License"] = page
        self.update_timer()
    
    def send_license(self):
        license_path = os.path.join(os.getcwd(), '.license')
        license_content = self.license_input.get()
        if license_content:
            try:
                with open(license_path, 'w') as file:
                    file.write(license_content)
                self.check_license()
                self.update_timer()
            except Exception as e:
                print(f"Error saving license: {e}")
        else:
            print("License cannot be empty")
    
    def check_license(self):
        license_path = os.path.join(os.getcwd(), '.license')
        
        # Cek apakah file lisensi ada
        if not os.path.exists(license_path):
            self.license_exists = False
            self.set_imagefx_inactive()
            return
        
        try:
            # Baca file lisensi
            with open(license_path, 'r') as f:
                data_license = f.read()
            
            # Dekripsi dan proses tanggal lisensi
            data_license = decrypt_message(b'test_test_123_12', rot13(data_license))
            
            year = int(data_license[:4])
            month = int(data_license[4:6])
            day = int(data_license[6:])
            end_date = datetime.datetime(year, month, day)
            
            # Hitung waktu yang tersisa
            remaining_time = end_date - datetime.datetime.now()
            
            if remaining_time.days >= 0:  # Lisensi masih berlaku
                self.license_exists = True
                self.set_imagefx_active()
            else:  # Lisensi telah kadaluarsa
                self.license_exists = False
                self.set_imagefx_inactive()
                messagebox.showwarning("Lisensi Kadaluarsa", "Lisensi Anda telah kadaluarsa!")
        
        except Exception as e:
            print(f"Error checking license: {e}")
            self.license_exists = False
            self.set_imagefx_inactive()
    
    def set_imagefx_active(self):
        self.menus["ImageFX"].bind("<Button-1>", lambda e, page="ImageFX": self.show_page(page))  # Aktifkan klik pada ImageFX
    
    def set_imagefx_inactive(self):
        self.menus["ImageFX"].bind("<Button-1>", lambda e, page="dummy": self.dummy_function(e))  # Non-aktifkan klik pada ImageFX
        self.menus["ImageFX"].config(bg=self.inactive_color)
    
    def update_timer(self):
        if not os.path.exists('.license'):
            return
        
        try:
            with open('.license') as f:
                data_license = f.read()
            
            data_license = decrypt_message(b'test_test_123_12', rot13(data_license))
            year = int(data_license[:4])
            month = int(data_license[4:6])
            day = int(data_license[6:])
            end_date = datetime.datetime(year, month, day)
            remaining_time = end_date - datetime.datetime.now()
            
            if remaining_time.days < 0:
                os.remove('.license')
                self.check_license()
                return
            
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_left = f"{days} hari, {hours} jam, {minutes} menit, {seconds} detik"
            self.timer_label.config(text=f"Waktu Sisa: {time_left}")
        
        except Exception as e:
            print(f"Error updating timer: {e}")
        
        self.root.after(1000, self.update_timer)
    
    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(expand=True, fill=tk.BOTH)
        for menu, label in self.menus.items():
            label.config(bg=self.active_color if menu == name else self.inactive_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
