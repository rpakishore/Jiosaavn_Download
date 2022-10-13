#!/usr/bin/env python
# coding: utf-8

# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
from dataclasses import dataclass
import json, pickle, os, time, shutil, unicodedata, re

from util import AK_log
#from util import Slack_util_class

from datetime import datetime
from sys import platform

#pip install requests
import requests
#pip install beautifulsoup4
from bs4 import BeautifulSoup as bs

#pip install ffmpy
from ffmpy import FFmpeg

#pip install eyed3
import eyed3

import pytest

@dataclass
class song:
    album: str
    album_url: str
    artists: list
    duration: int
    image_url: str
    media_url: str
    release_date: str
    singers: str
    title: str
    year: int
    id: str
    filename:str = ""
    
    
class main_instance:
    homedir = os.path.expanduser('~')
    # Define log level
    # Log levels: NOTSET DEBUG INFO WARNING ERROR CRITICAL
    log = AK_log.AKLog()
    #log.basicConfig(level=log.DEBUG,format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log.setLevel(10)
    
    # Constructor
    def __init__(self, args):
        log = self.log
        log.debug('Initializing Jiosaavn Module.')
        self.args = args
        log.debug(f"args passed: {args}")
        with open(args.filename, 'r') as f:
            self.user_prop = json.load(f)

        if args.writecache:
            #Mobilize Cache
            self.cache_file = self.user_prop["Cache_file"]
            if not os.path.isfile(self.cache_file):
                with open(self.cache_file, 'wb') as f:
                    downloaded = {}
                    pickle.dump(downloaded, f)
            with open(self.cache_file, 'rb') as f:
                self.downloaded = pickle.load(f)
            log.debug('Cache mobilized.')
        else:
            self.downloaded = {}
            
        self.ses = requests.Session()
        self.req_headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        self.ses.headers.update(self.req_headers)
        self.new_songs = []
        
        return

    def serialize_cache(self):
        """Writes the downloaded variable to cache
        """
        if self.args.writecache:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.downloaded, f)
            self.log.info('Cache updated')
        return
    
    
    def get_requests(self, url, tries = 3, delay = 0, timeout = 10):
        log = self.log
        log.info(f"Initiating requests: {url}")
        
        i = 0        
        while i < tries:
            try:
                res = self.ses.get(url, timeout=timeout)
                res.raise_for_status()
                
                if delay != 0:
                    time.sleep(res.elapsed.total_seconds())
                
                log.info(f"Request completed successfully for {res.url}")
                return res
            
            except Exception as e: 
                log.error(f'Request failed on try {str(tries)} for URL: {url}')
                i += 1
        log.error(f"NG - Getting soup element failed. Requests tried {str(tries)} times, without success")
        log.error(f"Failed URL: {url}")
        raise AssertionError("Requests tried " + str(tries) + " times, without success")
    
    # Desstructor
    def __del__(self):
        try:
            self.log.info("Action Complete. Exiting Now.")
        except:
            pass
        return
    
    def do_actions(self):
        log = self.log 
        args = self.args
        user_prop = self.user_prop
        
        if args.printcache:
            print(self.downloaded)
        
        if args.playlist:
            self.download_playlist(url=args.playlist, skip=args.skipdownloaded)
        
        if args.song:
            self.extract_song_info(args.song)
            
        if args.defaultplaylist:
            for playlist in user_prop["default_playlists"].keys():
                log.info(f"Downloading playlist: {playlist}")
                self.download_playlist(url=user_prop["default_playlists"][playlist], skip=args.skipdownloaded)
        return
    
    def extract_song_info(self, url, skip=False):
        log = self.log
        log.info(f"Initiating song download for {url}")
        
        data_dump = self.get_requests(f"http://{self.user_prop['ip']}:{self.user_prop['port']}/song/?query={url}").json()
        log.info(f"Found song {data_dump['song']} from {data_dump['album']}")
        if skip and data_dump['id'] in self.downloaded.keys():
            log.info(f"Skipping since `-s` passed. This song was previously downloaded on {self.downloaded[data_dump['id']].strftime('%b %d, %Y %H:%M:%S')}")
        else:
            filename = self.download_song(data_dump['media_url'], f"{data_dump['song']}-{data_dump['album']}({data_dump['year']})")
            self.write_metadata(filename, data_dump)
            data_dump['filename'] = filename
            self.move_to_destination(data_dump)
            self.downloaded[data_dump['id']] = datetime.now()
            self.serialize_cache()
        return
    

    def collect_songs_from_playlist(self, url: str):
        """
        Takes a jiosaavn playlist url as input and returns a list of song objects

        Returns:
            list[song]: Returns a list of song object
        """
        json_data = self.get_playlist_data(url)
        return [parse_song_data(song_info) for song_info in json_data['songs']]
            

    def get_playlist_data(self, url: str):
        """Takes a Jiosaavn URL and returns the json data from the locally hosted Jiosaavn API endpoint

        Args:
            url (str): Jiosaavn PLAYLIST url

        Returns:
            dict: Json data returned from the API
        """
        log = self.log
        log.info(f"Initiating playlist download for {url}")
        jiosaavn_hosted_url = f"http://{self.user_prop['ip']}:{self.user_prop['port']}/result/"
        return self.get_requests(f"{jiosaavn_hosted_url}?query={url}").json()

    def download_playlist(self, url: str, skip: bool):
        log = self.log
        log.info(f"Initiating playlist download for {url}")
        
        songs = self.collect_songs_from_playlist(url)
        to_download = []
        for song in songs:
            log.info(f"Found song {song.title} from {song.album}")
            if skip and song.id in self.downloaded.keys():
                log.info(f"Skipping since `-s` passed. This song was previously downloaded on {self.downloaded[song.id].strftime('%m %d, %Y %H:%M:%S')}")
                continue
            else:
                to_download.append(song)
            pass
        
        log.info(f"{len(to_download)} songs will be downloaded.")
        for song in to_download:
            song.filename = self.download_song(song.media_url, f"{song.title}-{song.album}({song.year})")
            self.write_metadata(song.filename, song)
            self.move_to_destination(song)
            self.downloaded[song.id] = datetime.now()
            self.serialize_cache()
            self.new_songs.append(song)
        return
    
    def move_to_destination(self, song):
        log = self.log
        destination = os.path.join(self.user_prop['final_destination'], os.path.basename(song['filename']))
        log.debug(f"Attempting to move file to final destination: {song['filename']} --> {destination}")
        shutil.move(song['filename'], destination)
        log.info(f"Moved: {song['filename']} --> {destination}")
        return
    
    def download_song(self, url, final):
        log = self.log
        local_filename = url.split('/')[-1]
        name, ext = os.path.splitext(local_filename)
        final_file = sanitize(final + '.mp3')
        
        log.info(f"Downloading from {url} to {final_file}")
        start = time.time()
        FFmpeg(
            inputs={url:None},
            outputs={final_file: None}
        ).run()

        size = os.path.getsize(final_file)/(1024*1024)  #In MB
        time_taken = time.time() - start
        log.info(f"Download completed ({round(size,2)} MB) in {round(time_taken,1)} sec(s) at {round(size/time_taken, 1)} MB/s")
        return final_file
        
    
    def download_file(self, url):
        log = self.log
        local_filename = url.split('/')[-1]
        
        log.info(f"Downloading from {url} to {local_filename}")
        start = time.time()
        with requests.get(url, stream=True, headers=self.req_headers) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        size = os.path.getsize(local_filename)/(1024*1024)  #In MB
        time_taken = time.time() - start
        log.info(f"Download completed ({round(size,2)} MB) in {round(time_taken,1)} sec(s) at {round(size/time_taken, 1)} MB/s")
        return local_filename
        
        
    def write_metadata(self, filename, song):
        log = self.log
        log.debug(f"Writing metadata to {filename}")
        audiofile = eyed3.load(filename)
        audiofile.initTag()
        audiofile.tag.artist = song.artists
        audiofile.tag.album = song.album
        audiofile.tag.album_artist= ', '.join(song.artists)

        audiofile.tag.title = song.title
        audiofile.tag.year = str(song.year)
        
        res = self.get_requests(song.image_url)
        audiofile.tag.images.set(3, res.content, "image/jpeg", u"cover")
        audiofile.tag.save()
        log.info(f"Metadata written for {song.title}")
        return
            


