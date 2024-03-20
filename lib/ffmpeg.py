import subprocess
import sys


######### FFMPEG DEPENDENCY CHECKS #########            
def check():
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

def install():
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
        
if __name__ == "__main__":
    check()
    install()