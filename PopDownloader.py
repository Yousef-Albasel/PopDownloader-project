import pytube
from pytube import Search
import sys

def print_stream_details(streams):
    for i, stream in enumerate(streams):
        if stream.filesize_mb <= 1:
            filesize = f"{round(stream.filesize_kb, 2)} KB"
        elif 1 < stream.filesize_mb < 1000:
            filesize = f"{round(stream.filesize_mb, 2)} MB"
        else:
            filesize = f"{round(stream.filesize_gb, 2)} GB"
        print(i+1, stream.resolution, filesize)

def progress_callback(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = (size - bytes_remaining) / size
    progress_percentage = round(progress * 100)
    print(f"Downloading... {progress_percentage}%")

# Get the YouTube video URL
search_or_url = input("Do you want to 'search' a video or paste a 'url' ? ")

if search_or_url not in ['search', 'url']:
    raise ValueError("Please input a valid option ('search' or 'url')")

if search_or_url == 'search':
    video_search = input("Enter your search query: ")
    video_search_res = Search(video_search)
    print(f"Found {len(video_search_res.results)} results!")
    for i, result in enumerate(video_search_res.results):
        print(f"{i+1}. {result.title} - {result.video_id}")
    selected_video = int(input("Enter the number of the video you want to download: ")) - 1
    selected_video_url = video_search_res.results[selected_video].watch_url
else:
    selected_video_url = input("Enter the YouTube video URL: ")

# Get the YouTube video
youtube_video = pytube.YouTube(selected_video_url, on_progress_callback=progress_callback)
print(f"You are downloading : {youtube_video.title} - {youtube_video.author} ",end="\n")
print(f"Description : {youtube_video.description[0:100]}.. \n")

# Get the video streams
aud_or_vid = input("Do You want to Download an 'audio' File or 'video' File ? ex:(audio) -")
if (aud_or_vid == "audio"):
    audio_streams = youtube_video.streams.filter(only_audio=True )
    print_stream_details(audio_streams)
    # Choose the selected quality
    selected_quality = int(input("Enter the number of the desired quality: ")) - 1
    selected_stream = audio_streams[selected_quality]

elif (aud_or_vid == "video"):
    video_streams = youtube_video.streams.filter(progressive=True).all()
    print_stream_details(video_streams)
    # Choose the selected quality
    selected_quality = int(input("Enter the number of the desired quality: ")) - 1
    selected_stream = video_streams[selected_quality]

# Choose location
download_location = input("Where do you want to download your video ? :")

# Download the video
print("Starting download...")
selected_stream.download(output_path=download_location)
print("Download complete!")
exit()