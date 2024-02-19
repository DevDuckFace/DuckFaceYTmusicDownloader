import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QLabel,
    QWidget,
)

# Install pytube and moviepy libraries if not already present
try:
    from pytube import YouTube
except ImportError:
    print("Please install pytube: pip install pytube")
    sys.exit()

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    print("Please install moviepy: pip install moviepy")
    sys.exit()


class DownloaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader & Converter")
        self.setFixedSize(400, 200)

        # Create layout
        self.layout = QVBoxLayout()

        # URL input field
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube video URL")
        self.layout.addWidget(self.url_input)

        # Output folder selection
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_button = QPushButton("Browse")
        self.output_folder_button.clicked.connect(self.select_output_folder)
        self.output_folder_path = QLineEdit()
        self.output_folder_path.setReadOnly(True)
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.output_folder_label)
        folder_layout.addWidget(self.output_folder_button)
        folder_layout.addWidget(self.output_folder_path)
        self.layout.addLayout(folder_layout)

        # Format selection combo box
        self.format_combo = QComboBox()
        self.format_combo.addItem("mp3")
        self.format_combo.addItem("aac")
        self.format_combo.addItem("wav")
        self.layout.addWidget(self.format_combo)

        # Download button
        self.download_button = QPushButton("Download & Convert")
        self.download_button.clicked.connect(self.download_and_convert)
        self.layout.addWidget(self.download_button)

        # Set central widget and show window
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.show()

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.output_folder_path.setText(folder_path)

    def download_and_convert(self):
        url = self.url_input.text()
        output_folder = self.output_folder_path.text()
        selected_format = self.format_combo.currentText()

        if not url or not output_folder:
            return

        try:
            # Download complete video (for potential FPS information)
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True).first()  # Try progressive stream
            video.download(output_path=output_folder)

            # Extract audio using moviepy
            filename = os.path.splitext(os.path.basename(video.default_filename))[0]
            output_file = os.path.join(output_folder, f"{filename}.{selected_format}")
            clip = VideoFileClip(os.path.join(output_folder, video.default_filename))
            clip.audio.write_audiofile(output_file)
            clip.close()

            # Delete downloaded video (optional)
            # os.remove(os.path.join(output_folder, video.default_filename))

            print(f"Download and conversion complete! File saved as: {output_file}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloaderWindow()
    sys.exit(app.exec_())
