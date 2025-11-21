# YT2Podcast 🎙️

Convert any YouTube channel into a podcast feed you can subscribe to in your favorite podcast app.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 About

YT2Podcast is a Flask-based service that generates RSS podcast feeds from YouTube channels. It allows you to listen to your favorite YouTube content in any podcast player that supports custom RSS feeds, with automatic audio extraction and caching.

## ✨ Features

- **Channel to Podcast**: Convert any YouTube channel to an RSS podcast feed.
- **Audio Extraction**: Automatically extracts audio from YouTube videos using yt-dlp and **streams it**.
- **Smart Caching**: Caches audio URLs to minimize API calls and improve performance.
- **Duration Filtering**: Filter channel videos by minimum/maximum duration.

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher.
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials)).[web:3]

### Setup with Docker Compose (Recommended)

The easiest way to run YT2Podcast is using Docker Compose, which handles dependencies and configuration automatically.

1. **Clone the repository**:
   ```
   git clone https://github.com/n0vella/yt2podcast.git
   cd yt2podcast
   ```

2. **Create `.secrets.toml`** in the project root:
   ```
   [youtube]
   api_key = "YOUR_YOUTUBE_API_KEY_HERE"
   
   # Optional: Logging tweaks
   [logging]
   log_file = "app.log"
   format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
   datefmt = "%Y-%m-%d %H:%M:%S"

   [logging.levels]
   root = "INFO"
   werkzeug = "WARNING"
   yt_api = "WARNING"
   ```

3. **Start with Docker Compose**:
   ```
   docker-compose up --build
   ```
   This builds and runs the Flask app on `http://localhost:5000`. Ensure Docker and Docker Compose are installed.

   Example `docker-compose.yml` (add to project root if not present):
   ```
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       env_file:
         - .secrets.toml
       volumes:
         - .:/app
   ```
   - Builds from a `Dockerfile` (create one if needed: `FROM python:3.10`, install requirements, expose 5000, CMD `flask --app yt2podcast.main run --host=0.0.0.0`).[web:6][web:12][web:15]

### Manual Setup (Alternative)

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Configure** as above with `.secrets.toml`.

3. **Start the server**:
   ```
   flask --app yt2podcast.main run --host=0.0.0.0
   ```

## 📖 Usage

Subscribe to channels using the URL format: `http(s)://<your-server>/feed/@YourFavouriteChannel`.

Additional query parameters:
- `min_duration`: Minimum video duration in seconds (e.g., `?min_duration=600` for 10 minutes).
- `max_duration`: Maximum video duration in seconds (e.g., `?max_duration=3600` for 1 hour).

Example: `http://localhost:5000/feed/@veritasium?min_duration=300` generates a filtered RSS feed.

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

**Features:**
- Supports HTTP range requests (seeking).
- Automatic URL caching with expiration.
- Chunked transfer for full downloads.

## ⚙️ How It Works

1. **Feed Request**: Client requests `/feed/@channelname`.
2. **Channel Lookup**: Server resolves channel handle to channel ID using YouTube API.
3. **Video Fetching**: Retrieves all videos from the channel's uploads playlist.
4. **Duration Extraction**: Fetches video durations and applies filters.
5. **Feed Generation**: Creates iTunes-compatible RSS XML feed.
6. **Storage**: Saves feed to local JSON for incremental updates.
7. **Audio Streaming**: When a podcast player requests audio, yt-dlp extracts the direct audio URL and streams it.[web:3]