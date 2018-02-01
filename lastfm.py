import csv
from datetime import datetime
import os
import pylast

# create your API keys at https://www.last.fm/api/account/create
API_KEY =  # api key
API_SECRET =  # api secret
username =  # your last.fm username

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username)
user = pylast.User(user_name=username, network=network)

# returns limit - 1 results, times in UNIX timestamp in UTC.
# Insert "None" in these fields to pull all data. Warning, that might take a while.
# If you're trying to pull your entire history, I recommend breaking it up into chunks.
recent_tracks = user.get_recent_tracks(limit=None, time_from=None, time_to=None)

track_data = [('Artist', 'Track', 'Album', 'Date', 'Time', 'Duration', 'Artist Top Tag', 'Album Top Tag')]

i = 0
for track in recent_tracks:
    i += 1
    if i % 25 == 0 and i != 0:
        print(str(i) + " : " + str(formatted_date))
    split = str(track).split(", ")
    artist = split[0][32:-1]
    title = split[1][1:-1]
    if track.album is None:
        album = ''
    else:
        album = str(track.album)
    parsed_date = datetime.strptime(track.playback_date, "%d %b %Y, %H:%M")
    formatted_date = parsed_date.strftime("%m-%d-%Y")
    formatted_time = parsed_date.strftime("%H:%M")
    is_new_track = 'Yes'
    if i > 1:
        for data in track_data:
            if data[0] == artist and data[1] == title and data[2] == album:
                duration = data[5]
                artist_top_tag = data[6]
                album_top_tag = data[7]
                is_new_track = 'No'
                break
    if is_new_track == 'Yes':
        try:
            duration_info = pylast.Track(artist, title, network)
            duration = duration_info.get_duration() / 1000
        except:
            duration = ''
        if pylast.Artist(artist, network).get_top_tags(limit=1) == []:
            artist_top_tag = ''
        else:
            artist_top_tag = pylast.Artist(artist, network).get_top_tags(limit=1)[0].item
        if pylast.Album(artist, album, network).get_top_tags(limit=1) == []:
            album_top_tag = ''
        else:
            album_top_tag = pylast.Album(artist, album, network).get_top_tags(limit=1)[0].item
    track_info = (artist, title, album, formatted_date, formatted_time, duration, str(artist_top_tag), str(album_top_tag))
    track_data.append(track_info)

with open('/path/to/file.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for track in track_data:
        writer.writerow(track)
