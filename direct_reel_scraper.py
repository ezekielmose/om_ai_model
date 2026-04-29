# scraper/direct_reel_scraper.py

import requests
import tempfile

def direct_reel_scraper(reel_url: str) -> str:
    """
    Downloads reel temporarily and returns a usable file path.
    Even though it's 'direct', OpenCV still needs a file.
    """

    response = requests.get(reel_url, stream=True)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch reel: {reel_url}")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            temp_file.write(chunk)

    temp_file.close()

    return temp_file.name