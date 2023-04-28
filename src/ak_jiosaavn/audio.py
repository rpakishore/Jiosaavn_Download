import eyed3
from time import time
from ak_file import File
from ffmpy import FFmpeg

from dataclasses import dataclass
from ak_file import sanitize

@dataclass
class Song:
    name: str
    album: str
    id: str
    media_url: str
    year: int
    image_url: str
    artist: str
    album_artists: str

    def __post_init__(self) -> None:
        self.filename = sanitize(f"{self.name}-{self.album}({self.year}).mp3")

def _write_metadata(song: Song, image: bytes) -> str:
    """Write song metadata to `.mp3` file
    """
    audiofile = eyed3.load(song.filename)
    audiofile.initTag()
    audiofile.tag.artist = song.artist
    audiofile.tag.album = song.album
    audiofile.tag.album_artist = song.album_artists
    audiofile.tag.title = song.name
    audiofile.tag.year = song.year
    audiofile.tag.images.set(3, image, "image/jpeg", u"cover")
    audiofile.tag.save()
    return f"Metadata written for {song.name}"

def _download_media(song: Song) -> str:
    """Downloads media for the specified Song Class to the local
        directory and returns download parameters"""
    start_time = time()
    FFmpeg(
        inputs={song.media_url:None},
        outputs={song.filename: None}
    ).run()
    file = File(song.filename)
    size = file.properties()['Size_B']/(1024*1024)  #In MB
    time_taken = time() - start_time
    return f"Download completed ({round(size,2)} MB) in \
        {round(time_taken,1)} sec(s) at {round(size/time_taken, 1)} MB/s"