import json
import unittest
import os
import requests

Youtube_API_KEY = "AIzaSyAIpi4EW96aXHex-_NjErwebb-VdWClSOE"

CLIENT_ID = 'ec98f72977e141cc8e39447422d24888'
CLIENT_SECRET = 'fc4b0dbfb7464faaa5bf91b025703289'
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

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

def get_youtube_url(id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={id}&key={Youtube_API_KEY}"
    return url

def get_youtube_data(list):
    youtube_data = []
    for i in range(0,len(list)):
        url = get_youtube_url(list[i])
        response = requests.get(url)
        d = response.json()
        youtube_data.append(d)
    return youtube_data

def write_spotify_data(filename, data):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as writer:
        writer.write(json_object)

def write_youtube_data(filename, data):
    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as writer:
        writer.write(json_object)

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename1 = dir_path + '/' + "spotify.json"
    filename2 = dir_path + '/' + 'youtube.json'
    spotify_id_list = ['7jVv8c5Fj3E9VhNjxT4snq','06HL4z0CvFAxyc27GXpf02']
    youtube_id_list =['UC_uMv3bNXwapHl8Dzf2p01Q','UCqECaJ8Gagnn7YCbPEzWH6g']
    # print(len(spotify_id_list))
    data1 = get_spotify_data(spotify_id_list)
    write_spotify_data(filename1,data1)
    data2 = get_youtube_data(youtube_id_list)
    write_youtube_data(filename2,data2)
    
main()
    
