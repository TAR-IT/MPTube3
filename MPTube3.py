import ffmpeg_installer
from pytube import YouTube
import subprocess
import sys
import os


def main():
    # Check if ffmpeg is installed
    if not ffmpeg_installer.check_ffmpeg():
        ffmpeg_installer()
        
    # If URL and download location are used in command line arguments, use them
    if len(sys.argv) == 3:
        url = sys.argv[1]
        download_location = sys.argv[2]
    elif len(sys.argv) == 2:
        # If only URL is provided, use it and ask for the download location
        url = sys.argv[1]
        download_location = str(input("Enter download location (or press Enter for the current directory): "))
        if not download_location:
            download_location = "./"  # Use the current directory if not provided
    else:
        # Else try to ask for URL and download location
        try:
            url = str(input("URL: "))
            download_location = str(input("Enter download location (or press Enter for the current directory): "))
            if not download_location:
                download_location = "./"  # Use the current directory if not provided
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
