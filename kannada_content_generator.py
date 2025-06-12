import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript import YouTubeTranscriptFetcher

# Load environment variables
load_dotenv()

class KannadaContentGenerator:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        )
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.transcript_fetcher = YouTubeTranscriptFetcher()
        self.transcript_cache = {}  # Cache for storing transcripts
        
        self.system_prompt = """
You are a professional Kannada writer and content creator with expertise in creating engaging blog posts 
and social media content. Your task is to take an English transcript and transform it into:
1. A well-structured blog post in Kannada that maintains the original message while adapting it 
   to resonate with Kannada-speaking audiences
2. A concise, engaging Instagram post in Kannada that captures the key points while maintaining 
   the cultural nuances of the Kannada language

Guidelines:
- Maintain professional Kannada writing standards
- Adapt content to be culturally relevant to Kannada audiences
- For blog posts: Create proper structure with headings, paragraphs, and conclusions
- For Instagram: Keep it concise, engaging, and use appropriate hashtags in Kannada
- Preserve the core message while making it feel native to Kannada readers
"""

    def _get_transcript(self, video_url: str) -> str:
        """Helper method to get or retrieve transcript from cache"""
        if video_url not in self.transcript_cache:
            transcript_data = self.transcript_fetcher.get_transcript(video_url)
            transcript = transcript_data.get('transcript', '')
            if not transcript:
                raise ValueError("No transcript content available")
            self.transcript_cache[video_url] = transcript
        return self.transcript_cache[video_url]

    def generate_blog_post(self, video_url: str) -> Dict[str, str]:
        """
        Generate a Kannada blog post from a YouTube video transcript
        
        Args:
            video_url (str): YouTube video URL
            
        Returns:
            dict: Contains the blog post content and metadata
        """
        try:
            # Get transcript from cache or fetch new
            transcript = self._get_transcript(video_url)

            # Generate blog post using OpenAI
            prompt = f"""
            {self.system_prompt}
            
            Please create a Kannada blog post from the following English transcript:
            
            {transcript}
            
            Format the response as JSON with the following structure:
            {{
                "title": "Kannada title here",
                "content": "Full blog post content in Kannada",
                "tags": ["tag1", "tag2", "tag3"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            blog_data = json.loads(result)  # Safely parse JSON
            blog_data["original_transcript"] = transcript
            
            return blog_data

        except Exception as e:
            raise Exception(f"Failed to generate blog post: {str(e)}")

    def generate_instagram_post(self, video_url: str) -> Dict[str, str]:
        """
        Generate a Kannada Instagram post from a YouTube video transcript
        
        Args:
            video_url (str): YouTube video URL
            
        Returns:
            dict: Contains the Instagram post content and metadata
        """
        try:
            # Get transcript from cache or fetch new
            transcript = self._get_transcript(video_url)

            # Generate Instagram post using OpenAI
            prompt = f"""
            {self.system_prompt}
            
            Please create a Kannada Instagram post from the following English transcript:
            
            {transcript}
            
            Format the response as JSON with the following structure:
            {{
                "caption": "Instagram caption in Kannada",
                "hashtags": ["hashtag1", "hashtag2"],
                "suggested_image_prompt": "Description for image generation"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            insta_data = json.loads(result)  # Safely parse JSON
            insta_data["original_transcript"] = transcript
            
            return insta_data

        except Exception as e:
            raise Exception(f"Failed to generate Instagram post: {str(e)}")

def main():
    # Example usage
    generator = KannadaContentGenerator()
    
    try:
        video_url = "https://youtu.be/0uhossX4UXs?si=-GvejL3WKgCvU7h0"
        
        # Generate blog post
        blog_post = generator.generate_blog_post(video_url)
        print("\nBlog Post:")
        print(f"Title: {blog_post['title']}")
        print(f"Content: {blog_post['content']}")
        print(f"Tags: {', '.join(blog_post['tags'])}")
        
        # Generate Instagram post
        insta_post = generator.generate_instagram_post(video_url)
        print("\nInstagram Post:")
        print(f"Caption: {insta_post['caption']}")
        print(f"Hashtags: {' '.join(insta_post['hashtags'])}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
