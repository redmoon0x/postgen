from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from kannada_content_generator import KannadaContentGenerator

app = Flask(__name__)
CORS(app)

generator = KannadaContentGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        video_url = data.get('video_url')
        
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # Generate both blog and Instagram content
        blog_post = generator.generate_blog_post(video_url)
        insta_post = generator.generate_instagram_post(video_url)

        return jsonify({
            'blog_post': blog_post,
            'instagram_post': insta_post
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
