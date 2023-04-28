import typer
from ak_jiosaavn.main import initialize
import json

app = typer.Typer()

@app.command()
def playlist(playlist_url: str,
                      skip_downloaded:bool = True, 
                      userinput_file: str = 'userinput.json'):
    """Download the songs from specified playlist URL
    """
    jiosaavn = initialize('userinput.json')
    jiosaavn.get_playlist(url=playlist_url, skip_existing=skip_downloaded)

@app.command()
def song(song_url: str,
                      skip_downloaded:bool = True, 
                      userinput_file: str = 'userinput.json'):
    """Download the songs from specified song URL
    """
    jiosaavn = initialize('userinput.json')
    jiosaavn.get_song(url=song_url, skip_existing=skip_downloaded)

@app.command()
def default(skip_downloaded:bool = True, 
                      userinput_file: str = 'userinput.json'):
    """Download the songs from playlists specified in `userinput_file`
    """
    jiosaavn = initialize('userinput.json')
    with open(userinput_file, 'r') as f:
        userinput = json.load(f)

    for playlist_url in userinput['default_playlists'].values():
        jiosaavn.get_playlist(url=playlist_url, skip_existing=skip_downloaded)