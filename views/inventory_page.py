# File: views/inventory_page.py
# (File BARU untuk halaman inventory)

import sys
import os
import requests 
import uuid 

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame,
    QDialog, QLineEdit, QComboBox, QFormLayout,
    QSpinBox, QMessageBox
)
from PySide6.QtGui import (
    QFont, QCursor
)
from PySide6.QtCore import (
    Qt, QDateTime
)

# Ambil URL dari file config baru
try:
    from config import API_INVENTORY_URL
except ImportError:
    # Fallback jika config.py tidak ditemukan
    API_INVENTORY_URL = "http://localhost:5042/api/InventoryLogs"


# =======================================================
# 1. DEFINISI KELAS POP-UP (Milik Halaman Inventory)
# =======================================================

class AddItemDialog(QDialog):
    """Form pop-up untuk menambah item baru atau stok ke inventory."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Tambah Item ke Inventory")
        self.setMinimumWidth(450)
        self.setStyleSheet("background-color: #90EE90; font-size: 14px;")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Tambah Stok Inventory")
        title.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        # 1. Input Form
        self.item_combo = QComboBox()
        self.item_id_new_input = QLineEdit()
        self.item_id_new_input.setPlaceholderText("Contoh: OLI-002, KBL-001")
        
        self.person_input = QLineEdit()
        self.person_input.setPlaceholderText("Contoh: Staf Gudang")
        self.qty_spinbox = QSpinBox()
        self.qty_spinbox.setRange(1, 1000) # Stok masuk
        self.ref_doc_input = QLineEdit()
        self.ref_doc_input.setPlaceholderText("Contoh: PO-12345")

        form_layout.addRow("Pilih Item:", self.item_combo)
        form_layout.addRow("Atau Item ID Baru:", self.item_id_new_input)
        form_layout.addRow("Jumlah Masuk:", self.qty_spinbox)
        form_layout.addRow("Nama Karyawan:", self.person_input)
        form_layout.addRow("Dokumen Referensi:", self.ref_doc_input)
        
        layout.addLayout(form_layout)

        # 2. Tombol Aksi
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Tambah Stok") # Tombol konfirmasi
        self.submit_button.setObjectName("scheduleButton") # Style biru
        self.cancel_button = QPushButton("Batal")
        self.cancel_button.setStyleSheet("background-color: #DDDDDD; padding: 10px; border-radius: 5px;")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        # (FIX) Tombol submit yang hilang ditambahkan ke layout
        button_layout.addWidget(self.submit_button) 
        
        layout.addLayout(button_layout)

        # Hubungkan sinyal
        self.submit_button.clicked.connect(self.submit_data)
        self.cancel_button.clicked.connect(self.reject)
        self.item_combo.currentTextChanged.connect(self.on_item_select)

        # Ambil data untuk ComboBox
        self.fetch_existing_items()

    def fetch_existing_items(self):
        """Mengambil daftar item unik dari log inventory."""
        self.item_combo.clear()
        self.item_combo.addItem("--- MASUKKAN ITEM BARU ---", None)
        
        try:
            response = requests.get(API_INVENTORY_URL, timeout=5)
            if response.status_code == 200:
                logs = response.json()
                # Dapatkan semua ID item unik
                unique_ids = sorted(list(set(log.get("iD_Items") for log in logs if log.get("iD_Items"))))
                for item_id in unique_ids:
                    self.item_combo.addItem(item_id, item_id)
        except Exception as e:
            print(f"Gagal memuat item inventory: {e}")
            # Tetap lanjut, pengguna masih bisa input manual

    def on_item_select(self, text):
        """Mengatur visibilitas input ID baru."""
        if text == "--- MASUKKAN ITEM BARU ---":
            self.item_id_new_input.show()
        else:
            self.item_id_new_input.hide()
            self.item_id_new_input.clear()

    def submit_data(self):
        """Mengirim data form ke API Backend."""
        
        # Tentukan Item ID
        item_id = ""
        if self.item_combo.currentText() == "--- MASUKKAN ITEM BARU ---":
            item_id = self.item_id_new_input.text()
        else:
            item_id = self.item_combo.currentData()
        
        person = self.person_input.text()
        quantity = self.qty_spinbox.value()
        ref_doc = self.ref_doc_input.text()

        if not item_id or not person:
            QMessageBox.warning(self, "Input Tidak Lengkap", "Item ID dan Nama Karyawan tidak boleh kosong.")
            return
        
        # (FIX) Pastikan Transaction_Type="IN" dan quantity positif
        log_payload = {
            "ID_Log": str(uuid.uuid4()), 
            "ID_Items": item_id,
            "ID_Karyawan": person,
            "Transaction_Type": "IN", # Stok masuk
            "Quantity_Change": quantity, # Kuantitas positif
            "Timestamp": QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate),
            "Reference_Doc": ref_doc
        }

        try:
            response_log = requests.post(API_INVENTORY_URL, json=log_payload, timeout=5)
            
            if response_log.status_code not in [200, 201]:
                raise Exception(f"Gagal menyimpan log. Server merespons: {response_log.text}")

            QMessageBox.information(self, "Sukses", "Stok item baru berhasil ditambahkan ke inventory.")
            self.accept() # Tutup dialog

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error Koneksi", "Tidak dapat terhubung ke server. Pastikan backend C# berjalan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan:\n{e}")

# =======================================================
# 2. DEFINISI KELAS HALAMAN INVENTORY
# =======================================================

class InventoryPage(QWidget):
    """Halaman untuk menampilkan log inventory dari API."""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # (BARU) Layout untuk Judul dan Tombol-tombol
        title_layout = QHBoxLayout()
        title_label = QLabel("Riwayat Log Inventory")
        title_font = QFont("Roboto", 18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("scheduleButton") # Style biru
        self.refresh_button.setFixedWidth(100)
        
        self.add_item_button = QPushButton("Tambah Item")
        self.add_item_button.setObjectName("completeButton") # Style hijau
        self.add_item_button.setFixedWidth(120)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.refresh_button)
        title_layout.addWidget(self.add_item_button)
        
        main_layout.addLayout(title_layout) # Tambahkan layout judul
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_content_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(8)
        self.scroll_area.setWidget(self.scroll_content_widget)
        
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        
        # Koneksi tombol
        self.refresh_button.clicked.connect(self.load_inventory)
        self.add_item_button.clicked.connect(self.open_add_item_dialog)
    
    # (BARU) Refresh otomatis saat tab diklik
    def showEvent(self, event):
        print("Menampilkan InventoryPage, memuat data...")
        self.load_inventory()
        event.accept()

    def open_add_item_dialog(self):
        """Membuka pop-up form AddItemDialog."""
        dialog = AddItemDialog(self)
        if dialog.exec():
            print("Dialog 'Tambah Item' ditutup, me-refresh daftar...")
            self.load_inventory() # Muat ulang HANYA jika dialog sukses
        else:
            print("Dialog 'Tambah Item' dibatalkan.")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

    def format_timestamp(self, timestamp_str):
        try:
            dt = QDateTime.fromString(timestamp_str, Qt.DateFormat.ISODateWithMs)
            if not dt.isValid():
                    dt = QDateTime.fromString(timestamp_str, Qt.DateFormat.ISODate)
            if dt.isValid():
                return dt.toLocalTime().toString("dd MMM yyyy, hh:mm:ss")
            else: return timestamp_str 
        except Exception: return timestamp_str 

    def load_inventory(self):
        self.clear_layout(self.scroll_layout)
        try:
            response = requests.get(API_INVENTORY_URL, timeout=5)
            if response.status_code != 200:
                raise Exception(f"Gagal memuat: Status {response.status_code}")
            
            log_list = response.json()
            if not log_list:
                info_label = QLabel("Tidak ada riwayat inventory untuk ditampilkan.")
                info_label.setFont(QFont("Roboto", 16))
                info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(info_label)
                return

            for log in sorted(log_list, key=lambda x: x.get('timestamp', ''), reverse=True):
                item_frame = QFrame()
                item_frame.setObjectName("historyItemFrame") 
                item_layout = QVBoxLayout(item_frame)
                
                timestamp = self.format_timestamp(log.get('timestamp', 'N/A'))
                quantity = log.get('quantityChange', 1)
                
                if quantity > 1:
                    header_color = "color: #006400;" # Hijau
                    tx_text = f"MASUK (+{quantity})"
                else:
                    header_color = "color: #8B0000;" # Merah
                    tx_text = f"KELUAR ({quantity})"
                
                tx_type = log.get('transactionType', 'N/A')
                header_text = f"{timestamp} — {tx_text} (Tipe: {tx_type})"
                header_label = QLabel(header_text)
                header_font = QFont("Roboto", 14) 
                header_label.setFont(header_font)
                header_label.setStyleSheet(header_color)
                
                detail_text = (
                    f"ID Item: {log.get('iD_Items', 'N/A')} "
                    f"(Oleh: {log.get('iD_Karyawan', 'N/A')})"
                )
                detail_label = QLabel(detail_text)
                detail_label.setFont(QFont("Roboto", 12)) 
                detail_label.setWordWrap(True)
                ref_doc = log.get('referenceDoc')

                item_layout.addWidget(header_label)
                item_layout.addWidget(detail_text)
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
        error_label = QLabel(str(message)) # (FIX) Konversi ke string
        error_label.setStyleSheet("color: red;")
        error_label.setFont(QFont("Roboto", 14))
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(error_label)