from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor
from PySide6.QtCore import Qt
import os
import sys
from pathlib import Path


def set_circular_pixmap(label, image_path):
    if not image_path:
        label.setPixmap(QPixmap())
        return

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        label.setPixmap(QPixmap())
        return

    scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    mask = QPixmap(scaled_pixmap.size())
    mask.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(Qt.GlobalColor.white))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
    painter.end()
    
    scaled_pixmap.setMask(mask.createMaskFromColor(Qt.GlobalColor.transparent))
    label.setPixmap(scaled_pixmap)

def format_speed(speed):
    if speed > 1000000:
        return f"{speed / 1000000:.2f} MB/s"
    elif speed > 1000:
        return f"{speed / 1000:.2f} KB/s"
    else:
        return f"{speed} B/s"

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{int(h)}h {int(m)}m {int(s)}s"
    elif m:
        return f"{int(m)}m {int(s)}s"
    else:
        return f"{int(s)}s"

def get_data_dir():
    """
    Get the application data directory path.
    On Windows: %APPDATA%/TubeTokDownloader
    On Linux: ~/.local/share/TubeTokDownloader
    On macOS: ~/Library/Application Support/TubeTokDownloader
    """
    if sys.platform.startswith("win"):
        base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
    elif sys.platform.startswith("darwin"):
        base_dir = os.path.expanduser('~/Library/Application Support')
    else:  
        base_dir = os.path.expanduser('~/.local/share')
    
    data_dir = os.path.join(base_dir, 'TubeTokDownloader')
    os.makedirs(data_dir, exist_ok=True)

   
    images_dir = os.path.join(data_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    return data_dir

def get_images_dir():
    
    return os.path.join(get_data_dir(), 'images')

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    Args:
        relative_path: Path relative to project root (e.g., 'assets/test.png')
    
    Returns:
        Absolute path to the resource
    """
    try:
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise AttributeError
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)