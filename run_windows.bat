@echo off
cd /d "%~dp0"
echo ========================================
echo SPK KNN - Instalasi dan Menjalankan App
echo ========================================
python --version
if errorlevel 1 (
  echo Python belum terpasang atau belum masuk PATH.
  echo Instal Python dari https://www.python.org/downloads/ lalu centang Add Python to PATH.
  pause
  exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Instalasi pustaka gagal. Periksa koneksi internet dan pesan error di atas.
  pause
  exit /b 1
)
python -m streamlit run app.py
pause
