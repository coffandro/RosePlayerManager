rmdir /S /Q .venv/
rmdir /S /Q __pycache__/

python venv .venv

python ICOConvert.py Icons/
python -m PyInstaller --noconfirm --onedir --icon=Icons/Rose256.png --add-data "C:\Users\Cornelius\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\customtkinter;customtkinter\" --add-data "RosePlayerGUI.py;." "RosePlayerManager.py"