rm -r build
rm -r dist
rm -r __pycache__
rm RosePlayerManager.spec
python3 ICOConvert.py Icons/
python3 ImageDownscaler.py Images/ 1920 1080
python3 -m pip install Linux-requirements.txt
python3 -m PyInstaller --noconfirm --onedir --windowed --add-data="/home/cornelius/.local/lib/python3.10/site-packages/customtkinter:customtkinter/" --icon="Icons/Rose256.ico" --add-data="Icons/*:." "RosePlayerManager.py"
chmod a+x dist/RosePlayerManager/RosePlayerManager
./dist/RosePlayerManager/RosePlayerManager