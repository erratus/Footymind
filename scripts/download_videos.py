from SoccerNet.Downloader import SoccerNetDownloader

# Define the directory to save videos
downloader = SoccerNetDownloader(LocalDirectory="./data/soccer_videos")

# List of available competitions (example: English Premier League)
competitions = ['england_epl', 'france_ligue-1', 'spain_laliga']

# Download videos for the selected competitions
downloader.downloadGames(competitions)

print("Download complete!")