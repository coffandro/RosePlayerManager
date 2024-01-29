import json
import RPlayer_GetPlayingInfo as MediaGetter
import asyncio

# Read Settings
try:
    f = open('Settings.json')

    # returns JSON object as 
    # a dictionary
    settings = json.load(f)

    # Closing file
    f.close()
except:
    settings = {"comport": "COM5", "multScreens": 0, "optionmenu1": "Media info","optionmenu2": "Media info"}
try:
    f = open('Media.json')

    # returns JSON object as 
    # a dictionary
    PastMedia = json.load(f)

    # Closing file
    f.close()
except:
    PastMedia = "N/A"

print(settings)

if 'Media info' in str(settings):
    current_media_info = asyncio.run(MediaGetter.get_media_info())
    print(current_media_info)
    print(PastMedia)
    if PastMedia != current_media_info:
        PastMedia = current_media_info
        print("different")
        with open('Media.json', 'w') as f:
            json.dump(PastMedia, f)
    else:
        print("same")