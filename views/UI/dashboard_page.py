# views/UI/dashboard_page.py

import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, 
    QFrame, QGridLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Impor dari file modular kita
from .config import API_BASE_URL
from .components import ComponentDialog, ImageCard, TextCard

class DashboardPage(QWidget):
    """Halaman dashboard utama dengan kartu gambar di atas kartu teks."""
    
    API_URL = API_BASE_URL
    
    def __init__(self):
        super().__init__()
        
        self.data_mesin_statis = [
            {"nama": "MesiN Bor Meja A-01",    "machine_id": "4", "gbr_mesin": "images/MesiN Bor Meja.jpg",   "health": "95%", "exhaust": "Optimal", "last_maintenance": "01 Nov 2025"},
            {"nama": "Mesin Press Brake B-02", "machine_id": "2", "gbr_mesin": "images/Mesin Press Brake.jpg", "health": "75%", "exhaust": "Perlu Cek", "last_maintenance": "15 Okt 2025"},
            {"nama": "Laser Cutter C-03",      "machine_id": "1", "gbr_mesin": "images/mesin-Laser Cutter.jpeg", "health": "98%", "exhaust": "Optimal", "last_maintenance": "03 Nov 2025"},
            {"nama": "Mesin Bubut D-04",       "machine_id": "3", "gbr_mesin": "images/mesin-bubut.jpg",      "health": "40% (Warning)", "exhaust": "Buruk", "last_maintenance": "01 Sep 2025"},
        ]

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Dashboard Monitoring Mesin")
        title_font = QFont("Roboto", 18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("padding-bottom: 10px;")
        page_layout.addWidget(title_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame) 
        self.scroll_area.setObjectName("scrollArea")
        
        self.scroll_content_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setVerticalSpacing(10) 
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll_area.setWidget(self.scroll_content_widget)
        page_layout.addWidget(self.scroll_area)

        self.tampilkan_data_kartu()

    def tampilkan_data_kartu(self):
        """Membuat kartu gambar di ATAS kartu teks dari data statis."""
        
        KOLOM_PER_MESIN = 4 
        
        for i, mesin in enumerate(self.data_mesin_statis):
            
            kartu_gambar = ImageCard(
                mesin["machine_id"],
                mesin["gbr_mesin"]
            )
            
            kartu_teks = TextCard(
                mesin["machine_id"],
                mesin["nama"],
                mesin["health"],
                mesin["exhaust"],
                mesin["last_maintenance"]
            )
            
            kartu_gambar.clicked.connect(self.tampilkan_komponen_dari_api)
            kartu_teks.clicked.connect(self.tampilkan_komponen_dari_api)
            
            baris = (i // KOLOM_PER_MESIN) * 2 
            kolom = i % KOLOM_PER_MESIN
            
            self.grid_layout.addWidget(kartu_gambar, baris, kolom)
            self.grid_layout.addWidget(kartu_teks, baris + 1, kolom)

        baris_selanjutnya = (len(self.data_mesin_statis) // KOLOM_PER_MESIN + 1) * 2
        self.grid_layout.setRowStretch(baris_selanjutnya, 1)
        self.grid_layout.setColumnStretch(KOLOM_PER_MESIN, 1)

    def tampilkan_komponen_dari_api(self, machine_id):
        """Fungsi yang dipanggil saat kartu diklik."""
        
        print(f"Mengambil data untuk machine_id: {machine_id}...")
        
        try:
            response = requests.get(f"{self.API_URL}/{machine_id}", timeout=5)
            
            if response.status_code == 200:
                data_mesin = response.json()
                nama_mesin = data_mesin.get("machine", "Nama Tidak Ditemukan")
                list_komponen = data_mesin.get("components", [])
                
                dialog = ComponentDialog(nama_mesin, list_komponen, self)
                dialog.exec()
                
            else:
                error_dialog = ComponentDialog(
                    f"Error {response.status_code}", 
                    [{"componentName": f"Gagal mengambil data dari API.\n{response.text}"}], 
                    self
                )
                error_dialog.exec()

        except requests.exceptions.ConnectionError:
            error_dialog = ComponentDialog(
                "Error Koneksi", 
                [{"componentName": "Tidak dapat terhubung ke API.\nPastikan backend .NET Anda sedang berjalan."}], 
                self
            )
            error_dialog.exec()
        except Exception as e:
            error_dialog = ComponentDialog(
                "Error", 
                [{"componentName": f"Terjadi kesalahan:\n{e}"}], 
                self
            )
            error_dialog.exec()