# LAPORAN DEMO TUGAS INDIVIDU: KEAMANAN INFORMASI
**Topik:** Simulasi Komunikasi Dua Arah dengan Enkripsi DES (Manual)

* **Nama:** Raihan Rasyid Ramadhan
* **NRP:** 5025241224
* **Kelas:** Keamanan Informasi B

---

## 1. Deskripsi Umum Sistem
Program yang saya buat adalah simulasi aplikasi *chat* rahasia (*Full-Duplex*) berbasis terminal. Sistem ini terdiri dari dua *node* (Pihak A sebagai Server dan Pihak B sebagai Client) yang berkomunikasi menggunakan protokol **TCP Socket** pada jaringan *localhost*. Seluruh lalu lintas teks antar kedua program ini diamankan menggunakan algoritma **Data Encryption Standard (DES)** yang diimplementasikan secara manual (tanpa *library* pihak ketiga).

## 2. Implementasi Kriptografi (File: `des_manual.py`)
Untuk memenuhi syarat **Tanpa Library Enkripsi Instan**, saya membangun logika algoritma DES murni dari nol. DES bekerja sebagai **Block Cipher** (memproses data per 64-bit / 8 byte). Alur utamanya meliputi:

* **PKCS7 Padding:** Karena DES butuh input kelipatan 8 byte, program saya akan menambahkan *padding* otomatis pada pesan yang panjangnya tidak pas.
* **Key Schedule:** *Pre-Shared Key* akan dikonversi menjadi biner, dilewatkan pada tabel permutasi `PC-1` dan `PC-2`, lalu digeser *(left shift)* untuk menghasilkan **16 Subkey** (anak kunci) berukuran 48-bit.
* **Feistel Network (16 Putaran):** Pesan (64-bit) akan diacak di *Initial Permutation (IP)*, lalu dibelah dua (Kiri dan Kanan). Bagian kanan diekspansi menjadi 48-bit, di-XOR dengan *subkey*, lalu masuk ke tahap **S-Box (Substitution Box)** untuk mengubah nilai secara non-linear menjadi 32-bit. Proses ini diulang 16 kali.

## 3. Arsitektur Komunikasi & Jaringan (File: `server.py` & `client.py`)
Untuk memenuhi kriteria **Penerapan Sistem** (bukan skrip tunggal) dan **Komunikasi Dua Arah**, saya merancang arsitektur berikut:

* **Socket Programming:** Pihak Server melakukan `bind` dan `listen` di port `65432`, sedangkan Client melakukan `connect`. Keduanya terhubung secara fisik/logikal lewat *Local Area Network* (Localhost).
* **Multi-Threading:** Saya menggunakan modul `threading` agar masing-masing program memiliki dua alur kerja secara bersamaan (*Concurrency*).
  * *Thread Utama:* Digunakan untuk menunggu input ketikan dan mengirim (*send*) pesan.
  * *Thread Daemon:* Berjalan di *background* yang bertugas mendengarkan pesan masuk (*receive*). 
  
  Hasilnya, kedua pihak bisa saling mengirim pesan kapan saja tanpa harus bergantian *(Full-Duplex)*.

## 4. Pengelolaan Kunci (Key Management)
Sesuai instruksi soal, kunci tidak boleh dikirimkan lewat transmisi soket. Oleh karena itu, saya menggunakan metode **Symmetric Pre-Shared Key**. 

Kunci dengan nilai `b"SECRET88"` (berukuran tepat 8 byte) sudah saya tulis secara *hardcoded* di dalam program pengirim dan penerima. Dalam skenario dunia nyata, kunci ini diasumsikan sudah didistribusikan secara fisik atau *offline* sebelum komunikasi online dimulai.

## 5. Analisis Output Transmisi (Ciphertext)
Saat program dijalankan dan pesan dikirim, layar penerima akan menampilkan dua proses:

1. **Ciphertext (Format Hex):** Saya mencetak data jaringan mentah dalam bentuk Hexadecimal. Ini adalah representasi dari bit-bit yang sudah diacak (contoh: `8a4f2b9d...`). Tujuannya sebagai **bukti bahwa integritas enkripsi berjalan** (penyadap hanya akan melihat kode acak ini). Selain itu, panjang string Hex-nya pasti kelipatan 16 karakter (karena 1 blok = 64-bit = 8 byte = 16 karakter Hex), membuktikan bahwa sistem *Block Cipher* berjalan dengan baik.
2. **Plaintext:** Setelah deretan byte Hex tersebut masuk ke fungsi `des_decrypt` dan di-*unpad*, pesan rahasia berhasil dipulihkan menjadi *string* utuh yang bisa dibaca.

## 6. Kesimpulan Pemenuhan Syarat Tugas
Secara keseluruhan, sistem ini telah memenuhi kelima syarat tugas yang diberikan:

- [x] **Komunikasi 2 Arah:** Terpenuhi (Berjalan simultan menggunakan Socket TCP & Threading).
- [x] **Pengelolaan Key:** Terpenuhi (Menggunakan *Pre-Shared Key*, tidak dikirim lewat soket).
- [x] **Penerapan Sistem:** Terpenuhi (Dipisah dalam entitas Server dan Client yang dikoneksikan via port jaringan).
- [x] **Bahasa Pemrograman:** Terpenuhi (Python 3).
- [x] **Ketentuan Library:** Terpenuhi (Algoritma DES, S-Box, Permutasi, dan perhitungan bit level blok diimplementasikan secara manual dari nol).
