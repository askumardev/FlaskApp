import json
from urllib.request import urlopen

from flask import render_template
from . import api_bp


@api_bp.route('/albums', methods=['GET'])
def albums():
    with urlopen("https://jsonplaceholder.typicode.com/albums/", timeout=10) as response:
        data = json.load(response)
    # return jsonify(data)
    return render_template("albums.html", albums=data)


@api_bp.route('/albums/<int:album_id>', methods=['GET'])
def album_detail(album_id):
    with urlopen(f"https://jsonplaceholder.typicode.com/albums/{album_id}", timeout=10) as response:
        album = json.load(response)
    return render_template("album_detail.html", album=album)