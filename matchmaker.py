import tree

data1 = tree.user1_likes_data
data2 = tree.user2_data
df1 = tree.user1_likes_df
df2 = tree.user2_df
artists1 = tree.user1_artists
artists2 = tree.user2_artists

# finding artists they both like 
shared_artists = []
for i in artists1:
    for j in artists2:
        if i == j and i not in shared_artists:
            shared_artists.append(i)

# finding features they both like
target_features = ['danceability', 'energy', 'acousticness', 'valence']
shared_features = []

for feature in target_features:
    if df1[feature].mean() > 0.5 and df2[feature].mean() > 0.5:
        shared_features.append(str("high " + feature))
    elif df1[feature].mean() < 0.5 and df2[feature].mean() < 0.5:
        shared_features.append(str("low " + feature))

# RESULTS
print(tree.user1_name + " and " + tree.user2_name + " are " + str(tree.compatibility * 100) + " percent compatible.\n")

if len(shared_artists) == 0:
    print("They don't like any of the same artists")
else:
    print("Artists they both like are: " + str(shared_artists) + "\n")

print("They both like songs that have: " + str(shared_features) + "\n")