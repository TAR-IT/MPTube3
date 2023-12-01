# script for checking/installing ffmpeg
import subprocess
import sys


def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        return False
    return True


def install_ffmpeg_windows():
    try:
        subprocess.run(['winget', 'install', '-e', '--id', 'ffmpeg'], check=True)
        print("FFmpeg has been installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing FFmpeg. Please install it manually.")
        sys.exit(1)


def install_ffmpeg_linux():
    try:
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
        print("FFmpeg has been installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing FFmpeg. Please install it manually using your package manager.")
        sys.exit(1)


def install_ffmpeg_macos():
    try:
        subprocess.run(['/usr/bin/ruby', '-e', '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)'], check=True)
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
        print("FFmpeg has been installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing FFmpeg. Please install it manually.")
        sys.exit(1)


def ask_install_ffmpeg():
    response = input("FFmpeg is not installed. Do you want to install it automatically? (y/n): ").strip().lower()
    if response == 'y':
        if sys.platform.startswith('win'):
            install_ffmpeg_windows()
        elif sys.platform.startswith('linux'):
            install_ffmpeg_linux()
        elif sys.platform.startswith('darwin'):
            install_ffmpeg_macos()
        else:
            print("Unsupported operating system.")
            sys.exit(1)
    else:
        print("FFmpeg is required for this script. Please install it manually.")
        sys.exit(1)


def main():
    if not check_ffmpeg():
        ask_install_ffmpeg()


if __name__ == "__main__":
    main()
