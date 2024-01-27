import asyncio
import serial
import json
import time

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


def GetPlaying():
    current_media_info = asyncio.run(get_media_info())
    print(current_media_info)


if __name__ == "__main__":
    GetPlaying()
