from mutagen.id3 import ID3, APIC, TIT2, TPE1, TDRC
import requests

######### METADATA FETCH & ATTACH #########     
def attach(video, mp3_file):
    try:
        # Download thumbnail image
        print("\nDownloading thumbnail...")
        thumbnail_content = requests.get(video.thumbnail_url).content

        print("\nAttaching metadata...")
        # Create an ID3 object
        audio = ID3()

        # Set title, artist, and year tags
        audio.add(TIT2(encoding=3, text=video.title))
        audio.add(TPE1(encoding=3, text=video.author if video.author else ''))
        audio.add(TDRC(encoding=3, text=str(video.publish_date)))

        print("\nAttaching thumbnail...")
        # Set the cover (APIC) tag with the downloaded thumbnail
        audio.add(
            APIC(
                encoding=3,
                mime='image/jpeg',  # Assuming thumbnail is JPEG format
                type=3,             # 3 is for album/cover image
                desc=u'Cover',
                data=thumbnail_content
            )
        )

        # Save the changes to the MP3 file 
        audio.save(mp3_file, v2_version=3)

        print("\nMetadata and thumbnail attached to the file.")
        
    except Exception as e:
        print(f"\nError attaching metadata to the file: {e}")    
        return None
    
if __name__ == "__main__":
    attach()