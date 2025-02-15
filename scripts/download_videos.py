import multiprocessing
from SoccerNet.Downloader import SoccerNetDownloader

downloader = SoccerNetDownloader(LocalDirectory="./data/soccer_videos")
downloader.password = "s0cc3rn3t"

train_videos = [f"{i}_224p.mkv" for i in range(1, 11)]
test_videos = [f"{i}_224p.mkv" for i in range(11, 14)]

def download_video(video_file, split):
    downloader.downloadGames(files=[video_file], split=[split])

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=6)  # Adjust based on CPU
    tasks = [(video, "train") for video in train_videos] + [(video, "test") for video in test_videos]
    pool.starmap(download_video, tasks)
    pool.close()
    pool.join()
    
print("✅ Faster parallel download completed!")
