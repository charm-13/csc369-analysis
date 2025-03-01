import os
import json
import time

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE")
SPOTIPY_REDIRECT_URI = "http://localhost:3000"

sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )
sp = spotipy.Spotify(auth_manager=sp_oauth)

def get_playlists():
    """
    playlists
    """
    playlists = [
        "0gN8NdFTQ057rqnqxL9PbJ", # https://open.spotify.com/playlist/0gN8NdFTQ057rqnqxL9PbJ?si=0d8c36a59c1c45dd
        "6NCpToMn8ITlk6W9YM44U1", # https://open.spotify.com/playlist/6NCpToMn8ITlk6W9YM44U1?si=a146cd55fd8740e0 
        "5sU9YTmkOdQEUT7jwW2ghp", # https://open.spotify.com/playlist/5sU9YTmkOdQEUT7jwW2ghp?si=aea606b3a2164a29 
        "6TVny9vg6tPRAGYJkZ0BHn", # https://open.spotify.com/playlist/6TVny9vg6tPRAGYJkZ0BHn?si=00c690768ef942e7 
        "5sY9rtjrwA5hpdn4zknWs7", # https://open.spotify.com/playlist/5sY9rtjrwA5hpdn4zknWs7?si=556fe08b4446411b 
        "1VhaPIizvGeZQly1TnFB53", # https://open.spotify.com/playlist/1VhaPIizvGeZQly1TnFB53?si=9d1321fa23624e60 
        "0gQE6eMZFPGky5nzWTpKPD", # https://open.spotify.com/playlist/0gQE6eMZFPGky5nzWTpKPD?si=bc9cfb6e76ba4689 
        "5tQandrYv1bkOdYB3wOUQs", # https://open.spotify.com/playlist/5tQandrYv1bkOdYB3wOUQs?si=aed34028baa64c63
        "7uAXLE3iy84teYwNjLChMU", # https://open.spotify.com/playlist/7uAXLE3iy84teYwNjLChMU?si=e6ac58edb91e40b9&pt=db4304563bbf880ac7b91f4fb8a4d46f 
        "0fJvT0OICtFQOHwZnVZGL4", # https://open.spotify.com/playlist/0fJvT0OICtFQOHwZnVZGL4?si=f33afe6e254a49ad 
        "26Zi3qLKC9cAWDs7wbbSzc", # https://open.spotify.com/playlist/26Zi3qLKC9cAWDs7wbbSzc?si=0607a78819a44b1d 
        "3hPk53Lsq9wlPLp7a5C1cO", # https://open.spotify.com/playlist/3hPk53Lsq9wlPLp7a5C1cO?si=e10d5b69cc544679 
        "1PFUEpZTRKcOGkmbKLYgKf", # https://open.spotify.com/playlist/1PFUEpZTRKcOGkmbKLYgKf?si=89f3c9b340714e10 
        "6udg8ZZIWMYzUDhH7rf5bC", # https://open.spotify.com/playlist/6udg8ZZIWMYzUDhH7rf5bC?si=679542b0964945a7 
        "5QfzUTL3kiwDhLfuDTYPBR", # https://open.spotify.com/playlist/5QfzUTL3kiwDhLfuDTYPBR?si=64db6e27dc094b50 
        "0hI2ckWwxfdQPZPPdzxYnp", # https://open.spotify.com/playlist/0hI2ckWwxfdQPZPPdzxYnp?si=a37995d3a34a4fb9 
        "4tfbVhQvZA0Q7qVjpJ3dqS", # https://open.spotify.com/playlist/4tfbVhQvZA0Q7qVjpJ3dqS?si=61e3260176544a8c&pt=93fa0a6a8312534a797248caa9430828 
        "6hXrr2RIxsmR9AKLY9DJnF", # https://open.spotify.com/playlist/6hXrr2RIxsmR9AKLY9DJnF?si=eacecae7450d4867 
        "3B8j0n3eYe4fHyZ9hpn3Ij", # https://open.spotify.com/playlist/3B8j0n3eYe4fHyZ9hpn3Ij?si=1a521d34ba7840c2 
        "3SDdmEcz2lj366dRwK2PZY", # https://open.spotify.com/playlist/3SDdmEcz2lj366dRwK2PZY?si=9b9297ff29fd4129 
        "7xIryD4qMC1bvDaG5OeTCu", # https://open.spotify.com/playlist/7xIryD4qMC1bvDaG5OeTCu?si=70b6bd4084514ee1 
        "2bgiONxpLAvajMosib7GOz", # https://open.spotify.com/playlist/2bgiONxpLAvajMosib7GOz?si=f96a38269f37443c 
        "23gerieDXqLdSpNsTjPrrN", # https://open.spotify.com/playlist/23gerieDXqLdSpNsTjPrrN?si=a540afdb6b2c45a8 
        "4abhyoYxGNEohoEeCkRwU4", # https://open.spotify.com/playlist/4abhyoYxGNEohoEeCkRwU4?si=6c3f7336374c43a3 
        "2u2s3P3fpLiMxA4puplgEn", # https://open.spotify.com/playlist/2u2s3P3fpLiMxA4puplgEn?si=884ef625b1dd479e 
        "2hn1HLOmmJJdw48MKbNnlw", # https://open.spotify.com/playlist/2hn1HLOmmJJdw48MKbNnlw?si=6a3dcfe83c5e489d 
        "4uHlxNGtrDtzlGf00DVSej", # https://open.spotify.com/playlist/4uHlxNGtrDtzlGf00DVSej?si=93990ac5e38147dd 
        "2Aq6hpz4vOZMKe2zvbuRHS", # https://open.spotify.com/playlist/2Aq6hpz4vOZMKe2zvbuRHS?si=1e003342d68047ce 
        "2QoXvUH1X8TMys0Ed0lxLd", # https://open.spotify.com/playlist/2QoXvUH1X8TMys0Ed0lxLd?si=002178f822dc4b6b 
        "7issh1vS02JqqM4GvNGwxL", # https://open.spotify.com/playlist/7issh1vS02JqqM4GvNGwxL?si=ad5496f041e04fac 
        "1F0X0x9V5HQc4zQeFnp7Jd", # https://open.spotify.com/playlist/1F0X0x9V5HQc4zQeFnp7Jd?si=010f552bd19e4a72 
        "2hVwt8pQ4yfWGO7AzybZM4", # https://open.spotify.com/playlist/2hVwt8pQ4yfWGO7AzybZM4?si=3cf669b56708448a&pt=b41144f89446caab48aa2d05ba2f62ba 
        "19iWQw6T18hetl58Nlhbkh", # https://open.spotify.com/playlist/19iWQw6T18hetl58Nlhbkh?si=e6cee30cc89b4319 
        "5Z6yhLGXGSyIQACblOnSxu", # https://open.spotify.com/playlist/5Z6yhLGXGSyIQACblOnSxu?si=0cb3a5ac6bc54575 
        "7tN95PBUKvOoJG4Lm8HjnV", # https://open.spotify.com/playlist/7tN95PBUKvOoJG4Lm8HjnV?si=cbd665dee9844ca9&pt=6788a1c839c95c88699b66077a6b2754 
        "4pxSfOEjdBoLACq1UdoPpv", # https://open.spotify.com/playlist/4pxSfOEjdBoLACq1UdoPpv?si=4294c0f8d82a4e07 
        "5g4pnd1kO4I7ISuvDcE4bp", # https://open.spotify.com/playlist/5g4pnd1kO4I7ISuvDcE4bp?si=59d404e91e0d4c6f 
        "0ISlTJWP0ms9ndgwCUbczF", # https://open.spotify.com/playlist/0ISlTJWP0ms9ndgwCUbczF?si=7915d421908040f0&pt=2d97e49467aaf1ff64b3ef2a0a27e4a8 
        "5fzAddNHc5njIHsrMA5ccu", # https://open.spotify.com/playlist/5fzAddNHc5njIHsrMA5ccu?si=3202736caea247d9 
        "6R2iiHUvcOpD87o7MAeQaD", # https://open.spotify.com/playlist/6R2iiHUvcOpD87o7MAeQaD?si=b69e2041c36749af&pt=5a46a16bf6561bd33013d63ad87981ab 
        "5zwVWnJeqpzUASz6W5JEtj", # https://open.spotify.com/playlist/5zwVWnJeqpzUASz6W5JEtj?si=f0fe3bb92d3d4c7d 
        "0r3j03Da0csWWx3h1sgVQ8", # https://open.spotify.com/playlist/0r3j03Da0csWWx3h1sgVQ8?si=f6e9786f85614b26 
        "0OgwwX14PZTBTZ1cjk7daw", # https://open.spotify.com/playlist/0OgwwX14PZTBTZ1cjk7daw?si=235acd07835b463a 
        "1RMkfKnJvdGEsvDENGNMAK", # https://open.spotify.com/playlist/1RMkfKnJvdGEsvDENGNMAK?si=2454cbf099234290 
        "4O27iXqKPKbnWaT1kAJWAi", # https://open.spotify.com/playlist/4O27iXqKPKbnWaT1kAJWAi?si=3d33d15593a34adb 
        "7KSA85tNHy6sta2H6JVPkJ", # https://open.spotify.com/playlist/7KSA85tNHy6sta2H6JVPkJ?si=4428701500454ae3 
        "1teOyXvYptEzBdXD0kJ1q7", # https://open.spotify.com/playlist/1teOyXvYptEzBdXD0kJ1q7?si=bd89d3ab155244f8 
        "3WTOwPgL64SyJZOefh7loI", # https://open.spotify.com/playlist/3WTOwPgL64SyJZOefh7loI?si=54c53fa7c5b449a0 
        "3YChEVjW6fYrzUuS9Z5efS", # https://open.spotify.com/playlist/3YChEVjW6fYrzUuS9Z5efS?si=189bd61910294dc6 
        "4Y4TbsPVMwyJxUsHK7BJjg", # https://open.spotify.com/playlist/4Y4TbsPVMwyJxUsHK7BJjg?si=5799b9f12f444b8b 
        "3lhnSLd65VfHWGjv7gnqkY", # https://open.spotify.com/playlist/3lhnSLd65VfHWGjv7gnqkY?si=b6d6e94e8b554596 
        "7uztrVI46BMMMqG6ZHHbuM", # https://open.spotify.com/playlist/7uztrVI46BMMMqG6ZHHbuM?si=1c739f56f80b4875
        "6wFsBxxwhGHAp8ewFt45ub", # https://open.spotify.com/playlist/6wFsBxxwhGHAp8ewFt45ub?si=11879da99f2a4ffd 
        "5a2UKuZMeZU2woTPn3IJ7f", # https://open.spotify.com/playlist/5a2UKuZMeZU2woTPn3IJ7f?si=5c19c2f1edb34624 
        "7M1G0yTw66ogktiATFa5Ij", # https://open.spotify.com/playlist/7M1G0yTw66ogktiATFa5Ij?si=22588f4b489e40de 
        "31ckXWrPVQHoJO6YlDKCG2", # https://open.spotify.com/playlist/31ckXWrPVQHoJO6YlDKCG2?si=6e2146aeac374025&pt=eb9e270410465fc6ec205fc9c5509771 
        "0emGwMVHdsuOhLMl3bAGW4", # https://open.spotify.com/playlist/0emGwMVHdsuOhLMl3bAGW4?si=951117e1533149fe 
        "0kl1kdmOkaCFdNULKcwqqI", # https://open.spotify.com/playlist/0kl1kdmOkaCFdNULKcwqqI?si=221b7b2e5f454e55 
        "2cNUparZMBsTzf0YrOl5Em", # https://open.spotify.com/playlist/2cNUparZMBsTzf0YrOl5Em?si=d728fa4703924c29 
        "29uEwYUREmE543EoxdG6FX", # https://open.spotify.com/playlist/29uEwYUREmE543EoxdG6FX?si=d4fb34af266c4a10 
        "4UeaUzZbm0u32txOK3bhn5", # https://open.spotify.com/playlist/4UeaUzZbm0u32txOK3bhn5?si=01b7f82884c845e0 
        "746XjcBfwLTjMXGxZGf8BC", # https://open.spotify.com/playlist/746XjcBfwLTjMXGxZGf8BC?si=b0327173d809431a 
        "5o0AyL9bdyZdih1ZuJ92gg", # https://open.spotify.com/playlist/5o0AyL9bdyZdih1ZuJ92gg?si=ddf6a6cad18845f5 
        "48BZmyaMcoyLxt9qjr075I" # https://open.spotify.com/playlist/48BZmyaMcoyLxt9qjr075I?si=1682464c16bd4fb5&pt=80034ec11c5138c6fc78e0af2c4fb50f 
    ]
    
    for p_id in playlists:
        playlist = sp.playlist(playlist_id=p_id)
        p = playlist["tracks"]
        songs = p["items"]
        while p["next"]:
            p = sp.next(p)
            songs.extend(p["items"])
            
        p = playlist
        p["tracks"]["next"] = None
        p["tracks"]["items"] = songs
        
        json_file_path = f"./data/playlists/playlist-{p_id}.json"
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(p, json_file, indent=4)
            
        print(f"done {p_id} :D !!")
        time.sleep(0.5)

def get_library():
    """
    liked songs
    """
    ## library
    library = sp.current_user_saved_tracks()
    songs = library["items"]
    lib = library
    
    while lib["next"]:
        lib = sp.next(lib)
        songs.extend(lib["items"])
        
    lib["items"] = songs
    lib["next"] = None
    
    json_file_path = f"./data/liked-songs.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(library, json_file, indent=4)
      
if __name__ == "__main__":
    # curr_user = insaneduck

    # get_playlists()
    get_library()
    