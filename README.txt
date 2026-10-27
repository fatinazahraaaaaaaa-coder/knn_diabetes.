MODEL SPK KNN - DATA MINING

ISI FOLDER
- app.py: aplikasi Streamlit metode KNN
- data/Data_Mining_KKN.xlsx: dataset Excel yang dikirim
- requirements.txt: pustaka Python yang diperlukan
- run_windows.bat: instalasi dan menjalankan aplikasi di Windows

MENJALANKAN DI WINDOWS
1. Ekstrak ZIP ke sebuah folder.
2. Pastikan Python 3.10 atau lebih baru sudah terpasang dan opsi Add Python to PATH dicentang.
3. Klik dua kali run_windows.bat, atau buka CMD pada folder ini.
4. Jalankan: python -m pip install -r requirements.txt
5. Jalankan: python -m streamlit run app.py
6. Buka alamat Local URL yang ditampilkan, biasanya http://localhost:8501.

MENJALANKAN ONLINE DI STREAMLIT COMMUNITY CLOUD
1. Upload seluruh isi folder ini ke satu repository GitHub.
2. Pastikan app.py, requirements.txt, dan folder data/Data_Mining_KKN.xlsx ikut ter-upload.
3. Di Streamlit Community Cloud, pilih repository dan file app.py.
4. Deploy. Jangan hanya upload app.py; file Excel di folder data juga harus diunggah.

Aplikasi akan mencari Excel berdasarkan lokasi relatif app.py sehingga tidak bergantung pada path komputer tertentu.
Hasil klasifikasi hanya untuk pembelajaran, bukan diagnosis medis.
