document.addEventListener('DOMContentLoaded', function() {
    // Element references
    const generateBtn = document.getElementById('generateBtn');
    const videoUrlInput = document.getElementById('videoUrl');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const urlStatus = document.getElementById('urlStatus');
    const urlError = document.getElementById('urlError');
    const loadingStage = document.getElementById('loadingStage');
    const progressBar = document.getElementById('progressBar');
    
    const blogTitle = document.getElementById('blogTitle');
    const blogContent = document.getElementById('blogContent');
    const blogTags = document.getElementById('blogTags');
    const instaCaption = document.getElementById('instaCaption');
    const instaHashtags = document.getElementById('instaHashtags');

    // Loading stages configuration
    const loadingStages = [
        'Fetching video transcript...',
        'Analyzing content...',
        'Generating blog post...',
        'Creating Instagram content...',
        'Finalizing results...'
    ];
    let currentStage = 0;

    // URL validation
    function validateYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})(&.*)?$/;
        return pattern.test(url);
    }

    // Loading state management
    function showLoading(show) {
        loadingDiv.classList.toggle('hidden', !show);
        generateBtn.disabled = show;
        generateBtn.classList.toggle('opacity-50', show);
        
        if (show) {
            currentStage = 0;
            updateLoadingStage();
            startProgressAnimation();
        } else {
            progressBar.style.width = '0%';
        }
    }

    function updateLoadingStage() {
        if (currentStage < loadingStages.length) {
            loadingStage.textContent = loadingStages[currentStage];
            currentStage++;
            setTimeout(updateLoadingStage, 2000);
        }
    }

    function startProgressAnimation() {
        let progress = 0;
        const interval = setInterval(() => {
            if (progress >= 90) {
                clearInterval(interval);
            } else {
                progress += 1;
                progressBar.style.width = `${progress}%`;
            }
        }, 100);
    }

    // Display results with animation
    function displayResults(data) {
        // Complete the progress bar
        progressBar.style.width = '100%';
        
        // Prepare content
        blogTitle.textContent = data.blog_post.title;
        blogContent.innerHTML = data.blog_post.content.replace(/\n/g, '<br>');
        blogTags.innerHTML = data.blog_post.tags
            .map(tag => `<span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm transform transition-transform hover:scale-105">${tag}</span>`)
            .join('');

        instaCaption.textContent = data.instagram_post.caption;
        instaHashtags.innerHTML = data.instagram_post.hashtags
            .map(tag => `<span class="px-3 py-1 bg-pink-100 text-pink-800 rounded-full text-sm transform transition-transform hover:scale-105">${tag}</span>`)
            .join('');

        // Show results with animation
        setTimeout(() => {
            resultsDiv.classList.remove('hidden');
            requestAnimationFrame(() => {
                resultsDiv.style.opacity = '1';
                resultsDiv.style.transform = 'translateY(0)';
            });
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 500);
    }

    // URL validation and status indicator
    videoUrlInput.addEventListener('input', function() {
        const url = this.value.trim();
        if (url) {
            if (validateYouTubeUrl(url)) {
                urlError.classList.add('hidden');
                urlStatus.classList.remove('hidden');
                generateBtn.disabled = false;
                generateBtn.classList.remove('opacity-50');
            } else {
                urlError.classList.remove('hidden');
                urlStatus.classList.add('hidden');
                generateBtn.disabled = true;
                generateBtn.classList.add('opacity-50');
            }
        } else {
            urlError.classList.add('hidden');
            urlStatus.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.classList.remove('opacity-50');
        }
    });

    generateBtn.addEventListener('click', async function() {
        const videoUrl = videoUrlInput.value.trim();
        
        if (!videoUrl) {
            urlError.textContent = 'Please enter a YouTube video URL';
            urlError.classList.remove('hidden');
            videoUrlInput.focus();
            return;
        }

        if (!validateYouTubeUrl(videoUrl)) {
            urlError.textContent = 'Please enter a valid YouTube URL';
            urlError.classList.remove('hidden');
            videoUrlInput.focus();
            return;
        }

        showLoading(true);
        resultsDiv.classList.add('hidden');
        resultsDiv.style.opacity = '0';
        resultsDiv.style.transform = 'translateY(20px)';

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
            urlError.textContent = data.error || 'An error occurred while generating content';
            urlError.classList.remove('hidden');
            videoUrlInput.focus();
            }
        } catch (error) {
            urlError.textContent = 'An error occurred while communicating with the server. Please try again.';
            urlError.classList.remove('hidden');
            videoUrlInput.focus();
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
