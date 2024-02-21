# to build run clone the repo, cd into the folder and run

# on windows
```
git clone https://github.com/coffandro/RosePlayerManager.git
cd RosePlayerManager

python -m venv .venv
call .venv\Scripts\activate.bat

python -m pip install -r requirements.txt
python -m pip install -U pyinstaller

python ICOConvert.py Icons/
python ImageDownscaler.py Images/src/ Images/ 1920 1080
pyinstaller "RosePlayerManager.spec"

call .venv\Scripts\deactivate.bat
```
then move the files inside dist/RosePlayerManager wherever you want (They have to be in the same folder though)
and run the .exe