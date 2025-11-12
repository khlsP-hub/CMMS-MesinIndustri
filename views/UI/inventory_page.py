# views/UI/inventory_page.py

import requests
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QLabel, QScrollArea, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QDateTime

# Impor dari file modular kita
from .config import API_INVENTORY_URL

class InventoryPage(QWidget):
    """Halaman untuk menampilkan log inventory dari API."""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("Riwayat Log Inventory")
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
        self.scroll_layout.setSpacing(8)

        self.scroll_area.setWidget(self.scroll_content_widget)
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        
        self.load_inventory()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def format_timestamp(self, timestamp_str):
        """Mengubah format timestamp ISO menjadi lebih mudah dibaca."""
        try:
            # Ubah string ISO (2025-11-12T13:34:12.441Z) ke objek datetime
            dt = QDateTime.fromString(timestamp_str, Qt.DateFormat.ISODateWithMs)
            if not dt.isValid():
                 # Coba format tanpa milidetik
                 dt = QDateTime.fromString(timestamp_str, Qt.DateFormat.ISODate)

            if dt.isValid():
                # Ubah ke zona waktu lokal dan format ulang
                return dt.toLocalTime().toString("dd MMM yyyy, hh:mm:ss")
            else:
                return timestamp_str # Kembalikan string asli jika format gagal
        except Exception:
            return timestamp_str # Kembalikan string asli jika ada error

    def load_inventory(self):
        """Mengambil data dari GET /api/InventoryLogs dan menampilkannya."""
        self.clear_layout(self.scroll_layout)
        
        API_URL = API_INVENTORY_URL
        
        try:
            response = requests.get(API_URL, timeout=5)
            if response.status_code != 200:
                raise Exception(f"Gagal memuat: Status {response.status_code}")
            
            log_list = response.json()
            
            if not log_list:
                info_label = QLabel("Tidak ada riwayat inventory untuk ditampilkan.")
                info_label.setFont(QFont("Roboto", 16))
                info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(info_label)
                return

            # Loop melalui setiap log dan tampilkan
            for log in log_list:
                item_frame = QFrame()
                item_frame.setObjectName("historyItemFrame") # Pakai style yang sama
                item_layout = QVBoxLayout(item_frame)
                
                # --- BAGIAN INI SUDAH DISESUAIKAN DENGAN FORMAT ANDA ---
                
                # 1. Format tanggal
                timestamp = self.format_timestamp(log.get('timestamp', 'N/A'))
                
                # 2. Tentukan warna & teks berdasarkan quantityChange
                quantity = log.get('quantityChange', 0)
                
                if quantity > 0:
                    header_color = "color: #006400;" # Hijau tua
                    tx_text = f"MASUK (+{quantity})"
                else: # quantity adalah 0 atau negatif
                    header_color = "color: #8B0000;" # Merah tua
                    tx_text = f"KELUAR ({quantity})" # quantity sudah negatif (misal -25)
                
                # Dapatkan Tipe Transaksi
                tx_type = log.get('transactionType', 'N/A')

                header_text = f"{timestamp} — {tx_text} (Tipe: {tx_type})"
                header_label = QLabel(header_text)
                header_font = QFont("Roboto", 14) 
                header_font.setBold(True)
                header_label.setFont(header_font)
                header_label.setStyleSheet(header_color)
                
                # 3. Buat teks detail
                detail_text = (
                    f"ID Item: {log.get('iD_Items', 'N/A')} "
                    f"(Oleh: {log.get('iD_Karyawan', 'N/A')})"
                )
                detail_label = QLabel(detail_text)
                detail_label.setFont(QFont("Roboto", 12)) 
                detail_label.setWordWrap(True)
                
                # 4. Tambahkan referensi jika ada
                ref_doc = log.get('referenceDoc')
                
                # ----------------------------------------------------

                item_layout.addWidget(header_label)
                item_layout.addWidget(detail_label)
                
                if ref_doc:
                    ref_label = QLabel(f"Referensi: {ref_doc}")
                    ref_label.setFont(QFont("Roboto", 10, italic=True))
                    ref_label.setStyleSheet("color: #555;")
                    item_layout.addWidget(ref_label)
                
                self.scroll_layout.addWidget(item_frame)

        except requests.exceptions.ConnectionError as e:
            self.show_error(f"Error Koneksi: {e}\n\nPastikan backend .NET Anda berjalan.")
        except requests.exceptions.Timeout:
            self.show_error("Error: Permintaan timeout.")
        except requests.exceptions.JSONDecodeError:
            self.show_error("Error: Gagal memproses data JSON dari API.")
        except Exception as e:
            self.show_error(f"Terjadi error saat memuat data: {e}")

    def show_error(self, message):
        self.clear_layout(self.scroll_layout)
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red;")
        error_label.setFont(QFont("Roboto", 14))
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(error_label)