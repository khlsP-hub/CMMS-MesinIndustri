# views/UI/asset_page.py

import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QLabel, QScrollArea, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Impor dari file modular kita
from .config import API_BASE_URL
# (Kita bisa impor ComponentDialog jika ingin mengaktifkan klik)
# from .components import ComponentDialog

class AssetMonitoringPage(QWidget):
    """Menampilkan daftar semua mesin dari API."""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Daftar Mesin")
        title_font = QFont("Roboto", 18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("padding-bottom: 10px;")
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scrollArea")
        
        self.scroll_content_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content_widget)
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.load_machines()

    def on_machine_click(self, machine_id, machine_name):
        """Dipanggil saat tombol mesin di daftar diklik."""
        print(f"Tombol diklik! ID: {machine_id}, Nama: {machine_name}")
        # TODO: Implementasikan pop-up detail komponen di sini
        # (Logikanya sama seperti di 'tampilkan_komponen_dari_api' di dashboard_page.py)

    def clear_layout(self, layout):
        """Menghapus semua widget dari layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_machines(self):
        """Mengambil data dari GET /api/Machines dan menampilkannya."""
        self.clear_layout(self.scroll_layout)
        
        API_URL = API_BASE_URL 
        
        try:
            response = requests.get(API_URL, timeout=5) 
            
            if response.status_code == 200:
                machines_data = response.json()
                
                if not machines_data:
                    info_label = QLabel("Database terhubung.\nBelum ada data mesin untuk ditampilkan.")
                    info_label.setFont(QFont("Roboto", 16))
                    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.scroll_layout.addWidget(info_label)
                    return

                for machine in machines_data:
                    machine_id = machine.get("machineId", "NO_ID") 
                    machine_name = machine.get("machine", "Nama Tidak Ditemukan")
                    
                    machine_button = QPushButton(machine_name)
                    machine_button.setFont(QFont("Roboto", 16))
                    machine_button.setObjectName("machineButton")
                    machine_button.setStyleSheet("text-align: left; padding: 10px;")
                    
                    machine_button.clicked.connect(
                        lambda checked=False, id=machine_id, name=machine_name: self.on_machine_click(id, name)
                    )
                    self.scroll_layout.addWidget(machine_button)
                    
            else:
                self.show_error(f"Gagal memuat: Status {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            self.show_error(f"Error Koneksi:\n{e}\n\nPastikan Windows Firewall mengizinkan python.exe dan backend berjalan.")
        except requests.exceptions.Timeout:
            self.show_error("Error: Permintaan timeout.\nPastikan API server berjalan dan responsif.")
        except Exception as e:
            self.show_error(f"Terjadi error: {e}")

    def show_error(self, message):
        """Helper untuk menampilkan pesan error di frame."""
        self.clear_layout(self.scroll_layout)
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red;")
        error_label.setFont(QFont("Roboto", 14))
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(error_label)