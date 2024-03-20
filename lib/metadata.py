from mutagen.id3 import ID3, APIC, TIT2, TPE1, TDRC, TCON
from decouple import config
import discogs_client
import requests


def main():
    get_youtube_meta()
    get_discogs_meta()


######### YOUTUBE METADATA FETCH & ATTACH #########     
def get_youtube_meta(video, mp3_file):
    try:
        print("Attaching YouTube metadata...")
        # Create an ID3 object
        audio = ID3()

        # Set title, artist, and year tags
        audio.add(TIT2(encoding=3, text=video.title))
        audio.add(TPE1(encoding=3, text=video.author if video.author else ''))
        audio.add(TDRC(encoding=3, text=str(video.publish_date)))
        audio.add(
            APIC(
                encoding=3,
                mime='image/jpeg',  # Assuming thumbnail is JPEG format
                type=3,             # 3 is for album/cover image
                desc=u'Cover',
                data=requests.get(video.thumbnail_url).content
            )
        )

        # Save the changes to the MP3 file 
        audio.save(mp3_file, v2_version=3)
        print("YouTube metadata attached successfully.")
        
    except Exception as e:
        print(f"Error attaching YouTube metadata to the file: {e}")    
        return None
    

######### DISCOGS METADATA FETCH & ATTACH #########
def get_discogs_meta(video, mp3_file):
    try:
        # Access the environment variable - or set user token manually
        user_token = config("DISCOGS_USER_TOKEN", default="")

        # Initialize Discogs client with the user token
        discogs = discogs_client.Client('MPy3.py', user_token=user_token)

        # Search for releases based on the video title
        search_results = discogs.search(f"{video.author} + {video.title}", type='release')
        
        for result in search_results:
            print(f"""
            Title:  {result.title}
            Artist: {', '.join(artist.name for artist in result.artists)}
            Year: {result.year}
            Genre: {', '.join(result.genres)}
            """)
            
            use_metadata = False  # Flag to track whether to use metadata or not

            while True:
                # Ask for permission to attach meta - if not show next result or quit
                use_result = input("Do you want to use this metadata? (y/yes to use, n/no to skip to the next result, q/quit to exit): ").lower()
                if use_result in ["y", "yes"]:
                    use_metadata = True
                    break
                elif use_result in ["n", "no"]:
                    # Skip to the next result
                    break
                elif use_result in ["q", "quit"]:
                    # Quit the function
                    return
                else:
                    print("Invalid input. Please enter 'y', 'n', or 'q'.")

            if use_metadata:
                # Create an ID3 object
                audio = ID3()

                # Set title, artist, and year tags
                audio.add(TIT2(encoding=3, text=result.title))
                audio.add(TPE1(encoding=3, text=result.artists[0].name))
                audio.add(TDRC(encoding=3, text=str(result.year)))
                audio.add(TCON(encoding=3, text=result.genres[0]))
                
                # Set the cover (APIC) tag - this functionality is commented out, since there is a bug with fetching the uri - TODO: Download image and attach file as meta 
                # if result.images:
                #     image_url = result.images[0]['uri']
                #     try:
                #         image_data = requests.get(image_url).content
                #         audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image_data))
                #     except requests.RequestException as e:
                #         print("Error fetching image:", e)
                # else:
                #     print("No images found for this release.")

                # Save the changes to the MP3 file 
                audio.save(mp3_file, v2_version=3)
                print("Discogs metadata attached successfully.")
                print("Metadata used.")
                return  # Exit the function since metadata is used

            print("Attaching metadata...")

    except Exception as e:
        print(f"Error attaching Discogs metadata to the file: {e}")    
        return None



if __name__ == "__main__":
    main()