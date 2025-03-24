# lofiSaver

I listen to a lot of non-lyrical stuff when working or studying. Sometimes a beat catches my attention and I want to log it for future reference. Manually going through a track list to find timestamps and titles became tedious, so I built lofiSaver—a tiny tool to help log all the cool beatz automatically.

**lofiSaver** extracts track information from YouTube videos using a Python Flask backend and a Chrome extension. The extension injects a persistent button on YouTube pages that, when clicked, captures the video ID and current playback time and sends this data to the Flask server.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Python Setup](#python-setup)
    - [Obtaining a YouTube API Key](#obtaining-a-youtube-api-key)
  - [Chrome Extension Setup](#chrome-extension-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project allows you to capture track data from YouTube videos by:
- Running a Flask server (Python) that processes track info.
- Injecting a persistent button via a Chrome extension (JavaScript) that:
  - Extracts the video ID from the URL.
  - Captures the current playback time.
  - Sends this information to the Flask server.

## Features

- **Python Backend:**  
  A Flask server that receives and processes track data (e.g., saving it to CSV, integrating with other APIs).

- **Chrome Extension:**  
  A content script (`content.js`) that injects a persistent button onto every YouTube page. Clicking the button fetches the video’s ID and current playback time, then sends the data to the backend.

## Prerequisites

- Python 3.7+
- Git
- Google Chrome (or any Chromium-based browser)
- Basic knowledge of terminal/command-line usage

## Installation

### Python Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/bainsabhi/lofiSaver.git
   cd lofiSaver

2. **Create and Activate a Virtual Environment:**

    ```bash
    Copy
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate

3. **Install Required Python Libraries:**

    ```bash
    pip install -r requirements.txt

4. **Set Up Environment Variables:**

    Create a .env file in the project root (this file is excluded from Git via .gitignore). For example:
  
    ```bash 
    API_KEY=your_youtube_api_key
    FILE_PATH=final.csv

  - Obtaining a YouTube API Key
    - To use the YouTube Data API, you need to obtain an API key:

    - Visit the Google Cloud Console:
  Go to https://console.cloud.google.com/.

    - Create or Select a Project:
  Click the project drop-down at the top and either select an existing project or create a new one.

    - Enable the YouTube Data API v3:
  Navigate to APIs & Services > Library.
  Search for YouTube Data API v3, click on it, then click Enable.

    - Create Credentials:
  Go to APIs & Services > Credentials.
  Click Create Credentials and select API key.
  Copy your generated API key.

    - Store the API Key:
  Paste your API key into your .env file as shown above. This key is used by the Flask server to make API calls to YouTube.

5. **Chrome Extension Setup**
    1. Locate the Extension Files:
      - The extension files are located in the extensions folder:

          - manifest.json
          - content.js

    2. Load the Extension in Chrome:
      - Open Chrome and navigate to chrome://extensions/.
      - Enable Developer mode (toggle in the top-right corner).
      - Click Load unpacked and select the extensions folder from the repository.
      - The extension will now be injected into every YouTube page you visit.

## Usage

1. **Start the Flask Server:**

    Ensure your virtual environment is active and run:

    ``` bash
    python main.py
    ```
    The Flask server will run on port 8080. (Make sure port 8080 is available.)

2. **Browse YouTube:**

    Open any YouTube video page in Chrome. You should see an overlay button (e.g., "Send Track Info") on the page.

3. **Capture Track Data:**

    Click the overlay button to capture:

    The data will be sent to the Flask server at http://localhost:8080/lofiBackend, which processes the track data (e.g., logging it to final.csv).

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with improvements, bug fixes, or new features. Feel free to open an issue if you have any questions.

## License
This project is licensed under the MIT License.

