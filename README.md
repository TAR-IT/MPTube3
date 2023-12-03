# MPy3 - a YouTube-to-MP3-converter
This is a handy little tool for converting YouTube videos to MP3 files (including meta data) using mainly PyTube and FFmpeg.
I decided to upload this to GiHub, since in my oppinion there are many unsatisfying solutions to this problem for daily usage. Many of the solutions I tried destroyed the MP3 header so that no meta attributes (Titel, Artist etc.) could be set for the files before converting them to mp3 manually using e.g. FFmpeg.

In this approach, the audio stream of the YouTube-video (mp4-format) is downloaded using PyTube and then converted into a mp3 file by ffmpeg, which prevents data corruption. After this, meta data is fetched from the Discogs API (a User Token is needed for this to work).
## Installation
1. Fork/clone the repository or download the repository as a .zip folder and unzip it.
2. Either install the dependencies manually or install using "pipenv":
```bash
pip install pipenv # installs the pipenv package
pipenv install # installs the dependencies using pipenv
```
3. Create a new file called ".env" in the repository and add the following lines:
```bash
DEFAULT_DOWNLOAD_DIRECTORY="./Downloads" # creates a Downloads folder in the current directory - change path if needed
DISCOGS_USER_TOKEN="yourusertoken" # insert your Discogs API User Token
```
4. Run the MPy3 script file via the command line. If you dont have FFmpeg installed yet, it will ask you to install it automatically.
## Usage
Just run the script via
```bash
pipenv run python MPy3.py
```
or if you have manually installed the dependencies:
```bash
python MPy3.py
```

Note: You can also use the program with the URL and/or the download directory as command line arguments:
```bash
pipenv run python MPy3.py "YOUR_URL" "YOUR_DOWNLOAD_DIRECTORY"
```
or
```bash
python MPy3.py "YOUR_URL" "YOUR_DOWNLOAD_DIRECTORY"
```
For fetching meta data via the Discogs API, a Discogs User Token is required. It can either be inserted into the code directly or set as a system variable ("DISCOGS_USER_TOKEN") to be recognized by the program automatically.
## Technologies Used
- [Python](https://www.python.org)
    - The project uses **Python** code mainly.
    - Python packaged used: 
        - [pytube](https://pytube.io/en/latest/)
        - [python-decouple](https://pypi.org/project/python-decouple/)
        - [pipenv](https://pipenv.pypa.io/en/latest/)
- [FFmpeg](https://ffmpeg.org)
    - The project uses FFmpeg to convert mp4 into mp3.
## Roadmap
- Automatically fetching meta data from YouTube, returning it to the Discogs API and attaching Discogs meta data to the file - for better search results.
- Ability to edit meta in the process of using the program.
- Intuitive GUI
