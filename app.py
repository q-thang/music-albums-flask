from flask import Flask, request, send_from_directory
import json
import math

app = Flask(__name__)


class Albums():
    """Class representing a collection of albums."""

    def __init__(self, albums_file, tracks_file):
        self.__albums = []
        self.__load_albums(albums_file)
        self.__load_tracks(tracks_file)

    def __load_albums(self, albums_file):
        """Loads a list of albums from a file."""
        # TODO complete
        with open(albums_file) as file:
            for item in file:
                item = item.strip()
                [album_id, album_artist, album_title,
                    album_image] = item.split("\t")
                album = {
                    "album_id": album_id,
                    "album_artist": album_artist,
                    "album_title": album_title,
                    "album_image": album_image,
                    "album_tracks": [],
                    "album_minutes": 0,
                    "album_seconds": 0,
                    "album_length": 0
                }
                self.__albums.append(album)

    def __load_tracks(self, tracks_file):
        """Loads a list of tracks from a file."""
        # TODO complete
        with open(tracks_file) as file:
            cnt = 0
            id_album = 1
            for item in file:
                item = item.strip()
                [track_id, track_title, track_length] = item.split("\t")
                if id_album == int(track_id):
                    cnt = cnt + 1
                else:
                    id_album = id_album + 1
                    cnt = 1
                track = {
                    "track_id": cnt,
                    "track_title": track_title,
                    "track_length": track_length
                }
                [track_minute, track_second] = track_length.split(":")

                self.__albums[int(track_id) - 1]['album_tracks'].append(track)
                self.__albums[int(track_id) -
                              1]['album_seconds'] += int(track_second)
                self.__albums[int(track_id) -
                              1]['album_minutes'] += int(track_minute)

        for album in self.__albums:
            album_second = album['album_seconds']
            # minute convert from second
            album_second_temp = math.floor(album_second / 60)
            album_minute = album['album_minutes'] + album_second_temp
            album_second = album_second % 60
            if (len(str(album_second))) == 1:
                album_second = "0" + str(album_second)
            album['album_length'] = str(
                str(album_minute) + ":" + str(album_second))

    def get_albums(self):
        """Returns a list of all albums, with album_id, artist and title."""
        # TODO complete
        return self.__albums

    def get_album(self, album_id):
        """Returns all details of an album."""
        # TODO complete
        album_id = int(album_id)
        return self.__albums[album_id - 1]


# the Albums class is instantiated and stored in a config variable
# it's not the cleanest thing ever, but makes sure that the we load the text files only once
app.config["albums"] = Albums("data/albums.txt", "data/tracks.txt")


@app.route("/albums")
def albums():
    """Returns a list of albums (with album_id, author, and title) in JSON."""
    albums = app.config["albums"]
    # TODO complete (return albums.get_albums() in JSON format)
    return json.dumps(albums.get_albums())


@app.route("/albuminfo")
def albuminfo():
    albums = app.config["albums"]
    album_id = request.args.get("album_id", None)
    if album_id:
        # TODO complete (return albums.get_album(album_id) in JSON format)
        return json.dumps(albums.get_album(album_id))
    return "Invalid album id"


@app.route("/images/<name>")
def albumcover(name):
    return send_from_directory('./static/images', name)


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run()
