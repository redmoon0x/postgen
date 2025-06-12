import requests
import re
import os
import json
from typing import Optional
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeTranscriptFetcher:
    def __init__(self):
        self.api_url = os.getenv('KOME_API_BASE_URL', 'https://kome.ai/api/transcript')
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,kn-IN;q=0.8,kn;q=0.7,hi;q=0.6,ckb;q=0.5",
            "content-type": "application/json",
            "cookie": "_ga=GA1.1.883560573.1749709747; _ga_J58R10RFE6=GS2.1.s1749709747$o1$g0$t1749709755$j52$l0$h0",
            "origin": "https://kome.ai",
            "referer": "https://kome.ai/tools/youtube-transcript-generator",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }

    def _extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from various forms of YouTube URLs
        """
        if not url:
            return None
            
        # Handle youtu.be URLs
        if "youtu.be" in url:
            path = urlparse(url).path
            return path.strip("/")
            
        # Handle youtube.com URLs
        if "youtube.com" in url:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            if "v" in query_params:
                return query_params["v"][0]
                
        # If URL is already a video ID
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
            return url
            
        return None

    def get_transcript(self, video_url: str) -> dict:
        """
        Fetch transcript for a YouTube video
        
        Args:
            video_url (str): YouTube video URL or video ID
            
        Returns:
            dict: Response containing transcript
            
        Raises:
            ValueError: If video URL is invalid
            requests.RequestException: If API request fails
        """
        video_id = self._extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL or video ID")

        # Format payload exactly as shown in the original request
        payload = {
            "video_id": f"https://youtu.be/{video_id}",
            "format": "true"  # Using string "true" instead of boolean True
        }
        print("\nDebug Info:")
        print("URL:", self.api_url)
        print("Headers:", json.dumps(self.headers, indent=2))
        print("Payload:", json.dumps(payload, indent=2))

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")

def main():
    # Example usage
    fetcher = YouTubeTranscriptFetcher()
    
    try:
        # Example video URL
        video_url = "https://youtu.be/0uhossX4UXs?si=-GvejL3WKgCvU7h0"
        result = fetcher.get_transcript(video_url)
        print(f"Transcript: {result['transcript']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
