# Format File Converter

A comprehensive, cross-platform file converter that allows users to convert between various formats for audio, video, images, and documents using a modern graphical user interface (GUI). The application also supports high-DPI displays and adds an optional "Format File" right-click context menu on Windows.

## Table of Contents
- [Features](#features)
- [Supported Formats](#supported-formats)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the GUI](#running-the-gui)
  - [Windows Right-Click Context Menu](#windows-right-click-context-menu)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Multi-format Support**: Converts files between a wide range of audio, video, image, and document formats.
- **User-Friendly GUI**: Clean, modern GUI with support for dark mode and high DPI screens.
- **Windows Context Menu Integration**: Add a "Format File" option to the Windows right-click menu for quick conversions.
- **High-DPI Support**: Adjusts UI scaling for high-resolution displays.

## Supported Formats
- **Audio**: `.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac`, `.aac`, `.wma`
- **Video**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`
- **Image**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
- **Document**: `.pdf`, `.epub`, `.mobi`, `.txt`, `.doc`, `.docx`, `.rtf`

## Installation
To run this application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/format-file-converter.git
   cd format-file-converter
   ```

2. **Install Required Dependencies**: Make sure Python 3.6 or higher is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**: FFmpeg is required for audio and video conversions.
   - Download it from FFmpeg's official website.
   - Add ffmpeg to your system PATH or provide the direct path in convert_audio() and convert_video() functions if preferred.

## Usage

### Running the GUI
To use the converter, you can start the application with the following command:
```bash
python converter.py
```

This command will add the converter to the context menu of Windows Explorer.
If successful, you will see "Format File" in the context menu when you right-click on any file in Windows Explorer. Selecting this option will open the GUI with the selected file loaded.

## Requirements
- Python 3.6+
- Dependencies:
  - ffmpeg-python
  - pillow
  - pypdf
  - ebooklib
- Optional:
  - FFmpeg: Required for audio and video conversions, available at FFmpeg.org.

## Troubleshooting

### FileNotFoundError for FFmpeg
Ensure FFmpeg is installed and accessible in your system's PATH. You can verify by running:
```bash
ffmpeg -version
```

### Conversion Errors
If a conversion fails, check the format compatibility and make sure all necessary dependencies are installed. Error details will be shown in a pop-up within the application.

### High DPI Scaling Issues
The application scales automatically based on DPI. If elements look too large or too small, check the system DPI settings or try adjusting `self.scale_factor` in the code.

## Contributing
Contributions are welcome! To get started:

1. Fork the repository.
2. Create a new branch with your feature/fix: `git checkout -b feature-branch-name`
3. Commit your changes: `git commit -m 'Add a feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request.

## License
This project is licensed under the MIT License.