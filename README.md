# YouTube Content Generator

A Python module that:
1. Fetches transcripts from YouTube videos using the Kome.ai API
2. Generates Kannada blog posts and Instagram content from the transcripts

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/redmoon0x/postgen.git
   cd postgen
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env   # or use your preferred editor
   ```
   Update the following variables in your .env file:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: GPT model to use (default: gpt-4)
   - `OPENAI_BASE_URL`: OpenAI API endpoint
   - `KOME_API_BASE_URL`: Kome API endpoint for transcripts

## Usage

### Command Line Interface

### Fetching Transcripts
```python
from youtube_transcript import YouTubeTranscriptFetcher

# Create an instance of the fetcher
fetcher = YouTubeTranscriptFetcher()

# Fetch transcript for a video
video_url = "https://youtu.be/your-video-id"
result = fetcher.get_transcript(video_url)
print(result['transcript'])
```

### Generating Kannada Content
```python
from kannada_content_generator import KannadaContentGenerator

# Create an instance of the generator
generator = KannadaContentGenerator()

# Generate a blog post
blog_post = generator.generate_blog_post(video_url)
print(f"Blog Title: {blog_post['title']}")
print(f"Blog Content: {blog_post['content']}")
print(f"Tags: {blog_post['tags']}")

# Generate an Instagram post
insta_post = generator.generate_instagram_post(video_url)
print(f"Caption: {insta_post['caption']}")
print(f"Hashtags: {insta_post['hashtags']}")
```

### Web Interface
1. Start the web application:
```bash
python app.py
```
2. Open your browser and navigate to `http://localhost:5000`
3. Enter a YouTube URL and click "Generate Content"
4. View the generated Kannada blog post and Instagram content

## Features

### Transcript Fetcher
- Supports various YouTube URL formats:
  - youtu.be short URLs
  - youtube.com full URLs
  - Direct video IDs
- Error handling for invalid URLs and API failures
- Clean and type-hinted code

### Kannada Content Generator
- Uses OpenAI API for professional content generation
- Generates professional Kannada blog posts from video transcripts
- Creates engaging Instagram posts in Kannada
- Maintains cultural relevance and language nuances
- Returns structured content with metadata (titles, tags, hashtags)
- Built-in system prompt for consistent content style
- Configurable OpenAI model selection through environment variables
- Modern web interface with responsive design
- Real-time content generation
- Clean and user-friendly UI with animations
- Support for Kannada font rendering

## Error Handling

The module raises exceptions in the following cases:
- `ValueError`: If the provided URL is invalid or video ID cannot be extracted
- `Exception`: If the API request fails

## Example

```python
try:
    fetcher = YouTubeTranscriptFetcher()
    result = fetcher.get_transcript("https://youtu.be/your-video-id")
    print(f"Transcript: {result['transcript']}")
except Exception as e:
    print(f"Error: {str(e)}")
