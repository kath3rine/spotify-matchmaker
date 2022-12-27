import data
from sklearn.tree import DecisionTreeClassifier

target_features = ['danceability', 'energy', 'acousticness', 'valence']
reduced_features = ['danceability', 'energy', 'acousticness', 'mode', 'valence', 'loudness', 'tempo', 'liveness', 'key', 'instrumentalness']

def find_compatibility(X_train, y_train, X_test, y_test):
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    compatibility = dtc.score(X_test, y_test)
    print(data.user1_name + " and " + data.user2_name + " are " + str(compatibility * 100) + "% compatible\n")

def find_shared_artists(): 
    shared_artists = []
    for artist in data.user1_artists:
        if artist in data.user2_artists and artist not in shared_artists:
            shared_artists.append(artist)
    if len(shared_artists) != 0:
        print("Artists they both like are: " + str(shared_artists) + "\n")

def find_shared_songs():
    shared_songs = []
    for song in data.user1_likes_titles:
        if song in data.user2_titles and song not in shared_songs:
            shared_songs.append(song)
    if len(shared_songs) != 0:
        print("Songs they both like are: " + str(shared_songs) + "\n")

def find_shared_features(target_features): 
    shared_features = []
    for feature in target_features:
        if data.user1_likes_df[feature].mean() > 0.5 and data.user2_df[feature].mean() > 0.5:
            shared_features.append(str("high " + feature))
        elif data.user1_likes_df[feature].mean() < 0.5 and data.user2_df[feature].mean() < 0.5:
            shared_features.append(str("low " + feature))
    if len(shared_features) != 0:
        print("They both like songs that have: " + str(shared_features) + "\n")


# DRIVER
find_compatibility(data.user1_df[reduced_features], data.user1_df['likes'], data.user2_df[reduced_features], data.user2_df['likes'])
find_shared_artists()
find_shared_songs()
find_shared_features(target_features)