def sanitize(filename):
    """Return a fairly safe version of the filename.

    We don't limit ourselves to ascii, because we want to keep municipality
    names, etc, but we do want to get rid of anything potentially harmful,
    and make sure we do not exceed Windows filename length limits.
    Hence a less safe blacklist, rather than a whitelist.
    """
    blacklist = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\0"]
    reserved = [
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
        "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
        "LPT6", "LPT7", "LPT8", "LPT9",
    ]  # Reserved words on Windows
    filename = "".join(c for c in filename if c not in blacklist)
    # Remove all charcters below code point 32
    filename = "".join(c for c in filename if 31 < ord(c))
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.rstrip(". ")  # Windows does not allow these at end
    filename = filename.strip()
    if all([x == "." for x in filename]):
        filename = "__" + filename
    if filename in reserved:
        filename = "__" + filename
    if len(filename) == 0:
        filename = "__"
    if len(filename) > 255:
        parts = re.split(r"/|\\", filename)[-1].split(".")
        if len(parts) > 1:
            ext = "." + parts.pop()
            filename = filename[:-len(ext)]
        else:
            ext = ""
        if filename == "":
            filename = "__"
        if len(ext) > 254:
            ext = ext[254:]
        maxl = 255 - len(ext)
        filename = filename[:maxl]
        filename = filename + ext
        # Re-check last character (if there was no extension)
        filename = filename.rstrip(". ")
        if len(filename) == 0:
            filename = "__"
    return filename

