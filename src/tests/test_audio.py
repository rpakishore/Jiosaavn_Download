from ak_jiosaavn.audio import Song, _write_metadata, _download_media
import pytest
import os

@pytest.fixture(scope="module")
def sample_song():
    return Song(
        name="My Song",
        album="My Album",
        id="123",
        media_url="https://example.com/my_song.mp3",
        year=2022,
        image_url="https://example.com/my_song_cover.jpg",
        artist="My Artist",
        album_artists="My Album Artist"
    )

def test_song_filename(sample_song):
    assert sample_song.filename == "My Song-My Album(2022).mp3"
