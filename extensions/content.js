// Wait for the page to load
window.addEventListener('load', function() {
    // Create and style a persistent button
    const button = document.createElement('button');
    button.textContent = 'SAVE LO-FI';
    button.style.position = 'fixed';
    button.style.top = '50px';
    button.style.right = '10px';
    button.style.zIndex = '9900';
    button.style.padding = '10px 20px';              // Wider and chunkier for retro feel
    button.style.backgroundColor = '#FF69B4';       // Bright pink (retro pink)
    button.style.color = '#000000';                 // Black text for contrast
    button.style.border = '4px solid #4B0082';      // Thick dark purple border
    button.style.borderRadius = '0';                // Sharp corners, no rounding
    button.style.fontFamily = '"Courier New", monospace'; // Pixel-like monospaced font
    button.style.fontSize = '16px';                 // Larger, blocky text
    button.style.fontWeight = 'bold';               // Bold for pixel art effect
    button.style.textTransform = 'uppercase';       // All caps for retro vibe
    button.style.letterSpacing = '1px';             // Slight spacing for pixelated look
    button.style.lineHeight = '16px';               // Match font size for blocky stack
    button.style.textShadow = '0px 1px 0px #FFFFFF, 1px 0px 0px #FFFFFF'; // Pixel highlights for jagged look
    button.style.boxShadow = '2px 2px 0px #FFFFFF, 4px 4px 0px #4B0082'; // White highlight + purple shadow
    button.style.cursor = 'pointer';

    // Hover effect for interactivity (shift to a lighter pink)
    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#FF8DA1';   // Lighter pink for hover
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#FF69B4';   // Back to bright pink
    });
    document.body.appendChild(button);

    // Add click event listener
    button.addEventListener('click', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const videoId = urlParams.get('v');
        const videoElement = document.querySelector('.video-stream.html5-main-video');

        if (videoId && videoElement) {
            const currentTime = videoElement.currentTime;

            const url = `http://localhost:8080/lofiBackend?videoId=${videoId}&timestamp=${currentTime}`;

            fetch(url)
                .then(response => response.text())
                .then(data => {
                    console.log('Backend response:', data);
                    alert('Data sent successfully: ' + data);
                })
                .catch(error => {
                    console.error('Error sending data to backend:', error);
                    alert('Failed to send data to backend.');
                });
        } else {
            console.error('Video ID or video element not found.');
            alert('Please ensure you are on a YouTube video page.');
        }
    });
});