import spotipy
import pandas as pd
import spotipy.util as util
import spotipy.oauth2 as oauth
import spotipy.client
Client_ID = '11b38cefc27c4e399f30c4fbc4bd5f68'
Client_Secret = '1acfedb043d644f48f3cf403e1995778'
username = 'mat.nob'
SPOTIPY_REDIRECT_URI = 'http://localhost/'
scope = 'playlist-modify-private'
credentials = oauth.SpotifyClientCredentials(Client_ID, Client_Secret)
# token = credentials.get_access_token(as_dict=False)


def chunkify(lst, n):
    L = [lst[i::n] for i in range(n)]
    return L


token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=Client_ID,
                                   client_secret=Client_Secret,
                                   redirect_uri=SPOTIPY_REDIRECT_URI)


def create_playlists(n, name):
    sp = spotipy.Spotify(auth=token)
    for i in range(1, n):
        k = str(i)
        Name = name + ' ' + k
        Source = 'Complete ' + Name
        file_source = Source + '.csv'
        try:
            tracks_database = pd.read_csv(file_source)
            if len(tracks_database['album'].values) < 10:
                pass
            else:
                # tracks_database = tracks_database.drop_duplicates(
                #     'track', keep='first')
                new_list = sp.user_playlist_create(
                    username, name=Name, public=False)
                list_id = new_list['id']
                tracks_id = list(tracks_database['id'])
                # sp.user_playlist_add_tracks(
                #     Client_ID, list_id, tracks_id)
                L = len(tracks_id)
                if L % 50 != 0.0:
                    n = 1 + int(L / 50)
                else:
                    n = int(L / 50)
                T = chunkify(tracks_id, n)
                for chunk in T:
                    sp.user_playlist_add_tracks(
                        Client_ID, list_id, chunk)
        except:
            pass
