document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const videoUrlInput = document.getElementById('videoUrl');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    const blogTitle = document.getElementById('blogTitle');
    const blogContent = document.getElementById('blogContent');
    const blogTags = document.getElementById('blogTags');
    const instaCaption = document.getElementById('instaCaption');
    const instaHashtags = document.getElementById('instaHashtags');

    function showLoading(show) {
        loadingDiv.classList.toggle('hidden', !show);
        generateBtn.disabled = show;
        generateBtn.classList.toggle('opacity-50', show);
    }

    function displayResults(data) {
        // Blog Post
        blogTitle.textContent = data.blog_post.title;
        blogContent.innerHTML = data.blog_post.content.replace(/\n/g, '<br>');
        blogTags.innerHTML = data.blog_post.tags
            .map(tag => `<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">${tag}</span>`)
            .join('');

        // Instagram Post
        instaCaption.textContent = data.instagram_post.caption;
        instaHashtags.innerHTML = data.instagram_post.hashtags
            .map(tag => `<span class="px-3 py-1 bg-pink-100 text-pink-800 rounded-full text-sm">${tag}</span>`)
            .join('');

        resultsDiv.classList.remove('hidden');
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }

    generateBtn.addEventListener('click', async function() {
        const videoUrl = videoUrlInput.value.trim();
        
        if (!videoUrl) {
            alert('Please enter a YouTube video URL');
            return;
        }

        showLoading(true);
        resultsDiv.classList.add('hidden');

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ video_url: videoUrl })
            });

            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                alert(data.error || 'An error occurred while generating content');
            }
        } catch (error) {
            alert('An error occurred while communicating with the server');
            console.error('Error:', error);
        } finally {
            showLoading(false);
        }
    });

    // Add keypress event listener for Enter key
    videoUrlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generateBtn.click();
        }
    });
});
