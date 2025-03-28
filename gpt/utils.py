from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_KEY = os.environ.get('SERPAPI_KEY', None)

def search_web(query):
    params = {
        "q": query,
        "hl": "ko",  # 한국어 인터페이스
        "gl": "kr",  # 한국 지역
        "api_key": SERPAPI_KEY,
        "num": 20 
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "organic_results" in results:
        return results["organic_results"]
    else:
        return results