# 🚀 YouTube Video Downloader (Cross-Platform)

## ✨ Overview

Welcome to the **YouTube Video Downloader (Cross-Platform)**!  
This project provides a simple yet powerful application for downloading YouTube videos and playlists across multiple operating systems.

Built with **Kivy/KivyMD** for a consistent UI and **PytubeFix** for reliable downloads, this app makes saving your favorite YouTube content easy and accessible.

**Note:** This app is under development.

---

## 🛠️ Current Functionality

The application currently supports the following features:

### Single Video Download

- Download individual YouTube videos with options for:
  - Audio only (`.m4a`)
  - Video only (`.mp4`, highest progressive resolution)
  - Combined audio and video (`.mp4`, merged using ffmpeg)

### Playlist Video Selection and Download

- Fetch and display videos from a YouTube playlist URL
- Show video titles and thumbnails
- Allow users to select specific videos from the playlist
- Download selected videos in highest progressive resolution

---

## 🚧 Work in Progress / Known Limitations

- **Playlist Download Options**
  - No option yet for selecting audio-only or combined video/audio for playlist items
  - All playlist videos download in default progressive `.mp4` format

---

## 🎯 Platform Goals

Future support is planned for:


- Windows

---

## ⚙️ Technologies Used

- **Kivy** – Python framework for building cross-platform apps
- **KivyMD** – Material Design widgets for Kivy
- **PytubeFix** – YouTube video downloading library
- **FFmpeg** – Used to merge video and audio streams

---

## 🚀 Getting Started 

### 1. Clone the Repository

```bash
git clone https://github.com/fused-player/Youtube-Video-Downloader-CrossPlatform.git
cd Youtube-Video-Downloader-CrossPlatform
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install kivy kivymd pytubefix ffmpeg-python plyer 
```



### 4. Prepare Directories

The app uses a `tmp` folder in the selected download location to store thumbnails.  
**Note: ** `tmp` is not a temporary dir to delete.

### 5. Run the Application

```bash
python main.py
```
---
## <img src="https://img.icons8.com/color/96/android-os.png" width="28" style="position:relative; top:4px"/> Android



- Go to [release](https://github.com/fused-player/Youtube-Video-Downloader-CrossPlatform/releases) section for download.

---
## Updates[15/06/25]
- **Linux Support** - Current Version is stable on linux and more features yet to come.
- **Android Support** – Currently stable . Added ffmpeg support.
- **Limits** - Playlist download limited to high res of progressive (not Full Quality).
- **More** - More Options are yet to come for playlist downloading.
---

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.
