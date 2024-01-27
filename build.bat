rmdir /S /Q .venv
rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q __pycache__
del /Q RosePlayerManager.spec

python -m venv .venv

call .venv\Scripts\activate.bat

python -m pip install -r requirements.txt
python -m pip install -U pyinstaller

python ICOConvert.py Icons/
python ImageDownscaler.py Images/ 1920 1080

pyinstaller --noconfirm --onedir --icon "Icons/Rose256.ico" --add-data "Icons/*;." "RosePlayerManager.py"

call .venv\Scripts\deactivate.bat

dist\RosePlayerManager\RosePlayerManager.exe