import csv
from datetime import datetime
import os
import pylast

# create your API keys at https://www.last.fm/api/account/create
api_key =  os.getenv('LASTFM_API_KEY')
api_secret =  os.getenv('LASTFM_API_SECRET')
username =  # your last.fm username

network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret, username=username)
user = pylast.User(user_name=username, network=network)

# Times in UNIX timestamp in UTC.
# Insert "None" in these fields to pull all data. Warning, that might take a while.
recent_tracks = user.get_recent_tracks(limit=100, time_from=None, time_to=None)
track_data = [('Artist', 'Track', 'Album', 'Date', 'Time')] 

for track in recent_tracks:
    split = str(track).split(", ")
    artist = split[0][32:-1]
    title = split[1][1:-1]
    if track.album is None:
        album = ''
    else:
        album = str(track.album)
    parsed_date = datetime.strptime(track.playback_date, "%d %b %Y, %H:%M")
    formatted_date = parsed_date.strftime("%Y-%m-%d")
    formatted_time = parsed_date.strftime("%H:%M")

    # Fix some encoding errors and output everything in UTF-8
    track_info = (artist.encode('ascii', 'ignore').decode('utf-8'), title.encode('ascii', 'ignore').decode('utf-8'), album.encode('ascii', 'ignore').decode('utf-8'), formatted_date, formatted_time) 
    track_data.append(track_info)

with open('/path/to/file.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for track in track_data:
        writer.writerow(track)
