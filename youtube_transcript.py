import requests
import re
import os
import json
import time
import random
from typing import Optional, List, Dict
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class TokenManager:
    def __init__(self):
        self.token = None
        self.token_expires_at = None
        self.retries = 5  # Increased retries
        self.retry_delay = 3  # seconds
        self._force_refresh = False
        
    def _generate_token(self) -> str:
        """Generate a new token by making a request to kome.ai"""
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        try:
            # This is a mock token generation - in reality you'd make a request to get a real token
            # The actual token generation endpoint would be provided by kome.ai
            self.token = f"kome_token_{int(time.time())}"
            self.token_expires_at = datetime.now() + timedelta(hours=1)
            return self.token
        except Exception as e:
            raise Exception(f"Failed to generate token: {str(e)}")

    def get_valid_token(self, force_refresh=False) -> str:
        """
        Get a valid token, generating a new one if necessary
        
        Args:
            force_refresh (bool): Force token refresh even if current token is valid
        """
        if force_refresh or not self.token or not self.token_expires_at or datetime.now() >= self.token_expires_at:
            self._force_refresh = False  # Reset force refresh flag
            for attempt in range(self.retries):
                try:
                    return self._generate_token()
                except Exception as e:
                    if attempt == self.retries - 1:
                        raise
                    time.sleep(self.retry_delay * (attempt + 1))
        return self.token
    
    def force_refresh(self):
        """Mark token for forced refresh on next get_valid_token call"""
        self._force_refresh = True

class UserAgentManager:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36"
        ]
        
    def get_random_user_agent(self) -> str:
        """Get a random user agent from the list"""
        return random.choice(self.user_agents)

class YouTubeTranscriptFetcher:
    def __init__(self):
        self.api_url = os.getenv('KOME_API_BASE_URL', 'https://kome.ai/api/transcript')
        self.token_manager = TokenManager()
        self.user_agent_manager = UserAgentManager()
        self.max_retries = 5  # Increased max retries
        self.base_delay = 3  # seconds
        self.rate_limit_delay = 30  # seconds

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
        Fetch transcript for a YouTube video with retry logic and rate limit handling
        
        Args:
            video_url (str): YouTube video URL or video ID
            
        Returns:
            Union[dict, list]: Response containing transcript data
            
        Raises:
            ValueError: If video URL is invalid
            requests.RequestException: If API request fails after all retries
        """
        """
        Fetch transcript for a YouTube video with retry logic and rate limit handling
        
        Args:
            video_url (str): YouTube video URL or video ID
            
        Returns:
            dict: Response containing transcript
            
        Raises:
            ValueError: If video URL is invalid
            requests.RequestException: If API request fails after all retries
        """
        video_id = self._extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL or video ID")

        payload = {
            "video_id": f"https://youtu.be/{video_id}",
            "format": "true"
        }

        for attempt in range(self.max_retries):
            try:
                # Get fresh token and random user agent for each attempt
                force_refresh = attempt > 0  # Force token refresh after first attempt
                token = self.token_manager.get_valid_token(force_refresh)
                user_agent = self.user_agent_manager.get_random_user_agent()
                
                headers = {
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/json",
                    "origin": "https://kome.ai",
                    "referer": "https://kome.ai/tools/youtube-transcript-generator",
                    "user-agent": user_agent,
                    "authorization": f"Bearer {token}"
                }

                print(f"\nAttempt {attempt + 1} Debug Info:")
                print("URL:", self.api_url)
                print("User-Agent:", user_agent)
                print("Payload:", json.dumps(payload, indent=2))

                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                # Handle rate limiting and server errors
                if response.status_code == 429:
                    print(f"Rate limited. Waiting {self.rate_limit_delay} seconds...")
                    time.sleep(self.rate_limit_delay)
                    continue
                elif response.status_code == 500:
                    print("Server error. Forcing token refresh and retrying...")
                    self.token_manager.force_refresh()
                    delay = self.base_delay * (attempt + 1)
                    time.sleep(delay)
                    continue
                    
                response.raise_for_status()
                data = response.json()
                if not data:
                    raise ValueError("Empty response received from server")
                return data
                
            except (requests.RequestException, json.JSONDecodeError) as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to fetch transcript after {self.max_retries} attempts: {str(e)}")
                    
                delay = self.base_delay * (attempt + 1)
                print(f"Request failed: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue

def main():
    # Example usage
    fetcher = YouTubeTranscriptFetcher()
    
    try:
        # Example video URL
        video_url = "https://youtu.be/0uhossX4UXs?si=-GvejL3WKgCvU7h0"
        result = fetcher.get_transcript(video_url)
        
        if not result:
            print("Error: Empty response received")
            return
            
        try:
            # Print the full response structure first time to inspect it
            print("Full API Response:", json.dumps(result, indent=2))
            
            transcript_text = []
            
            # Handle response based on its structure
            if isinstance(result, dict):
                # If result is a dictionary, try to find transcript data
                if result.get('data') and isinstance(result['data'], list):
                    # Handle case where transcript is in data array
                    for item in result['data']:
                        if isinstance(item, dict) and item.get('text'):
                            transcript_text.append(item['text'])
                elif result.get('transcript'):
                    # Handle case where transcript is direct key
                    if isinstance(result['transcript'], str):
                        transcript_text.append(result['transcript'])
                    elif isinstance(result['transcript'], list):
                        for item in result['transcript']:
                            if isinstance(item, dict) and item.get('text'):
                                transcript_text.append(item['text'])
                            elif isinstance(item, str):
                                transcript_text.append(item)
            elif isinstance(result, list):
                # If result is a list, assume it's transcript segments
                for item in result:
                    if isinstance(item, dict) and item.get('text'):
                        transcript_text.append(item['text'])
                    elif isinstance(item, str):
                        transcript_text.append(item)
                        
            if transcript_text:
                print("\nTranscript:")
                for line in transcript_text:
                    print(line)
            else:
                print("\nNo transcript found in response. Raw response:", result)
                
        except Exception as e:
            print(f"Error processing response: {str(e)}")
            print("Raw response:", result)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
