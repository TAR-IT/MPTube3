# MPTube3 - a YouTube-to-mp3-converter
from lib import ffmpeg_installer
from pytube import YouTube
import subprocess
import sys
import os

# Change default download directory "~/Downloads" to your needs
DEFAULT_DOWNLOAD_DIRECTORY = os.path.expanduser("~/Downloads")

def main():
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
        try:
            url = input("URL: ")
            download_location = input("Enter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
        # Catch invalid URL input
        except ValueError:
            print("Invalid input.")

    download_and_convert_to_mp3(url, download_location)


def download_and_convert_to_mp3(url, download_location):
    # Take URL and download
    video = YouTube(url)
    print(f"Title: {video.title}")
    print("Downloading...")

    # Get the best available video stream
    video_stream = video.streams.get_highest_resolution()

    # Download video to the specified location
    os.makedirs(download_location, exist_ok=True)
    video_file_path = os.path.join(download_location, f"{video.title}.mp4")
    video_stream.download(output_path=download_location, filename=f"{video.title}.mp4")

    # Wait until the file is fully downloaded
    while not os.path.exists(video_file_path):
        pass

    print(f"The video has been downloaded successfully to {video_file_path}.")

    # Convert video to MP3 using FFmpeg
    print(f"Converting video to MP3...")
    subprocess.run(['ffmpeg', '-i', video_file_path, '-q:a', '0', '-map', 'a', video_file_path.replace('.mp4', '.mp3')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Delete the original video file if needed
    os.remove(video_file_path)

    print(f"The video has been converted to MP3 successfully: {video_file_path.replace('.mp4', '.mp3')}.")


if __name__ == "__main__":
    main()
