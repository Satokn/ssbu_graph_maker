import youtube_dl, os

def download(url):
    VIDEO_DIR = os.getcwd()

    os.remove("{}/video.mp4".format(VIDEO_DIR))
    ydl_opts = {'outtmpl': '{}/video.mp4'.format(VIDEO_DIR)}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])