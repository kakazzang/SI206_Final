import json
import unittest
import os
import requests
import sqlite3

Youtube_API_KEY = "AIzaSyAIpi4EW96aXHex-_NjErwebb-VdWClSOE"

# unique spotify application information
CLIENT_ID = 'ec98f72977e141cc8e39447422d24888'
CLIENT_SECRET = 'fc4b0dbfb7464faaa5bf91b025703289'
# base URL to request temporary token
AUTH_URL = 'https://accounts.spotify.com/api/token'
# base URL to request v1 information (more info https://developer.spotify.com/documentation/web-api/reference/#/)
BASE_URL = 'https://api.spotify.com/v1/'

# get spotify artist data based unique id
def get_spotify_data(list):
    spotify_data = []
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']

    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    # Track ID from the URI
    for i in range(0,len(list)):
        track_id = list[i]
        # actual GET request with proper header
        r = requests.get(BASE_URL + 'artists/' + track_id, headers=headers)
        d = r.json()
        spotify_data.append(d)
        # print(d)
    return spotify_data

# create youtube api request link
def get_youtube_url(id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={id}&key={Youtube_API_KEY}"
    return url

# access youtube channel api data with specific id
def get_youtube_data(list):
    youtube_data = []
    for i in range(0,len(list)):
        url = get_youtube_url(list[i])
        response = requests.get(url)
        d = response.json()
        youtube_data.append(d)
    return youtube_data

# create spotify json data file for later analysis
def write_spotify_data(filename, data):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as writer:
        writer.write(json_object)

#create youtube json data file for later analysis
def write_youtube_data(filename, data):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as writer:
        writer.write(json_object)

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path+'/'+'music.db')
    cur = conn.cursor()

    filename1 = dir_path + '/' + "spotify.json"
    filename2 = dir_path + '/' + 'youtube.json'
    spotify_id_list = ['7jVv8c5Fj3E9VhNjxT4snq','06HL4z0CvFAxyc27GXpf02','3TVXtAsR1Inumwj472S9r4','4q3ewBCX7sLwd24euuV69X','5K4W6rqBFWDnAN6FQUkS6x','1Xyo4u8uXC1ZmMpatF05PJ','4MCBfE4596Uoi2O4DtmEMz','5f7VJjfbwm532GiveGC0ZK','2YZyLoL8N0Wb9xBt1NhZWg','4oUHIQIBe0LHzYfvXNW4QM','7wlFDEWiM5OoIAt8RSli8b','6KImCVD70vtIoJWnq6nGn3','246dkjvS1zLTtiykXe5h60','1URnnhqYAYcrqrcwql10ft','5cj0lLjcoR7YOSnhnX0Po5','6l3HvQ5sa6mXTsMTB19rO5','7dGJo4pcD2V6oG8kP0tJRR','15UsOTVnJzReFVN1VCnxy4','4O15NlyKLIASxsJ0PrXPfz','6AgTAQt8XS6jRWi4sX7w49','1uNFoZAHBGtllmzznpCI3s','4LLpKhyESsyAXpc4laK94U','6qqNVTkY8uBg9cP3Jd7DAH','0Y5tJX1MQlPlqiwlOH1tJY','66CXWjxzNUsdJxJ2JdwvnR','6eUKZXaKkcviH0Ku9w2n3V','0du5cEVh5yTK9QJze8zA0C','2LIk90788K0zvyj2JJVwkJ','46SHBwWsqBkxI7EeeBEQG7','6Xgp2XMz1fhVYe7i6yNAax','699OTQXzgjhIYAHMy9RyPD','718COspgdWOnwOFpJHRZHS','5pKCCKE2ajJHZ9KAiaK11H','6vWDO969PvNqNYHIOW5v0m','40ZNYROS4zLfyyBSs2PGe2','0hCNtLu0JehylgoiP8L4Gh','7tYKF4w9nC0nq9CsPZTHyP','1McMsnEElThX1knmY4oliG','6LuN9FCkKOj5PcnpouEgny','3qiHUAX7zY4Qnjx8TNUzVx']
    youtube_id_list =['UC_uMv3bNXwapHl8Dzf2p01Q','UCqECaJ8Gagnn7YCbPEzWH6g','UCByOQJjav0CUDwxCk-jVNRQ','UCmBA_wu8xGg1OfOkfW13Q0Q','UCs6eXM7s8Vl5WcECcRHc2qQ','UC0WP5P-ufpRfjbNrmOWwLBQ','UC0BletW9phE4xHFM44q4qKA','UCVS88tG_NYgxF6Udnx2815Q','UC3lBXcrKFnFAFkfVk5WuKcQ','UCzIyoPv6j1MAZpDHKLGP_eA','UClW4jraMKz6Qj69lJf-tODA','UCZFWPqqPkFlNwIxcpsLOwew','UCeLHszkByNZtPKcaVXOCOQQ','UCOjEHmBKwdS7joWpW0VrXkg','UCzpl23pGTHVYqvKsgY0A-_w','UCnc6db-y3IU7CkT_yeVXdVg','UCfM3zsQsOnfWNUppiycmBuw','UCM9r1xn6s30OnlJWb-jc3Sw','UCqwxMqUcL-XC3D9-fTP93Mg','UC0ifXd2AVf1LMYbqwB5GH4g','UCIwFjwMjI0y7PDBVEO9-bkQ','UC3SEvBYhullC-aaEmbEQflg','UCiGm_E4ZwYSHV3bcW1pnSeQ','UCtxdfwb9wfkoGocVUAJ-Bmg','UC9CoOnJkIBMdeijd9qYoT_g','UC0C-w0YjGpqDXGB8IHb662A','UCoUM-UJ7rirJYP8CQ0EIaHA','UC6vZl7Qj7JglLDmN_7Or-ZQ','UChEYVadfkMCfrKUi6qr3I1Q','UCstw-41J8syXgdJ8xWvaizA','UC652oRUvX1onwrrZ8ADJRPw','UCOSIXyYdT93OzpRnAuWaKjQ','UCcgqSM4YEo5vVQpqwN-MaNw','UCuHzBCaKmtaLcRAOoazhCPA','UCwK3C8Vgphad4PweezfUBAQ','UC3jOd7GUMhpgJRBhiLzuLsg','UCO5IQ70V7l-XpHW40HwaGsw','UCy3zgWom-5AGypGX_FVTKpg','UCkntT5Je5DDopF70YUsnuEQ','UCV4UK9LNNLViFP4qZA_Wmfw']
    # print(len(spotify_id_list))
    # print(len(youtube_id_list))
    data1 = get_spotify_data(spotify_id_list)
    write_spotify_data(filename1,data1)
    data2 = get_youtube_data(youtube_id_list)
    write_youtube_data(filename2,data2)
    
main()
    
