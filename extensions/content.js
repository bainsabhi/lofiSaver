function initializeButton() {
    // Remove existing button if it exists
    const existingButton = document.querySelector('#save-lo-fi-button');
    if (existingButton) existingButton.remove();

    //window.addEventListener('load', function() {
    // Create and style a persistent button
    const button = document.createElement('button');
    button.textContent = 'SAVE LO-FI';
    button.style.position = 'fixed';
    button.style.top = '50px';
    button.style.right = '10px';
    button.style.zIndex = '9900';
    button.style.padding = '10px 20px';              
    button.style.backgroundColor = '#FF69B4';       
    button.style.color = '#000000';                 
    button.style.border = '4px solid #4B0082';      
    button.style.borderRadius = '0';                
    button.style.fontFamily = '"Courier New", monospace'; 
    button.style.fontSize = '16px';                 
    button.style.fontWeight = 'bold';               
    button.style.textTransform = 'uppercase';       
    button.style.letterSpacing = '1px';             
    button.style.lineHeight = '16px';               
    button.style.textShadow = '0px 1px 0px #FFFFFF, 1px 0px 0px #FFFFFF'; 
    button.style.boxShadow = '2px 2px 0px #FFFFFF, 4px 4px 0px #4B0082'; 
    button.style.cursor = 'pointer';

    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#FF8DA1';
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#FF69B4';
    document.body.appendChild(button);

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

window.addEventListener('load', function() {
    initializeButton();
})};


let lastUrl = window.location.href;
new MutationObserver(() => {
    const currentUrl = window.location.href;
    if (currentUrl !== lastUrl && currentUrl.includes('youtube.com/watch?v=')) {
        console.log('URL changed to:', currentUrl);
        lastUrl = currentUrl;
        initializeButton();
    }
}).observe(document, { subtree: true, childList: true });