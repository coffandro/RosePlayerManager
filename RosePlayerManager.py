import sys
from colorama import Fore
import RosePlayerGUI as GUI
import RosePlayerPlaying as Playing
import getopt
import pystray
from PIL import Image


def IsBundled():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return True
    else:
        return False


print("Is bundled: " + str(IsBundled()))

args = sys.argv[1:]
image = Image.open("Icons/Rose256.png")
state = ""


def after_click(icon, query):
    if str(query) == "Open":
        app = GUI.App()
        app.mainloop()
    elif str(query) == "Exit":
        icon.stop()
        sys.exit(0)


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
    print("-H or --hidden to start the app in the tray")
    print("-m to get the media output" + Fore.RESET)


try:
    opts, args = getopt.getopt(args, "hHm", ["hidden"])
except getopt.GetoptError:
    print("Use -h for help")
    HelpFunc()
    sys.exit(1)

for opt, arg in opts:
    if opt == "-h":
        state = "Help"
    elif opt in ("-H", "--hidden"):
        state = "Hidden"
    elif opt == "-m":
        state = "Media"

if state == "Help":
    HelpFunc()
elif state != "Hidden":
    app = GUI.App()
    app.mainloop()
    icon.run()
elif state == "Media":
    print(Playing.GetPlaying())
else:
    icon.run()
