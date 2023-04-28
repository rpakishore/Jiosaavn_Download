from ak_jiosaavn.loginator import AKLog
from ak_cache import Cache
import time
import shutil
from pathlib import Path
from datetime import datetime

import requests
from requests.models import Response

from ak_jiosaavn.audio import _write_metadata, _download_media, Song

class JiosaavnAPI:
    def __init__(self, log:AKLog, cache: Cache, ip: str, 
                 port: str, destination_folder: str) -> None:
        self.log = log
        self.cache= cache
        self.ip = ip
        self.port = port
        self.destination_folder = str(destination_folder)
        self.ses = requests.Session()
        self.req_headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) \
                    Gecko/20100101 Firefox/49.0',
                'Accept': 'text/html,application/xhtml+xml,\
                    application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        self.ses.headers.update(self.req_headers)

        self.downloaded = cache.read()
        self.api_url = f"http://{ip}:{port}"

    def __str__(self) -> str:
        return "JiosaavnAPI Class Module"
    
    def __repr__(self) -> str:
        return "JiosaavnAPI()"
    
    def get(self, url) -> Response:
        return _get_requests(
            log = self.log,
            session=self.ses,
            tries = 3,
            delay=False,
            timeout=10
        )
    
    def get_song_info(self, url: str) -> Song:
        log = self.log
        log.info(f"Initiating song download for {url}")
    
        song_response = self.get(
            url = self.song_request_url.format(self.url))
        return _parse_song_info(song_response.json(), log=self.log)
    
    def _download_song(self, song: Song):
        self.log.info(f"Initiating song download for {song.media_url}")
        response = _download_media(song)
        self.log.info(response)
        
    def get_song(self, song: Song, skip_existing:bool = False) -> None:
        log = self.log
        if skip_existing and song.id in self.downloaded.keys():
            log.info(f"Skipping since `-s` passed. \
                     This song was previously downloaded \
                     on {self.downloaded[song.id].strftime('%b %d, %Y %H:%M:%S')}")
            return
        log.info(_download_media(song=song))
        res = self.get(song.image_url)
        log.info(_write_metadata(song=song, image=res.content))
        log.info(move_file_to_folder(
            filename=song.filename, destination_folder=self.destination_folder))
        self.downloaded[song.id] = datetime.now()
        self.cache.write(self.downloaded)
    
    def get_playlist(self, url: str, skip_existing:bool = False) -> None:
        log = self.log
        log.info(f"Initiating playlist download for {url}")
        playlist_data = self.get(
            url = self.playlist_request_url.format(self.url)).json()
        song_datas = playlist_data['songs']
        for song_data in song_datas:
            song = _parse_song_info(song_data=song_data, log=self.log)
            self.get_song(song=song, skip_existing=skip_existing)

    @property
    def song_request_url(self) -> str:
        return self.api_url + "/song/?query={}"
    
    @property
    def playlist_request_url(self) -> str:
        return self.api_url + "/result/?query={}"
    
def _get_requests(url, tries = 3, delay: bool = False, 
                  timeout = 10, log: AKLog = None, 
                  session: requests.Session = None) -> Response:
    
    if log:
        log.info(f"Initiating requests: {url}")
    else:
        print(f"Initiating requests: {url}")
   
    if not session:
        session = requests.Session()

    for _ in range(tries):
        try:
            res = session.get(url, timeout=timeout)
            res.raise_for_status()
            
            if delay != 0:
                time.sleep(res.elapsed.total_seconds())
            
            if log:
                log.info(f"Request completed successfully for {res.url}")
            else:
                print(f"Request completed successfully for {res.url}")
            return res
        
        except Exception as e:
            if log: 
                log.error(f'Request failed on try {str(tries)} for URL: {url}')
                log.error(f'Exception: {str(e)}')
            else:
                print(f'Request failed on try {str(tries)} for URL: {url}')
                print(f'Exception: {str(e)}')

    if log:
        log.error(f"NG - Getting soup element failed. \
                Requests tried {str(tries)} times, without success")
        log.error(f"Failed URL: {url}")
    else:
        print(f"NG - Getting soup element failed. \
                Requests tried {str(tries)} times, without success")
        print(f"Failed URL: {url}")
    raise AssertionError("Requests tried " + str(tries) + " times, without success")

def move_file_to_folder(filename: str, destination_folder: Path) -> str:
    """Move specifiec file to destination folder
    """
    origin_path = Path(str(filename))
    destination_path = destination_folder / str(filename)
    shutil.move(origin_path, destination_path)
    return f"Moved: {filename} --> {destination_path}"

def _parse_song_info(song_data: dict, log:AKLog = None) -> Song:
    try:
        album_artists = ', '.join(list(song_data['artistMap'].keys()))
    except Exception:
        try:
            album_artists = ', '.join(list(song_data['artistMap']))
        except Exception:
            album_artists = ""

    song = Song(
        name=song_data['song'],
        album=song_data['album'],
        id = song_data['id'],
        media_url=song_data['media_url'],
        year=song_data['year'],
        artist=song_data['primary_artists'],
        album_artists=album_artists,
        image_url=song_data['image']
    )
    if log:
        log.info(f"Found song {song.name} from {song.album}")
    else:
        print(f"Found song {song.name} from {song.album}")
    return song