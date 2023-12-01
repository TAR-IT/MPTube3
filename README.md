# MPy3 - a YouTube-to-MP3-converter
This is a handy little tool for converting YouTube videos to mp3 files using PyTube and FFMPEG.
I decided to upload this to GiHub, since there is many unsatisfying solutions to this problem for daily usage. Many of the solutions I tried destroyed the MP3 header so that no meta attributes (Titel, Artist etc.) could be set for the files.

In this approach, the video (mp4-format) is downloaded from YouTube using PyTube and then converted into a mp3 file by ffmpeg, which prevents data corruption.
## Installation
1. Fork/clone the repository or download the repository as a .zip folder and unzip it.
2. Install ffmpeg (if you don't already have it). If you run the script, it will ask you to automatically install it.
3. Run the MPTube3.py file via the command line.
## Usage
1. just running the script via
```
python MPTube3.py
```
or

2. using the URL and/or the download directory as command line arguments
```bash
python MPy3.py "YOUR_URL" "YOUR_DOWNLOAD_DIRECTORY"
```
## Technologies Used
- [Python](https://www.python.org)
    - The project uses **Python** code mainly.
- [FFmpeg](https://ffmpeg.org)
    - The project uses FFmpeg to convert mp4 into mp3.
## Roadmap
- Automatically fetching meta data and saving it to the mp3-file
- GUI
