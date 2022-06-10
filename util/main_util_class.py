#!/usr/bin/env python
# coding: utf-8

# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
from util import AK_log
import json, pickle, os, time, shutil, unicodedata, re

from util import AK_log
from util import Slack_util_class

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
        log.error(str(e))
        self.slack.msg("TamilSongDownload Script: Failure - See Log for details.", "python")
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
        
        if args.playlist:
            self.download_playlist(url=args.playlist, skip=args.skipdownloaded)
        return
    
    def download_playlist(self, url, skip):
        log = self.log
        log.info(f"Initiating playlist download for {url}")
        
        data_dump = self.get_requests(f"http://{self.user_prop['ip']}:{self.user_prop['port']}/result/?query={url}").json()
        
        to_download = []
        for song in data_dump['songs']:
            log.info(f"Found song {song['song']} from {song['album']}")
            if skip and song['id'] in self.downloaded.keys():
                log.info(f"Skipping since `-s` passed. This song was previously downloaded on {self.downloaded[song['id']].strftime('%m %d, %Y %H:%M:%S')}")
                continue
            else:
                to_download.append(song)
            pass
        
        log.info(f"{len(to_download)} songs will be downloaded.")
        for song in to_download:
            filename = self.download_song(song['media_url'], f"{song['song']}-{song['album']}({song['year']})")
            self.write_metadata(filename, song)
            song['filename'] = filename
            self.move_to_destination(song)
            self.downloaded[song['id']] = datetime.now()
            self.serialize_cache()
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
        
    def write_metadata(self, filename, data):
        log = self.log
        log.debug(f"Writing metadata to {filename}")
        audiofile = eyed3.load(filename)
        audiofile.initTag()
        audiofile.tag.artist = data['primary_artists']
        audiofile.tag.album = data['album']
        audiofile.tag.album_artist= ', '.join(list(data['artistMap'].keys()))
        audiofile.tag.title = data['song']
        audiofile.tag.year = data['year']
        
        res = self.get_requests(data['image'])
        audiofile.tag.images.set(3, res.content, "image/jpeg", u"cover")
        audiofile.tag.save()
        log.info(f"Metadata written for {data['song']}")
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