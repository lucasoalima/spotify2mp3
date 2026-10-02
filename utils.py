from const import colours
import string
import random
import eyed3
from eyed3.id3.frames import ImageFrame
import requests
import shutil
from pathlib import Path


def print_splash_screen():
        print(colours.SPOTIFYGREEN + '''
              


              
        ███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗██████╗ ███╗   ███╗██████╗ ██████╗ 
        ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝╚════██╗████╗ ████║██╔══██╗╚════██╗
        ███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝  █████╔╝██╔████╔██║██████╔╝ █████╔╝
        ╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝  ██╔═══╝ ██║╚██╔╝██║██╔═══╝  ╚═══██╗
        ███████║██║     ╚██████╔╝   ██║   ██║██║        ██║   ███████╗██║ ╚═╝ ██║██║     ██████╔╝
        ╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚═════╝         
              
        ''' + colours.ENDC + colours.BOLD + '''         Download your favourite songs as mp3s with the click of a button.  ''' + colours.ENDC + "\n")


def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters  # This includes both lowercase and uppercase letters.
    return ''.join(random.choice(letters) for i in range(length))

def resave_audio_clip_with_metadata(audio_input_path, song_metadata, song_output_path, audio_quality):
    audiofile = eyed3.load(audio_input_path)
    if audiofile is None:
        raise ValueError(f"Could not read generated MP3: {audio_input_path}")

    if audiofile.tag is None:
        audiofile.initTag()

    try:
        image_response = requests.get(song_metadata['image_url'], timeout=15)
        image_response.raise_for_status()
        audiofile.tag.images.set(
            ImageFrame.FRONT_COVER,
            image_response.content,
            'image/jpeg',
            "Cover Image from Spotify",
        )
    except requests.RequestException:
        pass

    audiofile.tag.title = song_metadata['title']
    audiofile.tag.artist = ", ".join(song_metadata['artist'])
    audiofile.tag.album = song_metadata['album']
    audiofile.tag.track_num = (song_metadata['track_num'], 0)
    audiofile.tag.release_date = song_metadata['release_date'][:4]
    audiofile.tag.save()

    Path(song_output_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(audio_input_path, song_output_path)
