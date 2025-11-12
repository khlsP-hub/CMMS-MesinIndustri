# views/main.py

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
    
    # 1. Cek apakah kita sudah di dalam venv
    if sys.prefix != sys.base_prefix:
        print("Sudah berada di dalam Virtual Environment.")
        print(f"Memeriksa/menginstal dependensi dari {REQUIREMENTS_FILE}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_FILE],
                stdout=subprocess.DEVNULL
            )
            print("Dependensi berhasil diperiksa/diinstal.")
            return True # Siap menjalankan aplikasi
        except subprocess.CalledProcessError as e:
            print(f"Error: Gagal menginstal dependensi di dalam venv. {e}")
            return False
        except FileNotFoundError:
            print(f"Error: File '{REQUIREMENTS_FILE}' tidak ditemukan.")
            return False
            
    # 2. Jika kita TIDAK di dalam venv (dijalankan global)
    print("Tidak berada di dalam Virtual Environment. Memulai setup...")

    # 3. Buat venv jika belum ada
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

    # 4. Tentukan path pip di dalam venv
    if sys.platform == "win32":
        pip_executable = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        pip_executable = os.path.join(VENV_DIR, "bin", "pip")

    if not os.path.exists(pip_executable):
        print(f"Error: 'pip' tidak ditemukan di {pip_executable}.")
        print("Coba hapus folder 'venv' dan jalankan lagi.")
        return False
        
    # 5. Instal dependensi ke dalam venv tersebut
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

    # 6. Beri instruksi kepada pengguna
    print("\n--- Setup Selesai ---")
    print(f"Silakan AKTIFKAN virtual environment Anda, lalu jalankan '{os.path.basename(__file__)}' lagi.")
    if sys.platform == "win32":
        print(f"Jalankan: .\\{VENV_DIR}\\Scripts\\activate")
    else:
        print(f"Jalankan: source {VENV_DIR}/bin/activate")
    
    return False # False karena aplikasi utama belum boleh berjalan


# --- Bagian 2: Titik Masuk Aplikasi ---

