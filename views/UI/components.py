# views/UI/components.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame,
    QDialog
)
from PySide6.QtGui import QFont, QPixmap, QCursor
from PySide6.QtCore import Qt, Signal

class ComponentDialog(QDialog):
    """Jendela dialog (pop-up) untuk menampilkan DAFTAR komponen."""
    def __init__(self, nama_mesin, list_komponen, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(f"Komponen - {nama_mesin}")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #FFFFFF;")

        layout = QVBoxLayout(self)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(scroll_content)

        if not list_komponen:
            label_komponen = QLabel("Tidak ada komponen terdaftar untuk mesin ini.")
            label_komponen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scroll_layout.addWidget(label_komponen)
        else:
            for comp in list_komponen:
                comp_name = comp.get("componentName", "Nama Komponen Tdk Ada")
                
                label_komponen = QLabel(comp_name)
                label_komponen.setFont(QFont("Roboto", 12))
                label_komponen.setStyleSheet(
                    "padding: 8px; background-color: #F0F0F0; border-radius: 4px; margin-bottom: 5px;"
                )
                scroll_layout.addWidget(label_komponen)

        layout.addWidget(scroll_area)
        
        tombol_tutup = QPushButton("Tutup")
        tombol_tutup.setFont(QFont("Roboto", 10))
        tombol_tutup.setMinimumHeight(30)
        tombol_tutup.clicked.connect(self.accept) 
        layout.addWidget(tombol_tutup)


class ImageCard(QFrame):
    """Widget kustom HANYA UNTUK GAMBAR mesin di dashboard."""
    clicked = Signal(str) 

    def __init__(self, machine_id, gbr_mesin):
        super().__init__()
        
        self.machine_id = machine_id
        
        self.setObjectName("imageCard")
        self.setFixedSize(250, 250)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        label_gambar = QLabel()
        pixmap_mesin = QPixmap(gbr_mesin)
        if pixmap_mesin.isNull():
            label_gambar.setText(f"Gagal muat:\n{gbr_mesin}")
            label_gambar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_gambar.setWordWrap(True)
            label_gambar.setFixedSize(230, 230)
            label_gambar.setStyleSheet("background-color: #EEE; border: 1px dashed #CCC;")
        else:
            scaled_pixmap = pixmap_mesin.scaled(230, 230, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label_gambar.setPixmap(scaled_pixmap)
            label_gambar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_gambar)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.machine_id)


class TextCard(QFrame):
    """Widget kustom HANYA UNTUK TEKS mesin di dashboard."""
    clicked = Signal(str)

    def __init__(self, machine_id, nama_mesin, health, exhaust, last_maintenance):
        super().__init__()
        
        self.machine_id = machine_id
        
        self.setObjectName("textCard") 
        self.setFixedSize(250, 200)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        label_nama = QLabel(nama_mesin)
        font_judul = QFont("Roboto", 14) 
        font_judul.setBold(True)
        label_nama.setFont(font_judul)
        label_nama.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_nama.setStyleSheet("margin-bottom: 10px; color: #333; background-color: transparent;")
        label_nama.setWordWrap(True)
        layout.addWidget(label_nama)
        
        info_frame = QWidget()
        info_frame.setStyleSheet("background-color: transparent;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(5, 10, 5, 5)
        info_layout.setSpacing(8)
        
        info_layout.addWidget(self.buat_info_label("Health:", health))
        info_layout.addWidget(self.buat_info_label("Exhaust:", exhaust))
        info_layout.addWidget(self.buat_info_label("Last Maintenance:", last_maintenance))
        
        layout.addWidget(info_frame)
        layout.addStretch() 
    
    def buat_info_label(self, key, value):
        widget = QWidget()
        widget.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        key_label = QLabel(key)
        key_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
        key_label.setStyleSheet("color: #555; background-color: transparent;")
        value_label = QLabel(value)
        value_label.setFont(QFont("Roboto", 10))
        value_label.setStyleSheet("color: #222; background-color: transparent;")
        value_label.setWordWrap(True)
        layout.addWidget(key_label)
        layout.addStretch()
        layout.addWidget(value_label)
        return widget

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.machine_id)