import json


def Read_Settings():
    # Read Settings
    try:
        f = open("Settings.json")

        # returns JSON object as
        # a dictionary
        settings = json.load(f)

        # Closing file
        f.close()
    except:
        settings = {
            "comport": "COM5",
            "multScreens": 1,
            "optionmenu1": "Media info",
            "optionmenu2": "Media info",
        }

    return settings


def Write_Settings(settings):
    with open("Settings.json", "w") as f:
        json.dump(settings, f)
