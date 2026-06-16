import re
import urllib.request

# 1. Fetch the official media player source code for Hungary Duna TV
try:
    req = urllib.request.Request(
        "https://player.mediaklikk.hu/playernew/player.php?video=mtv1live",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    html = urllib.request.urlopen(req).read().decode('utf-8')

    # 2. Extract the live tokenized .m3u8 URL from the script layout
    match = re.search(r'"file":\s*"(https:\\/\\/.*\.m3u8\?.*)"', html)
    if match:
        live_url = match.group(1).replace(r'\/', '/')
        print(f"Successfully pulled fresh token: {live_url}")
        
        # 3. Read your existing stream file and update the link
        with open("stream.m3u", "r") as file:
            content = file.read()

        # Regex replaces the old link right underneath your DUNA TV header block
        updated_content = re.sub(
            r'(#EXTINF:-1.*DUNA TV\n)https:\/\/.*\.m3u8.*',
            r'\1' + live_url,
            content
        )

        with open("stream.m3u", "w") as file:
            file.write(updated_content)
            
except Exception as e:
    print(f"Error scraping tokens: {e}")
