import requests
import os
from dotenv import load_dotenv 
load_dotenv(override=True)


def search_meta_ads(keyword: str, continuation_token : str = "") -> dict:
    """Fetch ads from Meta Ad Library API using the generated keyword."""
    if(continuation_token == ""):
        url = f"https://meta-ad-library.p.rapidapi.com/search/ads?query={keyword}&active_status=active&media_types=all&ad_type=all&country_code=IN"
    else:
        url = f"https://meta-ad-library.p.rapidapi.com/search/ads?query={keyword}&continuation_token={continuation_token}&active_status=active&media_types=all&ad_type=all&country_code=IN"
    
    headers = {
        "x-rapidapi-host": "meta-ad-library.p.rapidapi.com",
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")  # Store your key in an environment variable
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()
