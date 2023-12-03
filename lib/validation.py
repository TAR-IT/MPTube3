import sys
import re
from pytube import YouTube, exceptions


def main():
    get_valid_url()
    clean_filename()


def get_valid_url():
    while True:
        try:
            url = input("URL: ")
            if url.lower() in ['q', 'quit']:
                sys.exit(0)
            video = YouTube(url)  # Try creating a YouTube object with the input URL
            return url
        except exceptions.VideoUnavailable:
            print("Error: The YouTube video is unavailable.")
        except Exception as e:
            print(f"Error: {e}.")


def clean_filename(title):
    # Remove invalid characters from the title to make it suitable as a file name
    cleaned_title = re.sub(r'[<>:"/\\|?*]', '', title)
    return cleaned_title

if __name__ == "__main__":
    main()
