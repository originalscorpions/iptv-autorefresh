import subprocess
import re

def get_live_url():
    try:
        # Use yt-dlp to extract the raw, direct live token link
        # --get-url grabs the final authentic streaming manifest instantly
        result = subprocess.run(
            ["yt-dlp", "--get-url", "https://www.mediaklikk.hu/duna-elo/"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        if ".m3u8" in url:
            print(f"Extracted token url successfully: {url}")
            return url
    except Exception as e:
        print(f"Error executing yt-dlp stream grabber: {e}")
    return None

live_url = get_live_url()

if live_url:
    # Read the existing playlist layout
    try:
        with open("stream.m3u", "r") as file:
            content = file.read()

        # Overwrite the old address underneath the Duna TV channel definition
        updated_content = re.sub(
            r'(#EXTINF:-1.*DUNA TV\n)https:\/\/.*\.m3u8.*',
            r'\1' + live_url,
            content
        )

        with open("stream.m3u", "w") as file:
            file.write(updated_content)
        print("stream.m3u updated with the fresh link.")
    except Exception as e:
        print(f"File writing error: {e}")
