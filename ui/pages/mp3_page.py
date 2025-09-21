from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QFormLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.downloader import DownloadTask
from ui.components.animated_button import AnimatedButton
from ui.components.drag_drop_line_edit import DragDropLineEdit

class AudioPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        lbl = QLabel("Download Audio")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        
        self.mp3_url = DragDropLineEdit("Paste or drag a link here...")
        layout.addWidget(self.mp3_url)
        
        hl = QHBoxLayout()
        single_btn = AnimatedButton("Download Single Audio")
        single_btn.clicked.connect(lambda: self.start_download(playlist=False))
        playlist_btn = AnimatedButton("Download Playlist Audio")
        playlist_btn.clicked.connect(lambda: self.start_download(playlist=True))
        cancel_btn = AnimatedButton("Cancel All")
        cancel_btn.clicked.connect(self.parent.cancel_active)
        
        hl.addWidget(single_btn)
        hl.addWidget(playlist_btn)
        hl.addWidget(cancel_btn)
        layout.addLayout(hl)
        
        layout.addStretch()

    def start_download(self, playlist=False):
        link = self.mp3_url.text().strip()
        if not link:
            self.parent.show_warning("Error", "No URL given.")
            return
            
        task = DownloadTask(
            link, 
            self.parent.user_profile.get_default_resolution(),
            self.parent.user_profile.get_download_path(),
            self.parent.user_profile.get_proxy(),
            audio_only=True,
            playlist=playlist,
            from_queue=False,
            audio_format=self.parent.user_profile.get_audio_format(),
            audio_quality=self.parent.user_profile.get_audio_quality()
        )
        
     
        self.parent.run_task(task, None) 