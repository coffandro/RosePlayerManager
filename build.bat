rmdir /S /Q .venv/*
rmdir /S /Q build/*
rmdir /S /Q dist/*
rmdir /S /Q __pycache__/*

python -m venv .venv

.venv\Scripts\python.exe -m pip install -r requirements.txt

.venv\Scripts\python.exe ICOConvert.py Icons/
.venv\Scripts\python.exe ImageDownscaler.py Images/ 1920 1080

# python -m PyInstaller --noconfirm --onedir --icon=Icons/Rose256.png --add-data "C:\Users\Cornelius\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\customtkinter;customtkinter\" --add-data "RosePlayerGUI.py;." "RosePlayerManager.py"
.venv\Scripts\python.exe -m PyInstaller --noconfirm --onedir "RosePlayerManager.py"

dist\RosePlayerManager\RosePlayerManager.exe -H