@echo off
echo [INFO] Installing PyInstaller if not already installed...
pip install pyinstaller --quiet

echo [INFO] Compiling HackerDoomsday...

pyinstaller --noconfirm --onefile --windowed ^
    --icon="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\appicon.ico" ^
    --add-data="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\resources;resources" ^
    --add-data="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\gui.py;." ^
    --add-data="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\multimedia.py;." ^
    --add-data="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\gdi.py;." ^
    --add-data="C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\start_gdi.py;." ^
    --collect-all moviepy ^
    --collect-all imageio ^
    --collect-all imageio_ffmpeg ^
    --collect-all proglog ^
    --collect-all pygame ^
    --hidden-import="PIL._tkinter_finder" ^
    --hidden-import="win32gui" ^
    --hidden-import="win32con" ^
    --hidden-import="win32api" ^
    --hidden-import="win32ui" ^
    --hidden-import="psutil" ^
    --name="HackerDoomsday" ^
    "C:\Users\Owner\Downloads\BlooketFlooder-master\HackerDoomsday-main\main.py"

echo [INFO] Done! Your exe is in the dist folder.
pause