from sklearn.tree import DecisionTreeClassifier
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials( client_id='30680164aa8a48eb8d6b1a6e1469f0fa', 
    client_secret='9a71c4a8a62043329a538ddcedd00e77',))

features = ['id', 'title', 'danceability', 'energy', 'acousticness', 'mode', 'valence', 'loudness', 'tempo', 'liveness', 'key', 'instrumentalness', 'likes']
reduced_features = ['danceability', 'energy', 'acousticness', 'mode', 'valence', 'loudness', 'tempo', 'liveness', 'key', 'instrumentalness']

# PREPARE USER1 DATA
user1_name = 'kli-17'

# songs they like
user1_likes_pid = 'https://open.spotify.com/playlist/2T75XDoKsI4dCgPxMXz7KV?si=87fa7360a7e4407c'
user1_likes_pid = user1_likes_pid.split('playlist/')[1]
user1_likes_pid = user1_likes_pid.split('?')[0]

user1_likes_data = sp.user_playlist(user1_name, user1_likes_pid, 'tracks')['tracks']
user1_likes_ids = []
user1_likes_titles = []
user1_likes_result = []

for track in user1_likes_data['items']:
    user1_likes_ids.append(track['track']['id'])
    user1_likes_titles.append(track['track']['name'])
    user1_likes_result.append(1)

user1_likes_features = sp.audio_features(user1_likes_ids)
user1_likes_df = pd.DataFrame(data=user1_likes_features, columns=user1_likes_features[0].keys())

user1_likes_df['title'] = user1_likes_titles
user1_likes_df['likes'] = user1_likes_result

user1_likes_df = user1_likes_df[features]


# songs they dislike
user1_dislikes_pid = 'https://open.spotify.com/playlist/6Cf0jO8jFNkQYAd9QVtyZz?si=18052fbdf4384efd'
user1_dislikes_pid = user1_dislikes_pid.split('playlist/')[1]
user1_dislikes_pid = user1_dislikes_pid.split('?')[0]

user1_dislikes_data = sp.user_playlist(user1_name, user1_dislikes_pid, 'tracks')['tracks']
user1_dislikes_ids = []
user1_dislikes_titles = []
user1_dislikes_result = []

for track in user1_dislikes_data['items']:
    user1_dislikes_ids.append(track['track']['id'])
    user1_dislikes_titles.append(track['track']['name'])
    user1_dislikes_result.append(0)

user1_dislikes_features = sp.audio_features(user1_dislikes_ids)
user1_dislikes_df = pd.DataFrame(data=user1_dislikes_features, columns=user1_dislikes_features[0].keys())

user1_dislikes_df['title'] = user1_dislikes_titles
user1_dislikes_df['likes'] = user1_dislikes_result

user1_dislikes_df = user1_dislikes_df[features]

frames = [user1_likes_df, user1_dislikes_df]
user1_df = pd.concat(frames)

# PREPARE USER2 DATA

user2_pid = 'https://open.spotify.com/playlist/2MajKXDlY549dxlCwE5UDp?si=6e2799fb3da44e35'
user2_pid = user2_pid.split('playlist/')[1]
user2_pid = user2_pid.split('?')[0]

user2_data = sp.user_playlist(user1_name, user2_pid, 'tracks')['tracks']
user2_ids = []
user2_titles = []
user2_result = []

for track in user2_data['items']:
    user2_ids.append(track['track']['id'])
    user2_titles.append(track['track']['name'])
    user2_result.append(1)

user2_features = sp.audio_features(user2_ids)
user2_df = pd.DataFrame(data=user2_features, columns=user2_features[0].keys())

user2_df['title'] = user2_titles
user2_df['likes'] = user2_result

user2_df = user2_df[features]

# CLASSIFIER
X_train = user1_df[reduced_features]
y_train = user1_df['likes']
X_test = user2_df[reduced_features]
y_test = user2_df['likes']

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
score = dtc.score(X_test, y_test)
print(score)

