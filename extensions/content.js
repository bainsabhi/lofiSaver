function initializeButton() {
    const existingButton = document.querySelector('#save-lo-fi-button');
    if (existingButton){
        existingButton.remove();
        console.log('remnoved the existing button');
    }

    const button = document.createElement('button');
    button.textContent = 'SAVE LO-FI';
    button.id = 'save-lo-fi-button';
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

    if (document.body) {
        console.log('Appending button to page');
        document.body.appendChild(button);
    } else {
        console.error('document.body not found, retrying...');
        setTimeout(initializeButton, 1000);
    }

    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#FF8DA1';
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#FF69B4';
    });

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
}


if (document.readyState === 'complete' || document.readyState === 'interactive') {
    console.log('Document already loaded, running initializeButton immediately');
    initializeButton();
} else {
    console.log('Waiting for window.load event');
    window.addEventListener('load', function() {
        console.log('window.load event fired');
        initializeButton();
    });
}

let lastUrl = window.location.href;
new MutationObserver(() => {
    const currentUrl = window.location.href;
    if (currentUrl !== lastUrl && currentUrl.includes('youtube.com/watch?v=')) {
        console.log('URL changed to:', currentUrl);
        lastUrl = currentUrl;
        initializeButton();
    }
}).observe(document, { subtree: true, childList: true });