# MPTube3 - a YouTube-to-mp3-converter
from lib import ffmpeg_installer
from pytube import YouTube
import subprocess
import sys
import os
import re

# default download directory "~\Downloads" - change to your needs
DEFAULT_DOWNLOAD_DIRECTORY = os.path.expanduser("~\Downloads")


def get_valid_url():
    while True:
        try:
            url = input("URL: ")
            if url.lower() in ['q', 'quit']:
                sys.exit(0)
            YouTube(url)  # Try creating a YouTube object with the input URL
            return url
        except Exception as e:
            print("Invalid URL. Please enter a valid YouTube URL.")


def clean_filename(title):
    # Remove invalid characters from the title to make it suitable as a file name
    cleaned_title = re.sub(r'[<>:"/\\|?*]', '', title)
    return cleaned_title


def main():
    while True:
        # Check if FFmpeg is installed, if not ask to install it
        if not ffmpeg_installer.check_ffmpeg():
            ffmpeg_installer.ask_install_ffmpeg()
            sys.exit(0)

        # If URL and download location are used in command line arguments, use them
        if len(sys.argv) == 3:
            url = sys.argv[1]
            download_location = sys.argv[2]
        elif len(sys.argv) == 2:
            # If only URL is provided, use it and ask for the download location
            url = sys.argv[1]
            download_location = input("Enter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
        else:
            # Else try to ask for URL and download location
            url = get_valid_url()
            download_location = input("Enter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY

        download_and_convert_to_mp3(url, download_location)

        repeat = input("Do you want to download another file? (y/yes or q/quit to exit): ").lower()
        if repeat in ['q', 'quit']:
            sys.exit(0)


def download_and_convert_to_mp3(url, download_location):
    # Take URL and download
    video = YouTube(url)
    print(f"Title: {video.title}")
    print(f"Length: {video.length} seconds")

    # Get the best available video stream
    print("Getting highest bitrate stream available...")
    video_stream = video.streams.get_audio_only()

    # Clean the video title to remove invalid characters for use as a file name
    cleaned_title = clean_filename(video.title)
    print(f"Cleaned Title: {cleaned_title}")

    # Download video to the specified location
    print(f"Downloading file to '{download_location}'...")
    os.makedirs(download_location, exist_ok=True)
    video_file_path = os.path.join(download_location, f"{cleaned_title}.mp4")
    video_stream.download(output_path=download_location, filename=f"{cleaned_title}.mp4")

    # Wait until the file is fully downloaded
    while not os.path.exists(video_file_path):
        pass
    print(f"The file has been downloaded successfully to {video_file_path}.")

    # Convert video to MP3 using FFmpeg
    print(f"Converting file to MP3 using FFmpeg...")
    subprocess.run(['ffmpeg', '-i', video_file_path, '-q:a', '0', '-map', 'a', video_file_path.replace('.mp4', '.mp3')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"The file has been converted to MP3 successfully: {video_file_path.replace('.mp4', '.mp3')}.")

    # Delete the original video file if needed
    print(f"Deleting old file...")
    os.remove(video_file_path)
    print(f"Done!")


if __name__ == "__main__":
    main()
