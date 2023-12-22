import RPlayer_ManagerGui as GUI
import RPlayer_GetPlayingInfo as Media
import pystray
from PIL import Image
import sys
import getopts
import asyncio



# SETTING UP ICON

image = Image.open("Icons/Rose256.png")

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
        pystray.MenuItem("Exit", after_click)))



# RUNNING

icon.run()