if __name__ == "__main__":
    
    # 1. Jalankan setup.
    apakah_siap_jalan = setup_environment()

    # 2. HANYA JIKA siap (True), baru kita impor dan jalankan aplikasi
    if apakah_siap_jalan:
        
        # --- Bagian 3: Impor Aplikasi (HANYA JIKA SIAP) ---
        print("Setup venv beres. Memulai aplikasi PySide6...")
        
        import requests 
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QScrollArea, QStackedWidget, QFrame,
            QGridLayout, QDialog
        )
        from PySide6.QtGui import (
            QFont, QIcon, 
            QPixmap, QCursor
        )
        from PySide6.QtCore import (
            Qt, QSize, 
            Signal, QDateTime # <-- Pastikan QDateTime diimpor
        )

        # --- Bagian 4: Definisi Kelas (URUTAN SUDAH DIPERBAIKI) ---

        # =======================================================
        # 1. DEFINISI KELAS HELPER (POP-UP DAN KARTU)
        # =======================================================

        class MaintenanceDialog(QDialog):
            """Jendela dialog (pop-up) untuk menampilkan DAFTAR maintenance task."""
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
                    for task in list_task:
                        task_frame = QFrame()
                        task_frame.setObjectName("historyItemFrame") 
                        task_layout = QVBoxLayout(task_frame)
                        
                        header_text = f"{task.get('last_date', 'N/A')} — Komponen: {task.get('component_name', 'N/A')}"
                        header_label = QLabel(header_text)
                        header_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
                        header_label.setStyleSheet("color: #003366;") 
                        
                        detail_text = f"Tugas: {task.get('task_name', 'N/A')} (Oleh: {task.get('person_in_charge', 'N/A')})"
                        detail_label = QLabel(detail_text)
                        detail_label.setFont(QFont("Roboto", 10))
                        
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

        
        # =======================================================
        # 2. DEFINISI KELAS HALAMAN
        # =======================================================

        class DashboardPage(QWidget):
            """Halaman dashboard utama dengan kartu gambar di atas kartu teks."""
            
            API_MACHINE_URL = "http://localhost:5042/api/Machines"
            API_MAINTENANCE_URL = "http://localhost:5042/api/Maintenance"
            API_INVENTORY_URL = "http://localhost:5042/api/InventoryLogs" # <-- Tambah URL Inventory
            
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
                    
                    kartu_gambar.clicked.connect(self.tampilkan_maintenance_dari_api)
                    kartu_teks.clicked.connect(self.tampilkan_maintenance_dari_api)
                    
                    baris = (i // KOLOM_PER_MESIN) * 2 
                    kolom = i % KOLOM_PER_MESIN
                    self.grid_layout.addWidget(kartu_gambar, baris, kolom)
                    self.grid_layout.addWidget(kartu_teks, baris + 1, kolom)

                baris_selanjutnya = (len(self.data_mesin_statis) // KOLOM_PER_MESIN + 1) * 2
                self.grid_layout.setRowStretch(baris_selanjutnya, 1)
                self.grid_layout.setColumnStretch(KOLOM_PER_MESIN, 1)

            def tampilkan_maintenance_dari_api(self, machine_id):
                """Fungsi yang dipanggil saat kartu diklik."""
                
                print(f"Mengambil data maintenance untuk machine_id: {machine_id}...")
                
                try:
                    response = requests.get(f"{self.API_MAINTENANCE_URL}/{machine_id}", timeout=5)
                    
                    if response.status_code == 200:
                        list_task = response.json()
                        
                        nama_mesin = "Mesin"
                        for m in self.data_mesin_statis:
                            if m["machine_id"] == machine_id:
                                nama_mesin = m["nama"]
                                break
                        
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
                    error_dialog = MaintenanceDialog(
                        "Error Koneksi", 
                        [{"task_name": "Tidak dapat terhubung ke API.\nPastikan backend .NET Anda sedang berjalan."}], 
                        self
                    )
                    error_dialog.exec()
                except Exception as e:
                    error_dialog = MaintenanceDialog(
                        "Error", 
                        [{"task_name": f"Terjadi kesalahan:\n{e}"}], 
                        self
                    )
                    error_dialog.exec()


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
                # Di sini Anda bisa memanggil API detail dan membuka pop-up
                # (Sama seperti di DashboardPage)

            def clear_layout(self, layout):
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            def load_machines(self):
                """Mengambil data dari GET /api/Machines dan menampilkannya."""
                self.clear_layout(self.scroll_layout)
                
                API_URL = DashboardPage.API_MACHINE_URL 
                
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
                self.clear_layout(self.scroll_layout)
                error_label = QLabel(message)
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(error_label)


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
                
                API_URL = DashboardPage.API_MAINTENANCE_URL 
                
                try:
                    response = requests.get(API_URL, timeout=5)
                    if response.status_code != 200:
                        raise Exception(f"Gagal memuat: Status {response.status_code}")
                    
                    flat_history_list = response.json()
                    
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
                        
                        header_text = f"{item.get('last_date', 'N/A')} — {item.get('machine', 'N/A')}"
                        header_label = QLabel(header_text)
                        header_font = QFont("Roboto", 16)
                        header_font.setBold(True)
                        header_label.setFont(header_font)
                        header_label.setStyleSheet("color: #003366; background-color: transparent;")
                        
                        detail_text = f"Tugas: {item.get('task_name', 'N/A')} (Penanggung Jawab: {item.get('person_in_charge', 'N/A')})"
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

        
        # =======================================================
        # 3. (GANTI) DEFINISI KELAS HALAMAN INVENTORY
        # =======================================================
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
                    # Coba format dengan milidetik
                    dt = QDateTime.fromString(timestamp_str, Qt.DateFormat.ISODateWithMs)
                    if not dt.isValid():
                         # Coba format tanpa milidetik (jika '...Z' saja)
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
                
                API_URL = DashboardPage.API_INVENTORY_URL # Ambil URL dari DashboardPage
                
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
                        
                        # --- DISESUAIKAN DENGAN FORMAT JSON ANDA ---
                        
                        timestamp = self.format_timestamp(log.get('timestamp', 'N/A'))
                        quantity = log.get('quantityChange', 0)
                        
                        if quantity > 0:
                            header_color = "color: #006400;" # Hijau
                            tx_text = f"MASUK (+{quantity})"
                        else:
                            header_color = "color: #8B0000;" # Merah
                            tx_text = f"KELUAR ({quantity})"
                        
                        tx_type = log.get('transactionType', 'N/A')

                        header_text = f"{timestamp} — {tx_text} (Tipe: {tx_type})"
                        header_label = QLabel(header_text)
                        header_font = QFont("Roboto", 14) 
                        header_font.setBold(True)
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
                        # ----------------------------------------------

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
        
        
        # =======================================================
        # 4. DEFINISI KELAS JENDELA UTAMA (MAINWINDOW)
        # =======================================================

        class MainWindow(QMainWindow):
            """Kelas Aplikasi Utama yang menampung sidebar dan halaman."""
            
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
                """Membuat frame navigasi di sebelah kiri."""
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
                self.btn_inventory = QPushButton("Inventory") # <-- Tombol Anda
                
                sidebar_layout.addWidget(self.btn_dashboard)
                sidebar_layout.addWidget(self.btn_asset_monitoring)
                sidebar_layout.addWidget(self.btn_history)
                sidebar_layout.addWidget(self.btn_inventory) # <-- Tombol Anda
                
                sidebar_layout.addStretch() 

            def setup_main_content(self):
                """Membuat container untuk menampung semua halaman."""
                self.content_frame = QWidget()
                self.content_frame.setObjectName("contentArea")
                content_layout = QVBoxLayout(self.content_frame)
                content_layout.setContentsMargins(20, 20, 20, 20) 
                self.stacked_widget = QStackedWidget()
                content_layout.addWidget(self.stacked_widget)

                self.dashboard_page = DashboardPage()
                self.asset_page = AssetMonitoringPage()
                self.history_page = MaintenanceHistoryPage()
                self.inventory_page = InventoryPage() # <-- Halaman baru Anda

                self.stacked_widget.addWidget(self.dashboard_page)
                self.stacked_widget.addWidget(self.asset_page)
                self.stacked_widget.addWidget(self.history_page)
                self.stacked_widget.addWidget(self.inventory_page) # <-- Halaman baru Anda

                self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))
                self.btn_asset_monitoring.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.asset_page))
                self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.history_page))
                self.btn_inventory.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.inventory_page)) # <-- Halaman baru Anda
                
                self.stacked_widget.setCurrentWidget(self.dashboard_page)

        # --- CSS Global (QSS) ---
        GLOBAL_STYLESHEET = """
        QWidget#sidebar {
            background-color: #E8E8E8;
        }
        QWidget#sidebar QLabel {
            color: #333333;
            background-color: transparent;
        }
        QWidget#sidebar QPushButton {
            background-color: #D0D0D0;
            color: #222222;
            border: none;
            padding: 12px;
            font-size: 16px;
            font-family: Roboto;
            text-align: left;
            border-radius: 5px;
        }
        QWidget#sidebar QPushButton:hover {
            background-color: #C0C0C0;
        }
        QWidget#sidebar QPushButton:pressed {
            background-color: #B0B0B0;
        }
        QWidget#contentArea {
            background-color: #F4F4F4;
            font-family: Roboto;
        }
        QWidget#contentArea QLabel {
            background-color: transparent;
        }
        QPushButton#machineButton {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 5px;
            font-size: 15px;
        }
        QPushButton#machineButton:hover {
            background-color: #F0F0F0;
        }
        QFrame#historyItemFrame {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 8px;
        }
        QFrame#imageCard {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 8px;
        }
        QFrame#imageCard:hover {
            background-color: #F9F9F9;
            border: 1px solid #C0C0C0;
        }
        QFrame#textCard {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 8px;
        }
        QFrame#textCard:hover {
            background-color: #F9F9F9;
            border: 1px solid #C0C0C0;
        }
        QScrollArea {
            border: none;
            background-color: #F4F4F4;
        }
        /* Konten di dalam area scroll */
        QWidget#scrollAreaWidgetContents {
            background-color: #F4F4F4; 
        }
        QWidget {
            background-color: transparent;
            color: #333;
        }
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