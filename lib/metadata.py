###############################################################
######### metadata.py - helper for fetching metadata ##########
###############################################################

############ LIBRARIES ###########
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TDRC, TCON, TALB
from decouple import config
import discogs_client
import requests


######### MAIN FUNCTION #########
def main():
    get_youtube_meta()
    get_discogs_meta()


######### YOUTUBE METADATA FETCH & ATTACH #########     
def get_youtube_meta(video, mp3_file):
    try:
        # Print results to user
        print(f"""
        Title:  {video.title}
        Artist: {video.author if video.author else ''}
        Year: {video.publish_date}
        Thumbnail URL: {video.thumbnail_url}
        """)
        
        use_metadata = False
        
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
        print(f"Error fetching/attaching YouTube metadata: {e}")    
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
            # Fetch master information to get the correct album name
            master_release = discogs.master(result.master.id)
            album_name = master_release.title
            
            # Print results to user
            print(f"""
            Title:  {result.title}
            Artist: {', '.join(artist.name for artist in result.artists)}
            Album: {album_name}
            Year: {result.year}
            Genre: {', '.join(result.genres)}
            Cover URL: {result.images[0]['uri']}
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
                audio.add(TALB(encoding=3, text=album_name))
                audio.add(TDRC(encoding=3, text=str(result.year)))
                audio.add(TCON(encoding=3, text=result.genres[0]))
                 
                # Set the cover (APIC) tag
                if result.images:
                    image_url = result.images[0]['uri']
                    image_filename = 'album_cover.jpg'
                    if download_image(image_url, image_filename):
                        with open(image_filename, 'rb') as image_file:
                            image_data = image_file.read()
                            audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image_data))
                    else:
                        print("Failed to attach album artwork: Image download failed.")
                else:
                    print("No images found for this release.")

                # Save the changes to the MP3 file 
                audio.save(mp3_file, v2_version=3)
                print("Discogs metadata attached successfully.")
                print("Metadata used.")
                return  # Exit the function since metadata is used

    except Exception as e:
        print(f"Error fetching/attaching Discogs metadata: {e}")    
        return None
 
 
def download_image(image_url, filename):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        else:
            print(f"Failed to download image: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False
    

if __name__ == "__main__":
    main()