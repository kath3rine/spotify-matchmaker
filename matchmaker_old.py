# ignore this file (just for personal reference)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials( client_id='30680164aa8a48eb8d6b1a6e1469f0fa', 
    client_secret='9a71c4a8a62043329a538ddcedd00e77',))

# list of matches
matches = []

# URIs: creates lists of track ID's, titles, and artists for each person
# user
my_uri = input('Enter your URI: \n') 
my_username = my_uri.split(':')[2]
my_playlist_id = my_uri.split(':')[4]
my_results = sp.user_playlist(my_username, my_playlist_id, 'tracks')

my_data = my_results['tracks'] 

my_titles = []
my_artists = []
my_ids = []

for track in my_data['items']:
    my_ids.append(track['track']['id'])
    my_titles.append(track['track']['name'])
    track_artist = ''
    for artist in track['track']['artists']:
        track_artist = artist['name']
    my_artists.append(track_artist)

# Potential Match
their_name = input('Enter their name: \n') 
their_uri = input('Enter their URI: \n') 
their_username = their_uri.split(':')[2]
their_playlist_id = their_uri.split(':')[4]
their_results = sp.user_playlist(their_username, their_playlist_id, 'tracks')

their_data = their_results['tracks']

their_titles = []
their_artists = []
their_ids = []

for track in their_data['items']:
    their_ids.append(track['track']['id'])
    their_titles.append(track['track']['name'])
    track_artist = ''
    for artist in track['track']['artists']:
        track_artist = artist['name']
    their_artists.append(track_artist)

# artists both people like
shared_artists = []
for i in my_artists:
    for j in their_artists:
        if i == j and i not in shared_artists:
            shared_artists.append(i)

#Potential match's favorite artists
no_dupes = [*set(their_artists)]
counts = [] # num of occurences of each song
for i in no_dupes:
    curr_count = 0
    for j in their_artists:
        if i == j:
            curr_count = curr_count + 1
    counts.append(curr_count)
faves = []
for i in range(len(counts)):
   if counts[i] == max(counts):
       faves.append(no_dupes[i])

# extract audio features from each person's songs 
import numpy as np
my_features = sp.audio_features(my_ids)
their_features = sp.audio_features(their_ids)
# extracting traits (scale from 0 to 1, 1 is the highest amount)
def avg(lst):
    return sum(lst) / len(lst)
# empty list of the traits in DF
my_dance = []
my_energy = []
my_acoustic = []
my_mode = []
my_valence = []
my_loud = []
my_tempo = []

# add data from prev secion
for track in my_features:
    my_dance.append(track['danceability'])
    my_energy.append(track['energy'])
    my_acoustic.append(track['acousticness'])
    my_mode.append(track['mode'])
    my_valence.append(track['valence'])
    my_loud.append(track['loudness'])
    my_tempo.append(track['tempo'])

# scaled
my_loud_scl = 1 - (abs(avg(my_loud)) - 2) / 9 
my_tempo_scl = (avg(my_tempo) - 61) / 122

# repeat for PM
their_dance = []
their_energy = []
their_acoustic = []
their_mode = []
their_valence = []
their_loud = []
their_tempo = []
for track in their_features:
    their_dance.append(track['danceability'])
    their_energy.append(track['energy'])
    their_acoustic.append(track['acousticness'])
    their_mode.append(track['mode'])
    their_valence.append(track['valence'])
    their_loud.append(track['loudness'])
    their_tempo.append(track['tempo'])

# scaled
their_loud_scl = 1 - (abs(avg(their_loud)) - 2) / 9 # mean = -6.4, stdev = 2.3
their_tempo_scl = (avg(their_tempo) - 61) / 122 # mean = 123, stdev = 30.5
# create list of audio traits both users like, based on their avg scores for each individual characteristic
# cutoff values are +/- 0.5 stdev from the mean (using spotify's "Top 50" playlist as a benchmark)
traits = []

if avg(my_dance) > 0.57 and avg(their_dance) > 0.57:
    traits.append("danceable")
elif avg(my_dance) < 0.43 and avg(their_dance) > 0.43:
    traits.append("undanceable")
    
if avg(my_energy) > 0.58 and avg(their_energy) > 0.58:
    traits.append("energetic")
elif avg(my_energy) < 0.42 and avg(their_energy) < 0.42:
    traits.append("chill")
    
if avg(my_acoustic) > 0.62 and avg(their_acoustic) > 0.62:
    traits.append("acoustic")
elif avg(my_acoustic) < 0.38 and avg(their_acoustic) < 0.38:
    traits.append("electronically produced")
    
if avg(my_mode) > 0.7 and avg(their_mode) > 0.7:
    traits.append("written in a major key")
elif avg(my_mode) < 0.3 and avg(their_mode) < 0.3:
    traits.append("written in a minor key")
    
if avg(my_valence) > 0.72 and avg(their_valence) > 0.72:
    traits.append("happy")
elif avg(my_valence) < 0.28 and avg(their_valence) < 0.28:
    traits.append("sad")
    
if my_loud_scl > 0.64 and their_loud_scl > 0.64: 
    traits.append("loud")
elif my_loud_scl < 0.36 and their_loud_scl < 0.36:
    traits.append("quiet")

if my_tempo_scl > 0.66 and their_tempo_scl > 0.66: 
    traits.append("fast")
elif my_tempo_scl < 0.33 and their_tempo_scl < 0.33:
    traits.append("slow")

# REDO THIS PART W/ DECISION TREES


# computes compatibility scores from 0 to 1 (1 is most similar)
def get_score(lst1, lst2):
    return (1 - abs(avg(lst1) - avg(lst2)))

# individual trait
dance_score = get_score(my_dance, their_dance) 
energy_score = get_score(my_energy, their_energy)
acoustic_score = get_score(my_acoustic, their_acoustic)
mode_score = get_score(my_mode, their_mode) 
valence_score = get_score(my_valence, their_valence)
loud_score = 1 - abs(my_loud_scl - their_loud_scl)
tempo_score = 1 - abs(my_tempo_scl - their_tempo_scl)

# average of individuals
raw = (dance_score + energy_score + acoustic_score + mode_score 
       + valence_score + loud_score + tempo_score) / 7

# rounded & scaled
compatibility = round(100 * (2 * raw - 1), 3)

# if compatibility < 0 -> set to 0
if compatibility < 0: 
    compatibility = 0

# Final Output 
print()
print("Your URI: " + my_uri)
print(their_name + "'s URI: " + their_uri)
print()

# compatibility score
if compatibility > 80:
    print("Congratulations!")
if (compatibility < 20):
    print("Uh oh :( ")
print("You and " + their_name + " are " + str(compatibility) + "% compatible.")
print()

# their favorite artists
print(their_name + "'s favorite artist(s) are: ")
print(faves)
print()

# shared artists/traits
if len(shared_artists) != 0:
    print("You both listen to: ")
    print(shared_artists)
else:
    print("You don't like any of the same artists :(")
print()

if len(traits) != 0:
    print("You both like songs that are: ")
    print(traits)
    print()

# match?
response = input('Do you want to match? (yes/no)')
if response == "yes":
    matches.append(their_name)

print("Your matches are: ")
print(matches)

