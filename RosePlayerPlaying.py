import asyncio
import serial
import json
import time
from sys import platform
import subprocess

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if platform == "linux" or platform == "linux2":
    def get_media_info():
        data = str(subprocess.check_output(["playerctl", "metadata"]))
        info_dict = {}
        
        info_dict["title"] = find_between(data, "xesam:title", "\\").strip()
        info_dict["album_title"] = find_between(data, "xesam:album", "\\").strip()
        info_dict["artist"] = find_between(data, "xesam:artist", "\\").strip()
        
        return info_dict

elif platform == "win32":
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    )


    async def get_media_info():
        try:
            sessions = await MediaManager.request_async()

            current_session = sessions.get_current_session()
            if current_session:  # there needs to be a media session running
                info = await current_session.try_get_media_properties_async()

                # song_attr[0] != '_' ignores system attributes
                info_dict = {
                    song_attr: info.__getattribute__(song_attr)
                    for song_attr in dir(info)
                    if song_attr[0] != "_"
                }

                # converts winrt vector to list
                info_dict["genres"] = list(info_dict["genres"])

                info_dict.pop("thumbnail")

                return info_dict

        # It could be possible to select a program from a list of current
        # available ones. I just haven't implemented this here for my use case.
        # See references for more information.
        except:
            print("no media")
else:
    print("no media")


def GetPlaying():
    if platform == "linux" or platform == "linux2":
        current_media_info = get_media_info()
    elif platform == "win32":
        current_media_info = asyncio.run(get_media_info())
    print(current_media_info)


if __name__ == "__main__":
    GetPlaying()
