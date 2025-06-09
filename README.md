# FXImage_Auto: Generator & Downloader untuk Google ImageFX

![License](https://img.shields.io/badge/license-MIT-purple.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-Selenium-green)

`FXImage_Auto` adalah skrip otomasi yang berfungsi untuk menghasilkan (generate) dan mengunduh gambar secara massal dari layanan AI Google, **ImageFX**. Skrip ini menggunakan Selenium untuk mengontrol browser, memasukkan daftar prompt teks, dan men-download semua gambar yang dihasilkan secara otomatis.

Tujuan utama dari tool ini adalah untuk efisiensi, memungkinkan pengguna men-generate ratusan gambar dari puluhan prompt tanpa perlu intervensi manual.

## ⚠️ Peringatan Penting & Disclaimer

-   **Tidak Resmi**: Ini adalah tool tidak resmi dan tidak berafiliasi dengan Google.
-   **Risiko Perubahan**: Skrip ini bergantung pada struktur HTML/CSS dari website ImageFX. Jika Google mengubah desain websitenya, skrip ini kemungkinan besar akan **berhenti bekerja** sampai selector-nya diperbarui.
-   **Ketentuan Layanan**: Menggunakan otomasi pada layanan Google mungkin melanggar Ketentuan Layanannya. Gunakan dengan hati-hati dan bijaksana. **Risiko ditanggung oleh pengguna.**
-   **Membutuhkan Login**: Skrip ini kemungkinan besar memerlukan sesi browser yang sudah login ke Akun Google yang memiliki akses ke AI Test Kitchen.

## ✨ Fitur

-   **Generasi Massal**: Otomatis memasukkan setiap baris prompt dari file teks.
-   **Download Otomatis**: Secara otomatis mengunduh semua gambar yang berhasil di-generate oleh AI.
-   **Efisien**: Menghemat waktu dari pekerjaan manual mengetik prompt dan mengklik download berulang kali.
-   **Terstruktur**: Menyimpan hasil download ke dalam folder yang rapi.

## ⚙️ Prasyarat

Sebelum memulai, pastikan Anda telah menyiapkan:

1.  **Python 3.8** atau versi yang lebih baru.
2.  **Browser Google Chrome** yang ter-install di komputer Anda.
3.  **ChromeDriver**: Driver ini wajib ada agar Selenium bisa mengontrol Chrome.
    -   Download versi yang **sesuai dengan versi Google Chrome Anda** dari [situs resmi Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
    -   Ekstrak dan letakkan file `chromedriver.exe` (atau `chromedriver` untuk Linux/Mac) di dalam direktori yang sama dengan skrip `ImageFX.py` Anda.

## 🚀 Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/setiaone-tech/FXImage_Auto.git](https://github.com/setiaone-tech/FXImage_Auto.git)
    ```

2.  **Masuk ke direktori proyek:**
    ```bash
    cd FXImage_Auto
    ```

3.  **Install dependensi yang dibutuhkan (Selenium):**
    ```bash
    pip install selenium
    ```

## 📝 Konfigurasi & Cara Menjalankan

1.  **Siapkan Prompt Anda:**
    -   Buka atau buat file `prompts.txt`.
    -   Tulis semua prompt yang Anda inginkan, dengan **satu prompt per baris**.
    -   Contoh isi `prompts.txt`:
        ```txt
        A majestic cat wearing a king's crown, photorealistic
        Cyberpunk city skyline at night with flying cars, synthwave style
        A serene Japanese garden with a koi pond in spring, watercolor painting
        ```

2.  **Login ke Akun Google:**
    -   Sebelum menjalankan skrip, disarankan untuk membuka Google Chrome secara manual dan login ke akun Google Anda yang memiliki akses ke ImageFX. Ini akan memudahkan skrip untuk langsung mengakses layanannya.

3.  **Jalankan Skrip:**
    -   Buka terminal atau command prompt di dalam direktori proyek.
    -   Jalankan perintah berikut:
        ```bash
        python ImageFX.py
        ```

4.  **Biarkan Skrip Bekerja:**
    -   Sebuah jendela browser Chrome baru akan terbuka dan dikontrol oleh skrip.
    -   **PENTING: Jangan tutup atau berinteraksi dengan jendela browser ini.**
    -   Skrip akan menavigasi ke ImageFX, memasukkan prompt pertama, menunggu, mengunduh gambar, lalu melanjutkan ke prompt berikutnya hingga selesai.

5.  **Lihat Hasil:**
    -   Semua gambar yang berhasil diunduh akan tersimpan di dalam folder `downloads` (atau nama folder lain yang ditentukan di dalam skrip).

## 🤝 Kontribusi

Jika Anda menemukan bug, memiliki ide untuk perbaikan, atau ingin mengoptimalkan skrip, silakan buka *Issue* atau kirim *Pull Request*.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).
