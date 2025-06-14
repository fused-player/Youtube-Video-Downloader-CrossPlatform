# 🚀 YouTube Video Downloader (Cross-Platform)

## ✨ Overview

Welcome to the **YouTube Video Downloader (Cross-Platform)**!  
This project provides a simple yet powerful application for downloading YouTube videos and playlists across multiple operating systems.

Built with **Kivy/KivyMD** for a consistent UI and **PytubeFix** for reliable downloads, this app makes saving your favorite YouTube content easy and accessible.

**Note:** This is a prototype under active development. Core download features are working, but the UI and certain functionalities are still being refined.

---

## 🛠️ Current Functionality (Prototype)

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

- **UI Download Indication**
  - Single video download shows basic progress, but may not be real-time
  - Playlist downloads have no visual download progress shown

- **Playlist Download Options**
  - No option yet for selecting audio-only or combined video/audio for playlist items
  - All playlist videos download in default progressive `.mp4` format

---

## 🎯 Platform Goals

Future support is planned for:

- Android
- Linux
- Windows

---

## ⚙️ Technologies Used

- **Kivy** – Python framework for building cross-platform apps
- **KivyMD** – Material Design widgets for Kivy
- **PytubeFix** – YouTube video downloading library
- **FFmpeg** – Used to merge video and audio streams

---

## 🚀 Getting Started (Linux Prototype)

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



### 4. Prepare Temporary Directory

The app uses a `tmp` folder in the selected download location to store thumbnails.  
Ensure write permissions for this directory.

### 5. Run the Application

```bash
python main.py
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a new branch  
   `git checkout -b feature/your-feature-name`
3. Make changes and commit  
   `git commit -m "Add your message"`
4. Push the branch  
   `git push origin feature/your-feature-name`
5. Open a Pull Request

Suggestions and improvements for UI, playlist options, and bug fixes are appreciated.

---

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.
