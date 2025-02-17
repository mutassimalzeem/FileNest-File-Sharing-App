# File Sharing App

A simple yet powerful desktop application for easy local file sharing using QR codes. Built with Python and Tkinter.

![File Sharing App Screenshot](screenshots/app_screenshot.png) <!-- Add your screenshot file when available -->

## Features

- **Drag and Drop Interface**: Simply drag files into the application for quick sharing
- **QR Code Generation**: Share files instantly by scanning a QR code
- **File Preview**: Preview images and text files before sharing
- **Theme Options**: Switch between light and dark modes
- **Folder Organization**: Group shared files into folders
- **User Preference Saving**: Remembers your theme preference

## How It Works

1. Drag files into the application or use the browse button
2. Click "Start Sharing" to initiate the local HTTP server
3. A QR code will be generated and displayed
4. Other devices on the same network can scan the QR code to access the shared files

## Requirements

- Python 3.6+
- Tkinter
- tkinterdnd2
- PIL/Pillow
- pyqrcode
- png

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/file-sharing-app.git
   cd file-sharing-app
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Usage

### Sharing Files
1. Start the application
2. Drag files onto the "Drop Files Here" area or click "Browse Files"
3. Click "Start Sharing"
4. A QR code will appear that others can scan to access your files

### Organizing Files
- Enter a folder name in the text field and click "Create" to organize shared files into a folder

### Changing Theme
- Click "Toggle Theme" to switch between light and dark modes

## Security Notes

This application creates a simple HTTP server on your local network. Keep in mind:
- Files are shared without authentication
- Anyone on your network can access the shared files
- Use only on trusted networks for non-sensitive files

## Technical Details

The application uses:
- Tkinter with tkinterdnd2 for the drag and drop interface
- Python's built-in HTTP server for file sharing
- Socket programming to get the local IP address
- Threading to keep the UI responsive while the server runs
- PIL for image preview functionality
- pyqrcode for QR code generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)

## Future Enhancements

- Password protection for shared files
- Ability to manage which files are being shared
- File transfer progress indication
- Cross-platform functionality testing
- Mobile companion app
