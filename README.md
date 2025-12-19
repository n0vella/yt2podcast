# YT2Podcast 🎙️

Convert any YouTube channel into a podcast feed you can subscribe to in your favorite podcast app.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 About

YT2Podcast is a Flask-based service that generates RSS podcast feeds from YouTube channels. It allows you to listen to your favorite YouTube content in any podcast player that supports custom RSS feeds, with automatic audio extraction and caching.

**Please be polite and don't abuse this. If you think it's worth it, pay for a YouTube subscription or watch some ads to support the platform and its creators.**

## ✨ Features

- **Channel to Podcast**: Convert any YouTube channel to an RSS podcast feed.
- **Audio Extraction**: Automatically extracts audio from YouTube videos using yt-dlp and **streams it**.
- **Smart Caching**: Caches audio URLs to minimize API calls and improve performance.
- **Duration Filtering**: Filter channel videos by minimum/maximum duration.
- **Password authentication**: Token and HTTP-Basic-Auth methods supported

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher.
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials)).
	- Used to fetch channel videos and info, free for casual use like this.

### Setup with Docker Compose (Recommended)

The easiest way to run YT2Podcast is using Docker Compose, which handles dependencies and configuration automatically.

1. **Clone the repository**:
   ```
   git clone https://github.com/n0vella/yt2podcast.git
   cd yt2podcast
   ```

2. **Create `settings.toml`** in the project root (or just run it to get a copy of default_settings):

   Default settings are on [default_settings.toml]("./yt2podcast/default_settings.toml).
   At least you must configure YouTube API key on settings.toml
   It's free for this tool requirements: https://developers.google.com/youtube/v3/getting-started

   ```
   [youtube]
   api_key = "YOUR_YOUTUBE_API_KEY_HERE"
   ```

3. **Start with Docker Compose**:
   ```
   docker-compose up -d
   ```

   This builds and runs the Flask app on `http://localhost:18622`. Ensure Docker and Docker Compose are installed.

### Manual Setup (Alternative), you must have python installed

0. **(Recommended) create a virtual environment, you must have virtualenv installed**
   ```
   virtualenv venv

   # on Windows
   ./venv/Scripts/activate

   # on Linux
   source ./venv/bin/activate
   ```

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Configure** as above with `settings.toml`.

3. **Start the server**:
   ```
   python ./yt2podcast/main.py
   ```

## 📖 Usage

Subscribe to channels using the URL format: `http(s)://<your-server>/feed/@YourFavouriteChannel`.

Additional query parameters:
- `min_duration`: Minimum video duration in seconds (e.g., `?min_duration=600` for 10 minutes).
- `max_duration`: Maximum video duration in seconds (e.g., `?max_duration=3600` for 1 hour).

Example: `http://localhost:5000/feed/@veritasium?min_duration=300` generates a filtered RSS feed.

### 🔐Password prottection

If you didn't want to anyone abusing of your podcast server you can prtect it using:

   - Url token, added as "token GET parameter"
   - Password, using HTTP Basic Auth (Some clients like Antennapod supports it)
   
   Just check settings.toml to activate this:

   ```
   [auth]
   # Configure access control. Leave blank if unsure.
   # Token and password methods are mutually exclusive; configure only one.

   token = "" # Access via URL parameter: http(s)://<your_url>?token=<your_token>
   password = "" # Used for HTTP Basic Auth (required by clients like AntennaPod)

   # Set a hash_algorithm if you prefer not to store the password in plain text.
   # Supports 'md5', 'sha256', or any algorithm available in hashlib.
   # Reference: https://docs.python.org/3/library/hashlib.html
   hash_algorithm = ""
   ```


## 🔌 API Endpoints

### `GET /feed/<channel_name>`

Generates an RSS feed for the specified YouTube channel.

**Parameters:**
- `channel_name` (path): YouTube channel handle (with or without `@`) or channel ID.
- `min_duration` (query, optional): Minimum video duration in seconds.
- `max_duration` (query, optional): Maximum video duration in seconds.

**Response:** XML RSS feed.

### `GET /audio/<video_id>`

Streams audio from a YouTube video.

**Parameters:**
- `video_id` (path): YouTube video ID.

**Response:** Audio stream (typically audio/mp4).
