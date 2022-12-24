import tree

# finding artists they both like 
shared_artists = []
for artist in tree.user1_artists:
    if artist in tree.user2_artists and artist not in shared_artists:
        shared_artists.append(artist)

# finding songs they both like
shared_songs = []
for song in tree.user1_likes_titles:
    if song in tree.user2_titles and song not in shared_songs:
        shared_songs.append(song)

# finding features they both like
target_features = ['danceability', 'energy', 'acousticness', 'valence']
shared_features = []

for feature in target_features:
    if tree.user1_likes_df[feature].mean() > 0.5 and tree.user2_df[feature].mean() > 0.5:
        shared_features.append(str("high " + feature))
    elif tree.user1_likes_df[feature].mean() < 0.5 and tree.user2_df[feature].mean() < 0.5:
        shared_features.append(str("low " + feature))

# RESULTS
if len(shared_artists) != 0:
    print("Artists they both like are: " + str(shared_artists) + "\n")

if len(shared_songs) != 0:
    print("Songs they both like are: " + str(shared_songs) + "\n")

if len(shared_features) != 0:
    print("They both like songs that have: " + str(shared_features) + "\n")