# File: main_app.py (Ganti file lama Anda dengan kode lengkap ini)

import sys
import os
import subprocess
import venv 

# --- Bagian 1: Fungsi Setup Environment ---

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def setup_environment():
    """
    Memastikan venv ada dan dependensi terinstal.
    """
    if sys.prefix != sys.base_prefix:
        print("Sudah berada di dalam Virtual Environment.")
        print(f"Memeriksa/menginstal dependensi dari {REQUIREMENTS_FILE}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE],
                stdout=subprocess.DEVNULL
            )
            print("Dependensi berhasil diperiksa/diinstal.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: Gagal menginstal dependensi di dalam venv. {e}")
            return False
        except FileNotFoundError:
            print(f"Error: File '{REQUIREMENTS_FILE}' tidak ditemukan.")
            return False
            
    print("Tidak berada di dalam Virtual Environment. Memulai setup...")

    if not os.path.exists(VENV_DIR):
        print(f"Folder '{VENV_DIR}' tidak ditemukan. Membuat virtual environment...")
        try:
            venv.create(VENV_DIR, with_pip=True)
            print(f"Virtual environment berhasil dibuat di '{VENV_DIR}'.")
        except Exception as e:
            print(f"Error: Gagal membuat virtual environment. {e}")
            return False
    else:
        print(f"Folder '{VENV_DIR}' sudah ada.")

    if sys.platform == "win32":
        pip_executable = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        pip_executable = os.path.join(VENV_DIR, "bin", "pip")

    if not os.path.exists(pip_executable):
        print(f"Error: 'pip' tidak ditemukan di {pip_executable}.")
        print("Coba hapus folder 'venv' dan jalankan lagi.")
        return False
        
    print(f"Menginstal dependensi dari '{REQUIREMENTS_FILE}' ke dalam '{VENV_DIR}'...")
    try:
        subprocess.check_call(
            [pip_executable, "install", "-r", REQUIREMENTS_FILE],
            stdout=subprocess.DEVNULL
        )
        print("Instalasi dependensi ke venv berhasil.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Gagal menginstal dependensi ke venv. {e}")
        return False
    except FileNotFoundError:
        print(f"Error: File '{REQUIREMENTS_FILE}' tidak ditemukan.")
        print("Pastikan file 'requirements.txt' ada di folder yang sama.")
        return False

    print("\n--- Setup Selesai ---")
    print(f"Silakan AKTIFKAN virtual environment Anda, lalu jalankan '{os.path.basename(__file__)}' lagi.")
    if sys.platform == "win32":
        print(f"Jalankan: .\\{VENV_DIR}\\Scripts\\activate")
    else:
        print(f"Jalankan: source {VENV_DIR}/bin/activate")
    
    return False

# --- Bagian 2: Titik Masuk Aplikasi ---

