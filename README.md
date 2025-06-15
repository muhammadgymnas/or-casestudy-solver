# 📊 Linear Programming Solver Dashboard

Sebuah aplikasi web interaktif yang dibuat dengan Streamlit untuk menyelesaikan masalah *Linear Programming* (LP) menggunakan metode Simplex. Aplikasi ini menyediakan solusi optimal untuk masalah alokasi sumber daya dan perencanaan produksi.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://or-casestudy-solver.streamlit.app/)  ![Screenshot Aplikasi](https://i.ibb.co/SwrKyPR8/OR-Case-Study-Solver-App-Screenshot.jpg) 

## ✨ Fitur Utama

- **Solver Interaktif**: Ubah parameter input seperti koefisien fungsi tujuan, batasan, dan kapasitas secara *real-time*.
- **Dua Model LP**: Menyelesaikan dua studi kasus:
    - **Problem 13.8-5**: Perencanaan Produksi (Maksimalkan Profit)
    - **Problem 13.8-9**: Alokasi Sumber Daya (Maksimalkan Output dengan Batasan Anggaran)
- **Visualisasi Hasil**: Hasil optimisasi ditampilkan dalam bentuk tabel dan grafik (bar chart & pie chart) yang mudah dipahami menggunakan Plotly.
- **Antarmuka Modern**: UI yang bersih dan responsif dengan tema gelap dan CSS kustom.
- **Dukungan Multi-bahasa**: Beralih antara Bahasa Inggris dan Bahasa Indonesia dengan mudah langsung dari sidebar.

## 🛠️ Teknologi yang Digunakan

- **Framework**: Streamlit
- **Backend & komputasi**: Python, SciPy (`linprog`), NumPy, Pandas
- **Visualisasi**: Plotly

## 🚀 Cara Menjalankan Secara Lokal

Untuk menjalankan aplikasi ini di komputer Anda, ikuti langkah-langkah berikut:

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/muhammadgymnas/or-casestudy-solver.git
    cd NAMA_REPOSITORI_ANDA
    ```

2.  **Buat dan aktifkan virtual environment (opsional tapi disarankan):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
    ```

3.  **Install semua pustaka yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi Streamlit:**
    ```bash
    streamlit run app.py  # Ganti 'app.py' jika nama file utama Anda berbeda
    ```

## ☁️ Deployment di Streamlit Community Cloud

Aplikasi ini siap untuk di-deploy.

1.  **Push** kode Anda ke repositori GitHub ini.
2.  Pastikan file **`requirements.txt`** ada di dalam repositori.
3.  Buka [Streamlit Community Cloud](https://share.streamlit.io/).
4.  Klik **"New app"** dan hubungkan ke repositori GitHub ini.
5.  Pilih branch (misal: `main`) dan file utama (misal: `app.py`).
6.  Klik **"Deploy!"** dan aplikasi Anda akan online dalam beberapa menit.

---
*Dibuat dengan ❤️ oleh muhammadgymnas*
