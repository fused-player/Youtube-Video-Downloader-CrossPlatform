from pytubefix import YouTube
from pytubefix.cli import on_progress

def on_complete(stream, file_path):
    print("\n✅ Download complete:", file_path)

res = []
url = "https://youtu.be/BuAGbpDZS38?si=-EGWHVqmBxc3DFFz"
yt = YouTube(
    url,
    on_progress_callback=on_progress,
    on_complete_callback=on_complete
)

for stream in yt.streams:
    #print(stream.resolution)
    if stream.resolution:
        res.append(stream.resolution)


print(list(set(res)))
# print("📹 Title:", yt.title)

ys = yt.streams.get_highest_resolution()
print(yt.thumbnail_url)
print(ys.filesize_mb)
# ys.download()