if __name__ == "__main__":
    
    apakah_siap_jalan = setup_environment()

    if apakah_siap_jalan:
        
        # --- Bagian 3: Impor Aplikasi (HANYA JIKA SIAP) ---
        print("Setup venv beres. Memulai aplikasi PySide6...")
        
        import requests 
        import uuid 
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QScrollArea, QStackedWidget, QFrame,
            QGridLayout, QDialog, QLineEdit, QComboBox, QFormLayout,
            QSpinBox, QMessageBox, QCalendarWidget, QDateEdit
        )
        from PySide6.QtGui import (
            QFont, QIcon, 
            QPixmap, QCursor
        )
        from PySide6.QtCore import (
            Qt, QSize, 
            Signal, QDateTime, QDate
        )
        
        # --- Bagian 4: Definisi Kelas ---
        
        # =======================================================
        # 0. DEFINISI URL API (PENTING!)
        # =======================================================
        API_BASE_URL = "http://localhost:5042/api"
        API_MACHINE_URL = f"{API_BASE_URL}/Machines"
        API_MAINTENANCE_URL = f"{API_BASE_URL}/Maintenance"
        API_INVENTORY_URL = f"{API_BASE_URL}/InventoryLogs"
        

        # =======================================================
        # 1. DEFINISI KELAS HELPER (POP-UP DAN KARTU)
        # =======================================================

        class ScheduleMaintenanceDialog(QDialog):
            """Form pop-up untuk menjadwalkan maintenance baru."""
            
            def __init__(self, machine_id, machine_name, parent=None):
                super().__init__(parent)
                
                self.machine_id = machine_id
                self.machine_name = machine_name
                
                self.setWindowTitle(f"Jadwalkan Maintenance - {self.machine_name}")
                self.setMinimumWidth(450)
                self.setStyleSheet("background-color: #FFFFFF; font-size: 14px;")

                layout = QVBoxLayout(self)
                form_layout = QFormLayout()
                form_layout.setSpacing(15)
                form_layout.setContentsMargins(15, 15, 15, 15)

                title = QLabel(f"Mesin: {self.machine_name}")
                title.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
                title.setStyleSheet("margin-bottom: 10px;")
                layout.addWidget(title)

                self.task_name_input = QLineEdit()
                self.task_name_input.setPlaceholderText("Contoh: Ganti Filter Oli")
                self.person_input = QLineEdit()
                self.person_input.setPlaceholderText("Contoh: Budi Sudarsono")
                self.komponen_combo = QComboBox()
                
                self.schedule_date_input = QDateEdit()
                self.schedule_date_input.setCalendarPopup(True)
                self.schedule_date_input.setMinimumDate(QDate.currentDate())
                self.schedule_date_input.setDisplayFormat("yyyy-MM-dd")
                
                form_layout.addRow("Nama Tugas:", self.task_name_input)
                form_layout.addRow("Penanggung Jawab:", self.person_input)
                form_layout.addRow("Tanggal Dijadwalkan:", self.schedule_date_input)
                form_layout.addRow("Komponen Mesin:", self.komponen_combo)

                layout.addLayout(form_layout)
                
                inv_frame = QFrame()
                inv_frame.setFrameShape(QFrame.Shape.StyledPanel)
                inv_frame.setStyleSheet("background-color: #F8F8F8; border-radius: 5px;")
                inv_layout = QVBoxLayout(inv_frame)
                
                inv_title = QLabel("Penggunaan Item Inventory (Opsional)")
                inv_title.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
                inv_layout.addWidget(inv_title)
                
                inv_form_layout = QFormLayout()
                inv_form_layout.setSpacing(10)
                self.item_id_input = QLineEdit()
                self.item_id_input.setPlaceholderText("Contoh: OLI-001")
                self.item_qty_spinbox = QSpinBox()
                self.item_qty_spinbox.setRange(0, 100) # (FIX) Biarkan 0 untuk log "KELUAR (0)" jika tidak diisi
                
                inv_form_layout.addRow("ID Item:", self.item_id_input)
                inv_form_layout.addRow("Jumlah (Qty):", self.item_qty_spinbox)
                
                inv_layout.addLayout(inv_form_layout)
                layout.addWidget(inv_frame)

                button_layout = QHBoxLayout()
                self.submit_button = QPushButton("Submit Jadwal")
                self.submit_button.setStyleSheet("background-color: #007ACC; color: white; padding: 10px; border-radius: 5px;")
                self.cancel_button = QPushButton("Batal")
                self.cancel_button.setStyleSheet("background-color: #DDDDDD; padding: 10px; border-radius: 5px;")
                
                button_layout.addStretch()
                button_layout.addWidget(self.cancel_button)
                button_layout.addWidget(self.submit_button)
                
                layout.addLayout(button_layout)

                self.submit_button.clicked.connect(self.submit_data)
                self.cancel_button.clicked.connect(self.reject)
                self.fetch_komponen_data()

            def fetch_komponen_data(self):
                """Mengambil daftar komponen untuk mesin ini dari API."""
                try:
                    url = f"{API_MACHINE_URL}/{self.machine_id}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        data_mesin = response.json()
                        self.komponen_combo.clear()
                        
                        list_komponen = data_mesin.get("components", [])
                        if not list_komponen:
                            self.komponen_combo.addItem("Tidak ada komponen terdaftar", None)
                        else:
                            self.komponen_combo.addItem("-- Pilih Komponen --", None)
                            for comp in list_komponen:
                                health = comp.get('health', 100)
                                
                                # ==========================================================
                                # (PERBAIKAN #1 DI SINI)
                                # Ganti 'componentName' (camelCase) menjadi 'component_name' (snake_case)
                                comp_name = comp.get("component_name") 
                                # ==========================================================
                                
                                display_text = f"{comp_name} (Health: {health}%)"
                                self.komponen_combo.addItem(display_text, comp_name)
                    else:
                        self.komponen_combo.addItem("Gagal memuat komponen", None)
                except Exception as e:
                    self.komponen_combo.addItem(f"Error: {e}", None)
                    
            def submit_data(self):
                task_name = self.task_name_input.text()
                person = self.person_input.text()
                komponen = self.komponen_combo.currentData()
                scheduled_date = self.schedule_date_input.date().toString("yyyy-MM-dd")
                
                item_id = self.item_id_input.text()
                item_qty = self.item_qty_spinbox.value()

                if not task_name or not person or not komponen:
                    QMessageBox.warning(self, "Input Tidak Lengkap", "Nama Tugas, Penanggung Jawab, dan Komponen tidak boleh kosong.")
                    return
                
                task_payload = {
                    "machineId": self.machine_id,
                    "componentName": komponen,
                    "taskName": task_name,
                    "personInCharge": person,
                    "scheduledDate": scheduled_date 
                }

                try:
                    task_url = f"{API_MAINTENANCE_URL}/schedule"
                    response_task = requests.post(task_url, json=task_payload, timeout=5)
                    
                    if response_task.status_code not in [200, 201]:
                        raise Exception(f"Gagal menyimpan tugas. Server merespons: {response_task.text}")

                    # (FIX "KELUAR (0)") Hanya log jika item ID *dan* Qty > 0
                    if item_id and item_qty > 0:
                        log_payload = {
                            "ID_Log": str(uuid.uuid4()), 
                            "ID_Items": item_id,
                            "ID_Karyawan": person,
                            "Transaction_Type": "OUT", 
                            "Quantity_Change": -item_qty, 
                            "Timestamp": QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate),
                            "Reference_Doc": f"Maint: {task_name} (Mesin: {self.machine_name})"
                        }
                        
                        response_log = requests.post(API_INVENTORY_URL, json=log_payload, timeout=5)
                        
                        if response_log.status_code not in [200, 201]:
                            QMessageBox.warning(self, "Peringatan", 
                                f"Tugas Maintenance berhasil disimpan, TAPI GAGAL mencatat log inventory.\n{response_log.text}")
                        else:
                            QMessageBox.information(self, "Sukses", "Jadwal maintenance DAN log inventory berhasil disimpan.")
                    else:
                        QMessageBox.information(self, "Sukses", "Jadwal maintenance berhasil disimpan (tanpa log inventory).")
                    
                    self.accept() 

                except requests.exceptions.ConnectionError:
                    QMessageBox.critical(self, "Error Koneksi", "Tidak dapat terhubung ke server. Pastikan backend C# berjalan.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Terjadi kesalahan:\n{e}")

        
        # (FIX #1 & #2) Form pop-up untuk menambah item inventory
        class AddItemDialog(QDialog):
            """Form pop-up untuk menambah item baru atau stok ke inventory."""
            
            def __init__(self, parent=None):
                super().__init__(parent)
                
                self.setWindowTitle("Tambah Item ke Inventory")
                self.setMinimumWidth(450)
                self.setStyleSheet("background-color: #FFFFFF; font-size: 14px;")

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
                # (FIX #1) Tombol submit yang hilang ditambahkan ke layout
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
                        # (FIX) Gunakan key snake_case 'ID_Items'
                        unique_ids = sorted(list(set(log.get("ID_Items") for log in logs if log.get("ID_Items"))))
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
                
                # (FIX #2) Pastikan Transaction_Type="IN" dan quantity positif
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

        class MaintenanceDialog(QDialog):
            """Pop-up untuk riwayat maintenance (dari Dashboard)."""
            def __init__(self, nama_mesin, list_task, parent=None):
                super().__init__(parent)
                
                self.setWindowTitle(f"Riwayat Maintenance - {nama_mesin}")
                self.setMinimumSize(500, 400)
                self.setStyleSheet("background-color: #FFFFFF;")
                layout = QVBoxLayout(self)
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setFrameShape(QFrame.Shape.NoFrame)
                scroll_content = QWidget()
                scroll_layout = QVBoxLayout(scroll_content)
                scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                scroll_layout.setSpacing(8) 
                scroll_area.setWidget(scroll_content)

                if not list_task:
                    label_task = QLabel("Tidak ada riwayat maintenance untuk mesin ini.")
                    label_task.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    scroll_layout.addWidget(label_task)
                else:
                    # (FIX #3) Perbaiki 'sorted' agar kebal 'None'
                    for task in sorted(list_task, key=lambda x: (x.get('scheduled_date') or x.get('last_date') or ''), reverse=True):
                        task_frame = QFrame()
                        task_layout = QVBoxLayout(task_frame)
                        
                        status = task.get('status')
                        if not status: 
                            if task.get('last_date'): status = "Completed"
                            else: status = "Scheduled"
                        
                        if status == "Completed":
                            date_display = f"Selesai: {task.get('last_date') or 'N/A'}"
                            task_frame.setObjectName("historyItemFrame") 
                            header_color = "color: #006400;" 
                        else:
                            date_display = f"Terjadwal: {task.get('scheduled_date') or 'N/A'}"
                            task_frame.setObjectName("scheduledTaskFrame") 
                            header_color = "color: #B9770E;" 

                        header_text = f"{date_display} — Komp: {task.get('component_name', 'N/A')}"
                        header_label = QLabel(header_text)
                        header_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
                        header_label.setStyleSheet(header_color) 
                        
                        detail_text = f"Tugas: {task.get('task_name', 'N/A')} (Oleh: {task.get('person_in_charge', 'N/A')})"
                        # (FIX #3) Pastikan ini adalah QLabel
                        detail_label = QLabel(detail_text) 
                        detail_label.setFont(QFont("Roboto", 10))
                        detail_label.setWordWrap(True)
                        
                        task_layout.addWidget(header_label)
                        task_layout.addWidget(detail_label)
                        
                        scroll_layout.addWidget(task_frame)

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

        
        # --- (MODIFIKASI) TextCard sekarang menggunakan data LIVE ---
        class TextCard(QFrame):
            """Widget kustom HANYA UNTUK TEKS mesin di dashboard."""
            clicked = Signal(str)

            # (MODIFIKASI) Hanya menerima nama dan health (4 argumen)
            def __init__(self, machine_id, nama_mesin, health_percent):
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
                
                # (MODIFIKASI) Hanya tampilkan Health
                health_widget = self.buat_info_label("Health:", f"{health_percent}%")
                
                if health_percent < 80:
                    health_widget.setStyleSheet("color: #D35400; background-color: transparent; font-size: 14px;")
                else:
                    health_widget.setStyleSheet("color: #006400; background-color: transparent; font-size: 14px;")

                info_layout.addWidget(health_widget)
                
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

        
        # =======================================================
        # 2. DEFINISI KELAS HALAMAN
        # =======================================================

        # --- (MODIFIKASI BESAR) HALAMAN DASHBOARD SEKARANG LIVE ---
        class DashboardPage(QWidget):
            """Halaman dashboard utama yang mengambil data LIVE dari API."""
            
            def __init__(self):
                super().__init__()
                
                self.machine_image_map = {
                    "4": "views/images/MesiN Bor Meja.jpg",
                    "2": "views/images/Mesin Press Brake.jpg",
                    "1": "views/images/mesin-Laser Cutter.jpeg",
                    "3": "views/images/mesin-bubut.jpg",
                }

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
            
            # (FIX #5) Refresh otomatis saat tab diklik
            def showEvent(self, event):
                print("Menampilkan DashboardPage, memuat data...")
                self.load_machines_from_api()
                event.accept()
            
            def clear_layout(self, layout):
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            
            def show_error(self, message):
                self.clear_layout(self.grid_layout)
                error_label = QLabel(str(message)) # (FIX #2) Konversi ke string
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid_layout.addWidget(error_label, 0, 0) # (FIX #2) Tambahkan QLABEL

            def load_machines_from_api(self):
                """Memuat data LIVE dari API untuk Dashboard."""
                
                self.clear_layout(self.grid_layout)
                KOLOM_PER_MESIN = 4 
                
                try:
                    response = requests.get(API_MACHINE_URL, timeout=5) 
                    if response.status_code != 200:
                        raise Exception(f"Gagal memuat: Status {response.status_code}")
                    
                    machines_data = response.json()
                    
                    if not machines_data:
                        self.show_error("Database terhubung.\nBelum ada data mesin untuk ditampilkan.")
                        return

                    for i, machine in enumerate(machines_data):
                        
                        machine_id = machine.get("machine_id", "NO_ID")
                        machine_name = machine.get("machine", "Nama Tidak Ditemukan")
                        health = machine.get("overallHealth", 100)
                        
                        gbr_mesin = self.machine_image_map.get(machine_id, "views/images/default.jpg") 

                        kartu_gambar = ImageCard(
                            machine_id,
                            gbr_mesin
                        )
                        
                        # (FIX #1) Panggil TextCard dengan 4 argumen (data live)
                        kartu_teks = TextCard(
                            machine_id,
                            machine_name,
                            health # Kirim health asli
                        )
                        
                        kartu_gambar.clicked.connect(self.tampilkan_maintenance_dari_api)
                        kartu_teks.clicked.connect(self.tampilkan_maintenance_dari_api)
                        
                        baris = (i // KOLOM_PER_MESIN) * 2 
                        kolom = i % KOLOM_PER_MESIN
                        
                        self.grid_layout.addWidget(kartu_gambar, baris, kolom)
                        self.grid_layout.addWidget(kartu_teks, baris + 1, kolom)

                    baris_selanjutnya = (len(machines_data) // KOLOM_PER_MESIN + 1) * 2
                    self.grid_layout.setRowStretch(baris_selanjutnya, 1)
                    self.grid_layout.setColumnStretch(KOLOM_PER_MESIN, 1)

                except requests.exceptions.ConnectionError as e:
                    self.show_error(f"Error Koneksi:\n{e}\n\nPastikan backend .NET Anda berjalan.")
                except requests.exceptions.Timeout:
                    self.show_error("Error: Permintaan timeout.\nPastikan API server berjalan dan responsif.")
                except Exception as e:
                    self.show_error(f"Terjadi error: {e}")


            def tampilkan_maintenance_dari_api(self, machine_id):
                print(f"Mengambil data maintenance untuk machine_id: {machine_id}...")
                try:
                    response = requests.get(f"{API_MAINTENANCE_URL}/{machine_id}", timeout=5)
                    if response.status_code == 200:
                        list_task = response.json()
                        
                        nama_mesin = "Mesin"
                        try:
                            # Ambil nama live dari API
                            resp_mesin = requests.get(f"{API_MACHINE_URL}/{machine_id}", timeout=2)
                            if resp_mesin.status_code == 200:
                                nama_mesin = resp_mesin.json().get("machine", "Mesin")
                        except:
                            pass 

                        dialog = MaintenanceDialog(nama_mesin, list_task, self)
                        dialog.exec()
                    else:
                        error_dialog = MaintenanceDialog(
                            f"Error {response.status_code}", 
                            [{"task_name": f"Gagal mengambil data dari API.\n{response.text}"}], 
                            self
                        )
                        error_dialog.exec()
                except requests.exceptions.ConnectionError:
                    error_dialog = MaintenanceDialog( "Error Koneksi", 
                        [{"task_name": "Tidak dapat terhubung ke API.\nPastikan backend .NET Anda sedang berjalan."}], self )
                    error_dialog.exec()
                except Exception as e:
                    error_dialog = MaintenanceDialog( "Error", [{"task_name": f"Terjadi kesalahan:\n{e}"}], self )
                    error_dialog.exec()


        # --- (MODIFIKASI UTAMA DI SINI) ---
        class AssetMonitoringPage(QWidget):
            """Menampilkan daftar mesin dari API DENGAN NOTIFIKASI HEALTH."""
            
            def __init__(self):
                super().__init__()
                
                main_layout = QVBoxLayout(self)
                main_layout.setContentsMargins(0, 0, 0, 0)
                title_label = QLabel("Daftar Mesin & Status") 
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
                
            # (FIX #5) Refresh otomatis saat tab diklik
            def showEvent(self, event):
                print("Menampilkan AssetMonitoringPage, memuat data...")
                self.load_machines_live()
                event.accept()

            def open_schedule_dialog(self, machine_id, machine_name):
                """Membuka pop-up form ScheduleMaintenanceDialog."""
                dialog = ScheduleMaintenanceDialog(machine_id, machine_name, self)
                if dialog.exec():
                    print("Dialog ditutup dengan sukses, me-refresh daftar...")
                    self.load_machines_live() # Muat ulang HANYA jika dialog sukses
                else:
                    print("Dialog dibatalkan.")

            def clear_layout(self, layout):
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            
            # (BARU) Helper untuk menentukan status
            def get_status_details(self, machine_data):
                health = machine_data.get("overallHealth", 100)
                
                problem_component = None
                # Cari komponen pertama yang health-nya tidak 100
                for comp in machine_data.get("components", []):
                    if comp.get("health", 100) < 100:
                        
                        # ==========================================================
                        # (PERBAIKAN #2 DI SINI)
                        # Ganti 'componentName' (camelCase) menjadi 'component_name' (snake_case)
                        problem_component = comp.get("component_name", "Komponen Tidak Dikenal")
                        # ==========================================================
                        
                        break # Ambil yang pertama saja
                
                if health < 50:
                    return (health, "Berisiko", problem_component, "warningMachineFrame", "statusDotRed")
                elif health < 80:
                    return (health, "Perlu Cek", problem_component, "cautionMachineFrame", "statusDotYellow")
                else:
                    return (health, "Optimal", None, "historyItemFrame", "statusDotGreen")

            # (MODIFIKASI) Fungsi ini sekarang menggunakan data LIVE
            def load_machines_live(self):
                """Mengambil data dari GET /api/Machines dan menampilkannya."""
                self.clear_layout(self.scroll_layout)
                
                try:
                    response = requests.get(API_MACHINE_URL, timeout=5) 
                    if response.status_code == 200:
                        machines_data = response.json()
                        if not machines_data:
                            info_label = QLabel("Database terhubung.\nBelum ada data mesin untuk ditampilkan.")
                            info_label.setFont(QFont("Roboto", 16))
                            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.scroll_layout.addWidget(info_label)
                            return

                        # (MODIFIKASI) Loop melalui data LIVE
                        for machine in machines_data:
                            machine_id = machine.get("machine_id", "NO_ID")
                            machine_name = machine.get("machine", "Nama Tidak Ditemukan")
                            
                            # (MODIFIKASI) Ambil data LIVE dari helper
                            health, status_text, problem, frame_style, dot_style = self.get_status_details(machine)
                            
                            # Frame utama untuk baris
                            row_frame = QFrame()
                            row_layout = QHBoxLayout(row_frame)
                            row_layout.setContentsMargins(15, 10, 15, 10) # Beri padding
                            
                            # (BARU) Dot Indikator Status
                            status_dot = QLabel()
                            status_dot.setFixedSize(16, 16)
                            status_dot.setObjectName(dot_style) # Style dari helper
                            
                            # (BARU) Layout Kiri (Nama, Status, Info Komponen)
                            left_layout = QVBoxLayout()
                            left_layout.setSpacing(2)
                            
                            name_label = QLabel(f"{machine_name} (Health: {health}%)")
                            name_label.setFont(QFont("Roboto", 16, QFont.Weight.Bold))
                            
                            status_label = QLabel(f"Status: {status_text}")
                            status_label.setFont(QFont("Roboto", 12))
                            
                            left_layout.addWidget(name_label)
                            left_layout.addWidget(status_label)
                            
                            # (BARU) Tambahkan info komponen jika ada masalah
                            if problem:
                                problem_label = QLabel(f"Komponen Bermasalah: {problem}")
                                problem_label.setObjectName("problemLabel")
                                left_layout.addWidget(problem_label)
                            
                            # Tombol Jadwalkan
                            schedule_button = QPushButton("Jadwalkan Maintenance")
                            schedule_button.setFont(QFont("Roboto", 14))
                            schedule_button.setCursor(QCursor(Qt.PointingHandCursor))
                            schedule_button.setObjectName("scheduleButton")
                            
                            schedule_button.clicked.connect(
                                lambda checked=False, id=machine_id, name=machine_name: self.open_schedule_dialog(id, name)
                            )
                            
                            # Susun layout baris
                            row_layout.addWidget(status_dot) # Dot di kiri
                            row_layout.addLayout(left_layout) # Teks di tengah
                            row_layout.addStretch()
                            row_layout.addWidget(schedule_button) # Tombol di kanan
                            
                            row_frame.setObjectName(frame_style) # Style dari helper
                            
                            self.scroll_layout.addWidget(row_frame)
                            
                    else:
                        self.show_error(f"Gagal memuat: Status {response.status_code}")
                except requests.exceptions.ConnectionError as e:
                    self.show_error(f"Error Koneksi:\n{e}\n\nPastikan Windows Firewall mengizinkan python.exe dan backend berjalan.")
                except requests.exceptions.Timeout:
                    self.show_error("Error: Permintaan timeout.\nPastikan API server berjalan dan responsif.")
                except Exception as e:
                    self.show_error(f"Terjadi error: {e}")

            def show_error(self, message):
                self.clear_layout(self.scroll_layout)
                error_label = QLabel(str(message)) # (FIX #2) Konversi ke string
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(error_label) # (FIX #2) Tambahkan QLABEL


        class MaintenanceHistoryPage(QWidget):
            """Menampilkan DUA daftar: Terjadwal dan Selesai (Request #1)."""
            def __init__(self):
                super().__init__()
                main_layout = QVBoxLayout(self)
                main_layout.setContentsMargins(0, 0, 0, 0)
                
                # (BARU) Layout untuk Judul dan Tombol Refresh
                title_layout = QHBoxLayout()
                title_label = QLabel("Maintenance History") # Judul utama
                title_label.setFont(QFont("Roboto", 18, QFont.Weight.Bold))
                
                self.refresh_button = QPushButton("Refresh")
                self.refresh_button.setObjectName("scheduleButton") # Style biru
                self.refresh_button.setFixedWidth(100)
                
                title_layout.addWidget(title_label)
                title_layout.addStretch()
                title_layout.addWidget(self.refresh_button)
                
                main_layout.addLayout(title_layout) # Tambahkan layout judul
                
                columns_layout = QHBoxLayout()
                columns_layout.setSpacing(20) 
                
                # Kolom 1: Terjadwal
                scheduled_widget = QWidget()
                scheduled_layout = QVBoxLayout(scheduled_widget)
                scheduled_title = QLabel("Tugas Terjadwal")
                scheduled_title.setFont(QFont("Roboto", 16, QFont.Weight.Bold)) # Ukuran sub-judul
                self.scheduled_scroll_area = QScrollArea()
                self.scheduled_scroll_area.setWidgetResizable(True)
                self.scheduled_scroll_area.setObjectName("scrollArea")
                self.scheduled_content = QWidget()
                self.scheduled_layout = QVBoxLayout(self.scheduled_content)
                self.scheduled_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.scheduled_scroll_area.setWidget(self.scheduled_content)
                scheduled_layout.addWidget(scheduled_title)
                scheduled_layout.addWidget(self.scheduled_scroll_area)
                
                # Kolom 2: Selesai
                completed_widget = QWidget()
                completed_layout = QVBoxLayout(completed_widget)
                completed_title = QLabel("Riwayat Selesai")
                completed_title.setFont(QFont("Roboto", 16, QFont.Weight.Bold)) # Ukuran sub-judul
                self.completed_scroll_area = QScrollArea()
                self.completed_scroll_area.setWidgetResizable(True)
                self.completed_scroll_area.setObjectName("scrollArea")
                self.completed_content = QWidget()
                self.completed_layout = QVBoxLayout(self.completed_content)
                self.completed_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.completed_scroll_area.setWidget(self.completed_content)
                completed_layout.addWidget(completed_title)
                completed_layout.addWidget(self.completed_scroll_area)

                columns_layout.addWidget(scheduled_widget, 1) 
                columns_layout.addWidget(completed_widget, 1) 
                
                main_layout.addLayout(columns_layout)
                self.setLayout(main_layout)
                
                self.refresh_button.clicked.connect(self.load_history)
            
            # (FIX #5) Refresh otomatis saat tab diklik
            def showEvent(self, event):
                print("Menampilkan MaintenanceHistoryPage, memuat data...")
                self.load_history()
                event.accept()

            def clear_layouts(self):
                while self.scheduled_layout.count():
                    child = self.scheduled_layout.takeAt(0)
                    if child.widget(): child.widget().deleteLater()
                while self.completed_layout.count():
                    child = self.completed_layout.takeAt(0)
                    if child.widget(): child.widget().deleteLater()

            def complete_task(self, machine_id, component_name, task_id):
                """Memanggil API untuk menandai tugas sebagai selesai (Request #3)."""
                print(f"Menandai selesai: M:{machine_id}, C:{component_name}, T:{task_id}")
                try:
                    url = f"{API_MAINTENANCE_URL}/complete"
                    params = {
                        "machineId": machine_id,
                        "componentName": component_name,
                        "taskId": task_id
                    }
                    response = requests.put(url, params=params, timeout=5)
                    
                    if response.status_code == 200:
                        QMessageBox.information(self, "Sukses", "Tugas ditandai selesai! Status komponen telah diperbarui.")
                        self.load_history() 
                    else:
                        raise Exception(f"Gagal update: {response.text}")
                        
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Gagal menyelesaikan tugas:\n{e}")

            def load_history(self):
                """Mengambil data API dan membaginya ke dua kolom."""
                self.clear_layouts()
                
                try:
                    response = requests.get(API_MAINTENANCE_URL, timeout=5)
                    if response.status_code != 200:
                        raise Exception(f"Gagal memuat: Status {response.status_code}")
                    
                    all_tasks = response.json()
                    
                    if not all_tasks:
                        info_label = QLabel("Tidak ada riwayat maintenance.")
                        info_label.setFont(QFont("Roboto", 16))
                        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.scheduled_layout.addWidget(info_label)
                        return

                    scheduled_tasks = []
                    completed_tasks = []
                    
                    for task in all_tasks:
                        status = task.get("status")
                        task_id = task.get("task_id") 
                        
                        if not status: 
                            if task.get("last_date"): status = "Completed"
                            else: status = "Scheduled"
                        
                        # (FIX #4) Pindahkan data lama (tanpa task_id) ke Selesai
                        if status == "Scheduled" and not task_id:
                            status = "Completed_Old_Data" 
                        
                        if status == "Completed" or status == "Completed_Old_Data":
                            completed_tasks.append(task)
                        else:
                            scheduled_tasks.append(task)
                    
                    if not scheduled_tasks:
                        self.scheduled_layout.addWidget(QLabel("Tidak ada tugas terjadwal."))
                    
                    # (FIX #3) Urutkan dengan benar, tangani None
                    for item in sorted(scheduled_tasks, key=lambda x: (x.get('scheduled_date') or '')):
                        item_frame = QFrame()
                        item_frame.setObjectName("scheduledTaskFrame")
                        item_layout = QVBoxLayout(item_frame)
                        
                        scheduled_date = item.get('scheduled_date') or 'N/A'
                        header_text = f"Terjadwal: {scheduled_date} — {item.get('machine', 'N/A')}"
                        header_label = QLabel(header_text)
                        header_label.setObjectName("scheduledTaskHeader")
                        
                        detail_text = f"Tugas: {item.get('task_name', 'N/A')} (Oleh: {item.get('person_in_charge', 'N/A')})"
                        detail_label = QLabel(detail_text)
                        detail_label.setObjectName("taskDetailLabel")
                        detail_label.setWordWrap(True)
                        
                        complete_button = QPushButton("Tandai Selesai")
                        complete_button.setObjectName("completeButton")
                        complete_button.setCursor(QCursor(Qt.PointingHandCursor))
                        
                        machine_id = item.get('machine_id')
                        component_name = item.get('component_name')
                        task_id = item.get('task_id')
                        
                        if all([machine_id, component_name, task_id]):
                             complete_button.clicked.connect(
                                 lambda checked=False, mid=machine_id, cn=component_name, tid=task_id: self.complete_task(mid, cn, tid)
                             )
                        else:
                            complete_button.setText("Error: Data tidak lengkap")
                            complete_button.setDisabled(True)
                        
                        item_layout.addWidget(header_label)
                        item_layout.addWidget(detail_label)
                        item_layout.addStretch() 
                        item_layout.addWidget(complete_button)
                        self.scheduled_layout.addWidget(item_frame)

                    if not completed_tasks:
                        self.completed_layout.addWidget(QLabel("Tidak ada riwayat selesai."))
                    
                    # (FIX #3) Urutkan dengan benar, tangani None
                    for item in sorted(completed_tasks, key=lambda x: (x.get('last_date') or x.get('scheduled_date') or ''), reverse=True):
                        item_frame = QFrame()
                        item_frame.setObjectName("historyItemFrame")
                        item_layout = QVBoxLayout(item_frame)
                        
                        completed_date = item.get('last_date')
                        
                        if not completed_date and not item.get('scheduled_date'):
                            header_text = f"Selesai (Data Lama) — {item.get('machine', 'N/A')}"
                            header_label = QLabel(header_text)
                            header_label.setObjectName("completedTaskHeader")
                            header_label.setStyleSheet("color: #777; font-style: italic;") 
                        else:
                            header_text = f"Selesai: {completed_date or 'N/A'} — {item.get('machine', 'N/A')}"
                            header_label = QLabel(header_text)
                            header_label.setObjectName("completedTaskHeader")
                        
                        detail_text = f"Tugas: {item.get('task_name', 'N/A')} (Penanggung Jawab: {item.get('person_in_charge', 'N/A')})"
                        detail_label = QLabel(detail_text)
                        detail_label.setObjectName("taskDetailLabel")
                        detail_label.setWordWrap(True)

                        item_layout.addWidget(header_label)
                        item_layout.addWidget(detail_label)
                        self.completed_layout.addWidget(item_frame)

                except requests.exceptions.ConnectionError as e:
                    self.show_error(f"Error Koneksi: {e}")
                except requests.exceptions.Timeout:
                    self.show_error("Error: Permintaan timeout.")
                except Exception as e:
                    self.show_error(f"Terjadi error: {e}") 

            def show_error(self, message):
                self.clear_layouts()
                error_label = QLabel(str(message)) # (FIX #2) Konversi ke string
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scheduled_layout.addWidget(error_label) # (FIX #2) Tambahkan QLABEL
        
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
            
            # (FIX #5) Refresh otomatis saat tab diklik
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

                    # (FIX) Gunakan key 'Timestamp' dari C#
                    for log in sorted(log_list, key=lambda x: x.get('Timestamp', ''), reverse=True):
                        item_frame = QFrame()
                        item_frame.setObjectName("historyItemFrame") 
                        item_layout = QVBoxLayout(item_frame)
                        
                        # (FIX) Ganti key camelCase -> snake_case
                        timestamp = self.format_timestamp(log.get('Timestamp', 'N/A'))
                        quantity = log.get('Quantity_Change', 0)
                        
                        if quantity > 0:
                            header_color = "color: #006400;" # Hijau
                            tx_text = f"MASUK (+{quantity})"
                        else:
                            header_color = "color: #8B0000;" # Merah
                            tx_text = f"KELUAR ({quantity})"
                        
                        # (FIX) Ganti key camelCase -> snake_case
                        tx_type = log.get('Transaction_Type', 'N/A')
                        header_text = f"{timestamp} — {tx_text} (Tipe: {tx_type})"
                        header_label = QLabel(header_text)
                        header_font = QFont("Roboto", 14) 
                        header_label.setFont(header_font)
                        header_label.setStyleSheet(header_color)
                        
                        # (FIX) Ganti key camelCase -> snake_case
                        detail_text = (
                            f"ID Item: {log.get('ID_Items', 'N/A')} "
                            f"(Oleh: {log.get('ID_Karyawan', 'N/A')})"
                        )
                        detail_label = QLabel(detail_text)
                        detail_label.setFont(QFont("Roboto", 12)) 
                        detail_label.setWordWrap(True)
                        
                        # (FIX) Ganti key camelCase -> snake_case
                        ref_doc = log.get('Reference_Doc')

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
                error_label = QLabel(str(message)) # (FIX #2) Konversi ke string
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(error_label)
        
        
        # =======================================================
        # 4. DEFINISI KELAS JENDELA UTAMA (MAINWINDOW)
        # =======================================================
        class MainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("CMMS Dashboard - Mesin Industri")
                self.setGeometry(100, 100, 1100, 720)
                self.main_widget = QWidget()
                self.main_layout = QHBoxLayout(self.main_widget)
                self.main_layout.setContentsMargins(0, 0, 0, 0)
                self.main_layout.setSpacing(0) 
                self.setup_sidebar()
                self.setup_main_content()
                self.main_layout.addWidget(self.sidebar_frame, 1) 
                self.main_layout.addWidget(self.content_frame, 4) 
                self.setCentralWidget(self.main_widget)

            def setup_sidebar(self):
                self.sidebar_frame = QWidget()
                self.sidebar_frame.setObjectName("sidebar")
                sidebar_layout = QVBoxLayout(self.sidebar_frame)
                sidebar_layout.setContentsMargins(10, 20, 10, 20)
                sidebar_layout.setSpacing(15)
                self.sidebar_label = QLabel("CMMS Menu")
                font = QFont("Roboto", 20)
                font.setBold(True)
                self.sidebar_label.setFont(font)
                self.sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.sidebar_label.setStyleSheet("margin-bottom: 20px;")
                sidebar_layout.addWidget(self.sidebar_label)
                
                self.btn_dashboard = QPushButton("Dashboard")
                self.btn_asset_monitoring = QPushButton("Asset Monitoring")
                self.btn_history = QPushButton("Maintenance History")
                self.btn_inventory = QPushButton("Inventory")
                
                sidebar_layout.addWidget(self.btn_dashboard)
                sidebar_layout.addWidget(self.btn_asset_monitoring)
                sidebar_layout.addWidget(self.btn_history)
                sidebar_layout.addWidget(self.btn_inventory)
                
                sidebar_layout.addStretch() 

            def setup_main_content(self):
                self.content_frame = QWidget()
                self.content_frame.setObjectName("contentArea")
                content_layout = QVBoxLayout(self.content_frame)
                content_layout.setContentsMargins(20, 20, 20, 20) 
                self.stacked_widget = QStackedWidget()
                content_layout.addWidget(self.stacked_widget)

                self.dashboard_page = DashboardPage()
                self.asset_page = AssetMonitoringPage()
                self.history_page = MaintenanceHistoryPage()
                self.inventory_page = InventoryPage() 

                self.stacked_widget.addWidget(self.dashboard_page)
                self.stacked_widget.addWidget(self.asset_page)
                self.stacked_widget.addWidget(self.history_page)
                self.stacked_widget.addWidget(self.inventory_page) 

                self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))
                self.btn_asset_monitoring.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.asset_page))
                self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.history_page))
                self.btn_inventory.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.inventory_page))
                
                self.stacked_widget.setCurrentWidget(self.dashboard_page)

        # --- (MODIFIKASI) CSS Global (QSS) ---
        GLOBAL_STYLESHEET = """
        QWidget#sidebar { background-color: #E8E8E8; }
        QWidget#sidebar QLabel { color: #333333; background-color: transparent; }
        QWidget#sidebar QPushButton {
            background-color: #D0D0D0; color: #222222; border: none;
            padding: 12px; font-size: 16px; font-family: Roboto;
            text-align: left; border-radius: 5px;
        }
        QWidget#sidebar QPushButton:hover { background-color: #C0C0C0; }
        QWidget#sidebar QPushButton:pressed { background-color: #B0B0B0; }
        
        QWidget#contentArea { background-color: #F4F4F4; font-family: Roboto; }
        QWidget#contentArea QLabel { background-color: transparent; }
        
        QPushButton#machineButton {
            background-color: #FFFFFF; border: 1px solid #DDDDDD;
            border-radius: 5px; font-size: 15px;
        }
        QPushButton#machineButton:hover { background-color: #F0F0F0; }

        /* (BARU) Frame Kartu Peringatan (Merah) */
        QFrame#warningMachineFrame {
            background-color: #FADBD8; 
            border: 1px solid #E74C3C; 
            border-radius: 8px; 
            margin-bottom: 8px;
        }
        
        /* (BARU) Frame Kartu Hati-hati (Kuning) */
        QFrame#cautionMachineFrame {
            background-color: #FFF9E6; 
            border: 1px solid #F39C12;
            border-radius: 8px; 
            margin-bottom: 8px;
        }

        /* Frame Kartu Default (Riwayat Selesai & Asset Normal) */
        QFrame#historyItemFrame {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px; /* Sudut lebih bulat */
            padding: 10px;
            margin-bottom: 8px;
        }

        /* Label Header di Kartu Selesai */
        QLabel#completedTaskHeader {
            font-size: 16px;
            font-weight: bold;
            color: #006400; /* Hijau tua */
        }

        /* Frame Kartu Terjadwal */
        QFrame#scheduledTaskFrame {
            background-color: #FFF9E6; /* Kuning sangat pucat */
            border: 1px solid #F39C12; /* Border oranye */
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }

        /* Label Header di Kartu Terjadwal */
        QLabel#scheduledTaskHeader {
            font-size: 16px;
            font-weight: bold;
            color: #B9770E; /* Oranye tua */
        }
        
        /* Tombol "Tandai Selesai" */
        QPushButton#completeButton {
            background-color: #2ECC71; /* Hijau */
            color: white;
            font-weight: bold;
            font-size: 14px;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            margin-top: 10px;
        }
        QPushButton#completeButton:hover { background-color: #27AE60; }
        QPushButton#completeButton:pressed { background-color: #1E8449; }
        
        /* (BARU) Tombol "Jadwalkan Maintenance" */
        QPushButton#scheduleButton {
            background-color: #007ACC;
            color: white;
            font-size: 14px;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
        }
        QPushButton#scheduleButton:hover { background-color: #005A9C; }

        /* (PERBAIKAN UI) Menghilangkan "box-in-a-box" */
        QFrame QLabel {
            background-color: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }
        
        /* (PERBAIKAN UI) Label Detail Tugas */
        QLabel#taskDetailLabel {
            font-size: 14px;
            margin-top: 5px;
        }
        
        /* (BARU) Label Komponen Bermasalah */
        QLabel#problemLabel {
            font-size: 11px;
            font-style: italic;
            color: #C0392B; /* Merah */
            margin-top: 4px;
        }
        
        /* (BARU) Dot Indikator Status */
        QLabel#statusDot {
            min-width: 16px;
            max-width: 16px;
            min-height: 16px;
            max-height: 16px;
            border-radius: 8px;
            margin-right: 10px;
        }
        QLabel#statusDotGreen  { background-color: #2ECC71; }
        QLabel#statusDotYellow { background-color: #F39C12; }
        QLabel#statusDotRed    { background-color: #E74C3C; }


        QFrame#imageCard {
            background-color: #FFFFFF; border: 1px solid #DDDDDD; border-radius: 8px;
        }
        QFrame#imageCard:hover { background-color: #F9F9F9; border: 1px solid #C0C0C0; }
        QFrame#textCard {
            background-color: #FFFFFF; border: 1px solid #DDDDDD; border-radius: 8px;
        }
        QFrame#textCard:hover { background-color: #F9F9F9; border: 1px solid #C0C0C0; }
        
        QScrollArea { border: none; background-color: #F4F4F4; }
        QWidget#scrollAreaWidgetContents { background-color: #F4F4F4; }
        
        QWidget { background-color: transparent; color: #333; }
        
        QLineEdit, QComboBox, QSpinBox, QDateEdit {
            background-color: #FFFFFF; border: 1px solid #CCCCCC;
            border-radius: 4px; padding: 8px; font-size: 14px;
        }
        QCalendarWidget QWidget { background-color: #FFFFFF; }
        QComboBox::drop-down { border: none; }
        """

        # --- Bagian 5: Peluncuran Aplikasi ---
        
        app = QApplication(sys.argv)
        app.setStyleSheet(GLOBAL_STYLESHEET)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:
        # --- Setup Gagal atau Selesai (Global) ---
        print("\nSkrip berhenti. Silakan ikuti instruksi di atas untuk mengaktifkan venv.")
        sys.exit(0)