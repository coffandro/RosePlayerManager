
def LoadSettings():
    try:
        f = open('Settings.json', "rw")

        # returns JSON object as
        # a dictionary
        settings = json.load(f)

        # Closing file
        f.close()
    except:
        settings = {"comport": "COM5", "multScreens": 0, "optionmenu1": "Media info","optionmenu2": "Media info"}
    
    return settings
def SaveSettings():
    print(settings)
    with open('Settings.json', 'w') as f:
        json.dump(settings, f)