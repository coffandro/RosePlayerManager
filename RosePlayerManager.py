import sys
from colorama import Fore
import RosePlayerGUI as GUI
import RosePlayerPlaying as Playing
import getopt
import pystray
import RosePlayerFuncs as Global
from PIL import Image
import threading

args = sys.argv[1:]
if Global.IsBundled():
    image = Image.open("_internal/Icons/Rose256.png")
else:
    image = Image.open("Icons/Rose256.png")
state = ""

Global.Search_Ports()


def after_click(icon, query):
    if str(query) == "Open":
        app = GUI.App()
        app.mainloop()
    elif str(query) == "Exit":
        exit()


icon = pystray.Icon(
    "Rose Player Manager",
    image,
    "This is an app for managing the Rose Player",
    menu=pystray.Menu(
        pystray.MenuItem("Open", after_click, default=True),
        pystray.MenuItem("Exit", after_click),
    ),
)


def HelpFunc():
    print(
        Fore.CYAN
        + "(R)ose (P)layer Manager"
        + Fore.RESET
        + " is a tool used for managing the Rose Player device"
    )
    print(
        "currently only working on windows, hopefully I can extend it to pipewire and pulseaudio in the future"
    )
    print(Fore.BLUE + "")
    print("-h for help")
    print("-S or --shown to start the app with the window open")
    print("-m to get the media output" + Fore.RESET)


try:
    opts, args = getopt.getopt(args, "hSm", ["shown"])
except getopt.GetoptError:
    print("Use -h for help")
    HelpFunc()
    sys.exit(1)

for opt, arg in opts:
    if opt == "-h":
        state = "Help"
    elif opt in ("-S", "--shown"):
        state = "Shown"
    elif opt == "-m":
        state = "Media"

Background_Function = threading.Thread(
    target=Global.Playback_Service, name="Playback Refresh"
)
Background_Function.start()

if state == "Help":
    HelpFunc()
elif state == "Shown":
    app = GUI.App()
    app.mainloop()
    icon.run()
elif state == "Media":
    print(Playing.GetPlaying())
else:
    icon.run()
