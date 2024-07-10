# MPy3 - a YouTube-to-MP3-converter
This is a handy little tool for converting YouTube videos to MP3 files (including meta data) using mainly PyTube and FFmpeg.
I decided to upload this to GitHub, since in my opinion there are many unsatisfying solutions to this problem for daily usage. Many of the solutions I tried destroyed the MP3 header so that no meta attributes (Titel, Artist etc.) could be set for the files before converting them to mp3 manually using e.g. FFmpeg.

In this approach, the audio stream of the YouTube-video (mp4-format) is downloaded using PyTube and then converted into a mp3 file by ffmpeg, which prevents data corruption. After this, meta data is fetched from YouTube and attached to the file. In the next step, more metadata can be fetched from the Discogs API if needed (a User Token is needed for this to work).
## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Getting Started](#getting-started)
    - [Installing](#installing)
    - [Usage](#usage)
3. [License](#license)
## Technologies Used
- [Python](https://www.python.org)
    - The project uses **Python** code mainly.
    - Python packaged used: 
        - [pytube](https://github.com/pytube/pytube)
        - [python-decouple](https://github.com/HBNetwork/python-decouple)
        - [pipenv](https://github.com/pypa/pipenv)
        - [discogs_client](https://github.com/joalla/discogs_client)
        - [mutagen](https://github.com/quodlibet/mutagen)
- [FFmpeg](https://ffmpeg.org)
    - The project uses FFmpeg to convert mp4 into mp3.
## Getting Started
### Installation
1. Fork/clone the repository or download the repository as a .zip folder and unzip it.
2. Either install the dependencies manually or install using "pipenv":
```bash
pip install pipenv # installs the pipenv package
pipenv install # installs the dependencies using pipenv
```
3. Create a new file called ".env" in the repository and add the following lines:
```bash
DEFAULT_DOWNLOAD_DIRECTORY="./Downloads" # creates a Downloads folder in the current directory - change path if needed
DISCOGS_USER_TOKEN="yourusertoken" # insert your Discogs API User Token if you want to fetch meta from there
```
4. Run the MPy3 script file via the command line. If you dont have FFmpeg installed yet, it will ask you to install it automatically.
### Usage
Just run the file MPy3.py (or MPy3.bat of the .py file is making trouble), or run the script via
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
<!-- TODO: ## Testing -->
<!-- TODO: ## Contributing -->
## License
This project, aswell as [pytube](https://github.com/pytube/pytube), is licensed under the [The Unlicense](https://choosealicense.com/licenses/unlicense/).

[FFmpeg](https://ffmpeg.org) is licensed under [GNU Lesser General Public License](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).