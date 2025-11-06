# views/UI/history_page.py

import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QLabel, QScrollArea, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Impor dari file modular kita
from .config import API_BASE_URL

class MaintenanceHistoryPage(QWidget):
    """Menampilkan semua riwayat task dari semua mesin."""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("Riwayat Maintenance (Semua Mesin)")
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
        
        self.load_history()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_history(self):
        """Mengambil data API, meratakannya, dan menampilkannya."""
        self.clear_layout(self.scroll_layout)
        
        API_URL = API_BASE_URL 
        
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code != 200:
                raise Exception(f"Gagal memuat: Status {response.status_code}")
            
            all_machines = response.json()
            
            flat_history_list = []
            for machine in all_machines:
                machine_name = machine.get("machine", "N/A") 
                for component in machine.get("components", []):
                    component_name = component.get("componentName", "N/A")
                    for task in component.get("maintenanceTasks", []):
                        flat_history_list.append({
                            "machine": machine_name,
                            "component": component_name,
                            "task": task.get("taskName", "N/A"),
                            "date": task.get("lastDate", "N/A"),
                            "person": task.get("personInCharge", "N/A")
                        })
            
            if not flat_history_list:
                info_label = QLabel("Tidak ada riwayat maintenance untuk ditampilkan.")
                info_label.setFont(QFont("Roboto", 16))
                info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(info_label)
                return

            for item in flat_history_list:
                item_frame = QFrame()
                item_frame.setObjectName("historyItemFrame")
                item_layout = QVBoxLayout(item_frame)
                
                header_text = f"{item['date']} — {item['machine']}"
                header_label = QLabel(header_text)
                header_font = QFont("Roboto", 16)
                header_font.setBold(True)
                header_label.setFont(header_font)
                header_label.setStyleSheet("color: #003366; background-color: transparent;")
                
                detail_text = f"Tugas: {item['task']} (Penanggung Jawab: {item['person']})"
                detail_label = QLabel(detail_text)
                detail_label.setFont(QFont("Roboto", 14))
                detail_label.setWordWrap(True)
                detail_label.setStyleSheet("background-color: transparent;")

                item_layout.addWidget(header_label)
                item_layout.addWidget(detail_label)
                
                self.scroll_layout.addWidget(item_frame)

        except requests.exceptions.ConnectionError as e:
            self.show_error(f"Error Koneksi: {e}")
        except requests.exceptions.Timeout:
            self.show_error("Error: Permintaan timeout.")
        except Exception as e:
            self.show_error(f"Terjadi error: {e}")

    def show_error(self, message):
        self.clear_layout(self.scroll_layout)
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red;")
        error_label.setFont(QFont("Roboto", 14))
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(error_label)