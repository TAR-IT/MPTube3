# MPy3 - a YouTube-to-mp3-converter
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TDRC
from pytube import YouTube, exceptions
from decouple import config
import requests
import subprocess
import sys
import os
import re


# default download directory - change to your needs (or use .env file)
DEFAULT_DOWNLOAD_DIRECTORY = config("DEFAULT_DOWNLOAD_DIRECTORY", default=os.path.join(".", "Downloads"))


def main():
    while True:
        # Check if FFmpeg is installed, if not ask to install it
        if not check_ffmpeg():
            install_ffmpeg()
            sys.exit(0)

        # If URL and download location are used in command line arguments, use them
        if len(sys.argv) == 3:
            url = get_valid_url(sys.argv[1])
            download_location = sys.argv[2]
        elif len(sys.argv) == 2:
            # If only URL is provided, use it and ask for the download location
            url = get_valid_url(sys.argv[1])
            download_location = input("\nEnter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
        else:
            # Else try to ask for URL and download location
            url = get_valid_url(input("\nURL: "))
            download_location = input("\nEnter download location (or press Enter for the default directory): ")
            download_location = download_location if download_location else DEFAULT_DOWNLOAD_DIRECTORY
            
        video = YouTube(url)
        metadata = get_metadata(video)
        mp4_file = download_video(video, download_location)
        mp3_file = convert_video(mp4_file)
        attach_metadata(metadata, mp3_file)
        
        print(f"\nCleaning everything up...")
        os.remove(mp4_file)

        repeat = input("\nDone! Do you want to download another file? (y/yes or q/quit to exit): ").lower()
        if repeat in ["q", "quit"]:
            sys.exit(0)
            
def check_ffmpeg():
    try:
        # Use 'where' command on Windows to check for the existence of ffmpeg
        if sys.platform.startswith('win'):
            subprocess.run(['where', 'ffmpeg'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        else:
            # Use 'which' command on Unix-like systems
            subprocess.run(['which', 'ffmpeg'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        return False
    return True

def install_ffmpeg():
    response = input("FFmpeg is not installed. Do you want to install it automatically? (y/n): ").strip().lower()
    if response == 'y':
        if sys.platform.startswith('win'):
            try:
                subprocess.run(['winget', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError:
                print("Error: 'winget' not found. Please make sure it's available on your system or manually install ffmpeg using your package manager.")
                sys.exit(1)

            try:
                subprocess.run(['winget', 'install', 'ffmpeg'], check=True)
                print("FFmpeg has been installed successfully. Please restart your terminal to make use of the changes, otherwise the script does not work.")
            except subprocess.CalledProcessError:
                print("Error installing FFmpeg. Please install it manually.")
                sys.exit(1)
        elif sys.platform.startswith('linux'):
            try:
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
                print("FFmpeg has been installed successfully. Please restart your terminal to make use of the changes, otherwise the script does not work.")
            except subprocess.CalledProcessError:
                print("Error installing FFmpeg. Please install it manually using your package manager.")
                sys.exit(1)
        elif sys.platform.startswith('darwin'):
            try:
                subprocess.run(['/usr/bin/ruby', '-e', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'], check=True)
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
                print("FFmpeg has been installed successfully. Please restart your terminal to make use of the changes, otherwise the script does not work.")
            except subprocess.CalledProcessError:
                print("Error installing FFmpeg. Please install it manually.")
                sys.exit(1)
        else:
            print("Unsupported operating system.")
            sys.exit(1)
    else:
        print("FFmpeg is required for this script. Please install it manually.")
        sys.exit(1)
            

def get_valid_url(url):
    while True:
        try:
            if url.lower() in ['q', 'quit']:
                sys.exit(0)
            return url
        except exceptions.VideoUnavailable:
            print("\nError: The YouTube video is unavailable.")
        except Exception as e:
            print(f"\nError: {e}.")
         
            
def get_metadata(video):
    try:
        metadata = {
            'title': video.title,
            'artist': video.author if video.author else '',
            'year': video.publish_date,
            'thumbnail': requests.get(video.thumbnail_url).content
        }
        return metadata
    except Exception as e:
        print(f"Error fetching YouTube metadata: {e}")
        return None


def download_video(video, download_location):
    print(f"""
          Title: {video.title}
          Author: {video.author}
          Length: {video.length} seconds
          """)

    # Get the best available video stream with a flashing dot
    print("\nGetting highest bitrate stream available...")
    stream = video.streams.get_audio_only()
    print("\nStream found.")

    # Clean the video title to remove invalid characters for use as a file name
    print("\nCleaning title from invalid characters...")
    cleaned_title = re.sub(r'[<>:"/\\|?*]', "", f"{video.author} - {video.title}")
    print(f"\nCleaned Title: {cleaned_title}")

    # Download video to the specified location
    print(f"\nDownloading file to '{download_location}'...")
    os.makedirs(download_location, exist_ok=True)
    mp4_file = os.path.join(download_location, f"{cleaned_title}.mp4")
    stream.download(output_path=download_location, filename=f"{cleaned_title}.mp4")
    print(f"\nThe file has been downloaded successfully to {mp4_file}.")
    return mp4_file
    
    
def convert_video(mp4_file):
    mp3_file = mp4_file.replace('.mp4', '.mp3')

    # Convert video to MP3 using FFmpeg
    print(f"\nConverting file to MP3 using FFmpeg...")
    subprocess.run(['ffmpeg', '-i', mp4_file, '-q:a', '0', '-map', 'a', mp3_file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\nThe file has been converted to MP3 successfully: {mp3_file}")
    return mp3_file
    
    
def attach_metadata(metadata, mp3_file):
    try:
        audio = ID3(mp3_file)
        audio.add(TIT2(encoding=3, text=metadata['title']))
        audio.add(TPE1(encoding=3, text=metadata['artist']))
        audio.add(TDRC(encoding=3, text=str(metadata['year'])))
        audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=metadata['thumbnail']))
        audio.save()
        print("\nMetadata attached to the file.")
    except Exception as e:
        print(f"\nError attaching metadata to the file: {e}")    
    

if __name__ == "__main__":
    main()