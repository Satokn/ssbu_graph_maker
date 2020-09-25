import youtube_dl, os, sys

def download(url):
    VIDEO_DIR = os.getcwd()

    try:
        os.remove("{}/video.mp4".format(VIDEO_DIR))
    except:
        pass

    ydl_opts = {'outtmpl': '{}/video.mp4'.format(VIDEO_DIR)}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download(sys.argv[1])