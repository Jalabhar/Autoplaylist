from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import numpy as np
import pandas as pd
import time


def get_related(lista):
    sleep_min = 0.5
    sleep_max = 1.0
    request_count = 0
    relacionados_full = []
    client_id = '11b38cefc27c4e399f30c4fbc4bd5f68'
    client_secret = '1acfedb043d644f48f3cf403e1995778'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    for ID in lista:
        info = sp.artist_related_artists(ID)
        for i in range(len(info['artists'])):
            relacionados_full.append(info['artists'][i]['id'])
    return relacionados_full
