# Optimasi Pemilihan Tim Proyek (Branch & Bound)

Sebuah aplikasi berbasis Web untuk menyelesaikan masalah optimasi pemilihan tim menggunakan algoritma **Branch and Bound**. Aplikasi ini bertujuan untuk memilih tepat $k$ orang kandidat dari $n$ kandidat yang tersedia, sedemikian rupa sehingga total biaya (cost) tim tersebut seminimal mungkin dan **tidak melebihi batas anggaran (budget)**.

## Fitur Utama
- **Penemuan Solusi Optimal yang Pasti:** Menggunakan pendekatan *Admissible Heuristic* (Greedy) sebagai fungsi bounding.
- **Transparansi Logika (Expansion Order):** Melacak dan menampilkan langkah demi langkah bagaimana algoritma melakukan *Pruning* (Pemangkasan).
- **Import Data Massal:** Mendukung *upload* dataset menggunakan file Excel (`.xlsx`) dan CSV (`.csv`) untuk pengujian skala besar.
- **FastAPI Backend:** Komputasi tingkat lanjut yang terpusat dan berkecepatan tinggi.

---

## Tech Stack
- **Backend**: Python 3, FastAPI, Uvicorn, Pandas (untuk baca Excel/CSV).
- **Frontend**: Vanilla Web Technologies (HTML5, CSS3, JavaScript murni). Tidak butuh Node.js / NPM.

---

## Panduan Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek secara lokal setelah kamu melakukan `git clone`.

### 1. Persyaratan (Prerequisites)
Pastikan kamu sudah menginstal:
- **Python 3.9** atau yang lebih baru.
- **Git** (untuk clone repositori).

### 2. Setup Backend (Server API)
Buka terminal/command prompt, arahkan ke folder proyek ini, lalu jalankan:

```bash
# 1. Pindah ke folder backend
cd backend

# 2. (Opsional tapi disarankan) Buat Virtual Environment
python -m venv venv
venv\Scripts\activate      # Untuk Windows
# source venv/bin/activate # Untuk Mac/Linux

# 3. Install semua dependensi yang dibutuhkan
pip install -r requirements.txt

# 4. Jalankan server FastAPI menggunakan Uvicorn
python -m uvicorn main:app --reload
```
*Server Backend akan berjalan di `http://localhost:8000`. Biarkan terminal ini tetap terbuka.*

### 3. Setup Frontend (Antarmuka Pengguna)
Karena frontend dibangun menggunakan Vanilla JS, kamu **tidak perlu** menginstal apapun!
- Buka folder `frontend/` melalui File Explorer komputer kamu.
- Klik dua kali (Double-click) pada file **`index.html`** untuk membukanya langsung di *browser* (seperti Chrome/Edge/Firefox).
- *(Alternatif)*: Jika kamu menggunakan VS Code, kamu bisa klik kanan pada `index.html` dan pilih **Open with Live Server**.

---

## Cara Penggunaan Aplikasi
1. Buka halaman `index.html` di browser.
2. **Pilih Preset atau Input Manual:** Kamu bisa mengisikan jumlah kandidat ($n$), ukuran tim ($k$), dan budget secara manual, lalu mengisi biaya satu per satu.
3. **Menggunakan Fitur Import (Rekomendasi):**
   - Siapkan file `.csv` atau `.xlsx`.
   - Pastikan ada kolom yang memuat list angka biaya para kandidat (aplikasi akan secara pintar mencari angka tersebut).
   - Klik tombol **📥 Import Excel/CSV** dan pilih file kamu (kamu bisa memakai `data_dummy.csv` yang sudah ada di repo ini untuk tes).
4. Klik **Jalankan B&B** dan lihat ajaibnya algoritma ini bekerja. Pada bagian bawah, kamu bisa membedah tabel **Urutan Ekspansi Simpul** untuk melihat alasan matematis dari setiap pemangkasan cabang!

---

## Struktur Direktori
```text
 TimProyek_BnB
 ┣ backend/
 ┃  ┣ algorithm/
 ┃  ┃  ┗ branch_bound.py    # Inti algoritma (Logika, Heuristik, Pruning)
 ┃  ┣ main.py               # Router API endpoint (FastAPI)
 ┃  ┗ requirements.txt      # Daftar pustaka Python (Pandas, FastAPI, dll)
 ┣ frontend/
 ┃  ┣ index.html            # Kerangka Web UI
 ┃  ┣ style.css             # Gaya / Desain web
 ┃  ┗ app.js                # Logika fetch API dan rendering UI
 ┣ data_dummy.csv           # File dataset sampel untuk dicoba
 ┗ README.md
```
