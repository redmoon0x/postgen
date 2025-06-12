import json
import traceback
from kannada_content_generator import KannadaContentGenerator
from youtube_transcript import YouTubeTranscriptFetcher

def print_formatted_json(data: dict):
    """Print dictionary in a formatted, readable way"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    # Sample YouTube video URLs to test with
    video_urls = [
        "https://youtu.be/0uhossX4UXs?si=-GvejL3WKgCvU7h0",  # Replace with any YouTube video URL
    ]
    
    generator = KannadaContentGenerator()
    
    for video_url in video_urls:
        print(f"\nTesting with video: {video_url}\n")
        print("=" * 80)
        
        try:
            # First test just transcript fetching
            print("\n📝 FETCHING TRANSCRIPT:")
            print("-" * 40)
            fetcher = YouTubeTranscriptFetcher()
            transcript_data = fetcher.get_transcript(video_url)
            print("Transcript response:", transcript_data)
            print("\n")

            if transcript_data.get('transcript'):
                # Generate and display blog post
                print("🌟 BLOG POST:")
                print("-" * 40)
                blog_post = generator.generate_blog_post(video_url)
                print_formatted_json(blog_post)
            else:
                print("❌ No transcript available in the response")
            
            # Generate and display Instagram post
            print("\n📸 INSTAGRAM POST:")
            print("-" * 40)
            insta_post = generator.generate_instagram_post(video_url)
            print_formatted_json(insta_post)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("\nDetailed error traceback:")
            traceback.print_exc()
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
