# MPT3.py - a YouTube-to-MP3-converter using PyTube
This is a handy little tool for converting YouTube videos to mp3 files using PyTube and FFMPEG.
I decided to upload this to GiHub, since there is many unsatisfying solutions to this problem for daily usage. Many of the solutions I tried destroyed the MP3 header so that no meta attributes could be set for the files.

In this approach, the video is downloaded from YouTube using PyTube and then converted into a mp3 file by ffmpeg, which is a more safe way to prevent data corruption.

This program can be used by either 
1. just running the file ("python MPT3.py") or 
2. using the URL and/or the download directory as command line arguments ("python MPT3.py https://www.youtube.com/watch... C:/Users/...").
## Installation
1. Fork/clone the repository or download the repository as a .zip folder and unzip it.
2. Install ffmpeg (if you don't already have it). For windows, you can type "winget install ffmpeg" into the terminal.
3. Run the .py file.
## Technologies Used
- [Python](https://www.python.org)
    - The project uses **Python** code mainly.
- [FFmpeg](https://ffmpeg.org)
    - The project uses FFmpeg to convert mp4 into mp3.

