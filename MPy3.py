#####################################################
######### MPy3 - a YouTube-to-mp3-converter #########
#####################################################

############ LIBRARIES ###########
from pytube import YouTube, exceptions
from decouple import config
import subprocess
import sys
import os
import re

from lib import ffmpeg, metadata

############# CONFIG #############
# default download directory - change to your needs (or use .env file)
# You can also just create a file called ".env" in this same directory
# and add the following line: 
# DEFAULT_DOWNLOAD_DIRECTORY="./Downloads"
DEFAULT_DOWNLOAD_DIRECTORY = config("DEFAULT_DOWNLOAD_DIRECTORY", default=os.path.join(".", "Downloads"))

######### MAIN FUNCTION #########
def main():
    # Exit if file is started e.g. in pipeline or GitHub Actions
    if not sys.stdin.isatty():
       sys.exit(0)
    while True:
        # Check if FFmpeg is installed, if not ask to install it
        if not ffmpeg.check():
            ffmpeg.install()
            sys.exit(0)

        # If URL and download location are used in command line arguments, use them
        if len(sys.argv) == 3:
            url = get_valid_url(sys.argv[1])
            download_location = sys.argv[2]
        elif len(sys.argv) == 2:
            # If only URL is provided, use it and ask for the download location
            url = get_valid_url(sys.argv[1])
            download_location = input("Enter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
        else:
            # Else try to ask for URL and download location
            url = get_valid_url(input("URL: "))
            download_location = input("Enter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
            
        # create video object, download video and convert to mp3
        video = YouTube(url)
        mp3_file = download_and_convert_video(video, download_location)
        
        # adding YouTube meta
        metadata.get_youtube_meta(video, mp3_file)
        
        while True:
            # ask to fetch Discogs meta and add it to the file (overwriting the YouTube meta)
            discogs_answer = input("Do you want to search Discogs for metadata as well? (y/yes or n/no): ").lower()
            if discogs_answer in ["y", "yes"]:
                metadata.get_discogs_meta(video, mp3_file)
                break
            elif discogs_answer in ["n", "no"]:
                break
            else:
                print("Invalid input. Please enter 'y'/'yes' or 'n'/'no'.")

        # repeat or exit
        repeat = input("Done! Do you want to download another file? (Press Enter to start over or n/no/q/quit to exit): ").lower()
        if repeat in ["q", "quit", "n", "no"]:
            sys.exit(0)


######### URL VALIDATION ######### 
def get_valid_url(url):
    while True:
        try:
            if url.lower() in ['q', 'quit']:
                sys.exit(0)
            return url
        except exceptions.VideoUnavailable:
            print("Error: The YouTube video is unavailable.")
        except Exception as e:
            print(f"Error: {e}.")


######### VIDEO DOWNLOAD AND CONVERTION ######### 
def download_and_convert_video(video, download_location):
    print(f"""
          Title: {video.title}
          Author: {video.author}
          Length: {video.length} seconds
          """)

    # Get the best available video stream with a flashing dot
    print("Getting highest bitrate stream available...")
    stream = video.streams.get_audio_only()

    # Clean the video title to remove invalid characters for use as a file name
    print("Stream found. Cleaning title from invalid characters...")
    cleaned_title = re.sub(r'[<>:"/\\|?*]', "", f"{video.author} - {video.title}")

    # Download video to the specified location
    print(f"""
          Cleaned Title: {cleaned_title}
          Downloading file to '{download_location}'...
          """)
    os.makedirs(download_location, exist_ok=True)
    mp4_file = os.path.join(download_location, f"{cleaned_title}.mp4")
    stream.download(output_path=download_location, filename=f"{cleaned_title}.mp4")
    print(f"The file has been downloaded successfully to {mp4_file}.")
    
    mp3_file = mp4_file.replace('.mp4', '.mp3')

    # Convert video to MP3 using FFmpeg
    print("Converting file to MP3 using FFmpeg...")
    subprocess.run(['ffmpeg', '-i', mp4_file, '-q:a', '0', '-map', 'a', mp3_file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"The file has been converted to MP3 successfully: {mp3_file}")

    print("Cleaning everything up...")
    os.remove(mp4_file)
    
    return mp3_file
 

if __name__ == "__main__":
    main()