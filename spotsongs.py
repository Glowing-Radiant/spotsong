import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API credentials
client_id = 'your-client-id'
client_secret = 'your-client-secret'
redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-modify-public'

# Ask user whether to scan current directory or enter folder path
while True:
    option = input("Enter '1' to scan current directory or '2' to enter folder path: ")
    if option == '1':
        folder_path = os.getcwd()
        break
    elif option == '2':
        folder_path = input("Enter folder path to scan: ")
        if not os.path.exists(folder_path):
            print(f"Folder path '{folder_path}' does not exist.")
        else:
            break
    else:
        print("Invalid option. Please enter '1' or '2'.")

# Set up logging to write to file
log_file_path = os.path.join(folder_path, 'playlist.log')
if os.path.exists(log_file_path):
    os.remove(log_file_path) # Remove previous log file
log_file = open(log_file_path, 'w')

# Set up Spotify API authentication and create new playlist
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri=redirect_uri, scope=scope))
playlist_name = os.path.basename(folder_path) # Use folder name as playlist name
playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, public=False)

# Loop through files in folder and add songs to playlist
for filename in os.listdir(folder_path):
    song_name = os.path.splitext(filename)[0]
    results = sp.search(q=song_name, type='track')
    if results['tracks']['total'] > 0:
        track_uri = results['tracks']['items'][0]['uri']
        response = sp.playlist_add_items(playlist_id=playlist['id'], items=[track_uri])
        if response['snapshot_id']:
            log_file.write(f"Added '{song_name}' to playlist.\n")
        else:
            log_file.write(f"Failed to add '{song_name}' to playlist.\n")
    else:
        log_file.write(f"No results found for '{song_name}'.\n")
log_file.close()
