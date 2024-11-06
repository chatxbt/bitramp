import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


BASE_URL = "https://api.getpartna.com/v1/"
OFF_RAMP_BASE_URL = "https://staging-biz.coinprofile.co/v2/"
HEADERS = {
    "X-Api-User": os.getenv("PARTNA_API_USER"),
    "X-Api-Key": os.getenv("PARTNA_API_KEY"),
    "X-User-Version": "v2",
}


def make_request(method: str, endpoint: str, **kwargs):
    """Handles API requests with dynamic HTTP methods."""
    response = requests.request(method, f"{OFF_RAMP_BASE_URL}/{endpoint}", headers=HEADERS, **kwargs)
    response.raise_for_status()
    return response.json()