def parse_song_data(song_dict: dict) -> song:
    """Takes a dict of song data from Jiosaavn and turns it into a song object  

    Returns:
        song: Song object of the data passed
    """
    album = song_dict["album"] if "album" in song_dict.keys() else ""
    album_url = song_dict["album_url"] if "album_url" in song_dict.keys() else ""
    if "artistMap" in song_dict.keys():
        if type(song_dict['artistMap']) == dict:
            artists = list(song_dict['artistMap'].keys())
        elif type(song_dict['artistMap']) == list:
            artists = song_dict['artistMap']
        else:
            artists = ""
    artists = list(song_dict['artistMap'].keys()) if "singers" in song_dict.keys() else ""
    duration = int(song_dict["duration"]) if "duration" in song_dict.keys() else ""
    image_url = song_dict["image"] if "image" in song_dict.keys() else ""
    year = int(song_dict["year"]) if "year" in song_dict.keys() else ""
    media_url = song_dict["media_url"] if "media_url" in song_dict.keys() else ""
    release_date = song_dict["release_date"] if "release_date" in song_dict.keys() else ""
    singers = song_dict["singers"].split(', ') if "singers" in song_dict.keys() else ""
    title = song_dict["song"]
    id = song_dict["id"]
    
    return song(
        album=album, album_url=album_url, artists=artists, duration=duration, 
        image_url=image_url, media_url=media_url, release_date=release_date, 
        singers=singers, title=title, year=year, id=id
    )

def test_parse_song_data():
    with open('userinput.json', 'r') as f:
        user_prop = json.load(f)
    url = f"http://{user_prop['ip']}:{user_prop['port']}/result/?query=https://www.jiosaavn.com/featured/romantic-hits-2020—hindi/ABiMGqjovSFuOxiEGmm6lQ__"
    raw_data = requests.get(url).json()['songs'][0]
    song_obj = parse_song_data(raw_data)
    
    assert type(song_obj) == song
    assert song_obj.album == "Love Aaj Kal (Original Motion Picture Soundtrack)"
    assert song_obj.album_url == "https://www.jiosaavn.com/album/love-aaj-kal-original-motion-picture-soundtrack/08dQgBZGh20_"
    assert song_obj.artists == ["Arijit Singh", "Irshad Kamil", "Kartik Aaryan", "Pritam", "Sara Ali Khan"]
    assert song_obj.duration == 247
    assert song_obj.image_url == "https://c.saavncdn.com/862/Love-Aaj-Kal-Hindi-2020-20200214140423-500x500.jpg"
    assert song_obj.year == 2020
    assert song_obj.media_url == "https://aac.saavncdn.com/862/e277c1b441b562640c6b264aa3335a83_320.mp4"
    assert song_obj.release_date == "2020-02-14"
    assert song_obj.singers == ["Pritam", "Arijit Singh"]
    assert song_obj.title == "Shayad"