import sys
import os
import subprocess
import venv  # Modul untuk membuat virtual environment

# --- Bagian 1: Fungsi Setup Environment ---

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def setup_environment():
    """
    Memastikan venv ada dan dependensi terinstal.
    
    Logika:
    1. Cek apakah skrip ini dijalankan dari dalam venv.
    2. JIKA YA: Langsung instal requirements (untuk memastikan) dan kembali (True).
    3. JIKA TIDAK (dijalankan global):
       a. Cek apakah folder 'venv' ada.
       b. JIKA TIDAK ADA: Buat venv baru.
       c. Tentukan path 'pip' yang benar DI DALAM venv.
       d. Instal requirements menggunakan pip dari venv tersebut.
       e. Beri tahu pengguna untuk mengaktifkan venv dan menjalankan skrip lagi.
    """
    
    # 1. Cek apakah kita sudah di dalam venv
    #    'sys.prefix' akan berbeda dari 'sys.base_prefix' jika di dalam venv
    if sys.prefix != sys.base_prefix:
        print("Sudah berada di dalam Virtual Environment.")
        print(f"Memeriksa/menginstal dependensi dari {REQUIREMENTS_FILE}...")
        try:
            # Gunakan sys.executable untuk memastikan pip dari venv yang aktif
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
    
    # 1. Jalankan setup. Fungsi ini mengembalikan True jika siap, False jika tidak.
    apakah_siap_jalan = setup_environment()

    # 2. HANYA JIKA siap (True), baru kita impor dan jalankan aplikasi
    if apakah_siap_jalan:
        
        # --- Bagian 3: Impor Aplikasi (HANYA JIKA SIAP) ---
        print("Setup venv beres. Memulai aplikasi PySide6...")
        
        # Impor ini HARUS ada di dalam 'if' agar tidak error 
        # jika modul belum terinstal
        import requests 
        from PySide6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QScrollArea, QStackedWidget, QFrame
        )
        from PySide6.QtGui import QFont, QIcon
        from PySide6.QtCore import Qt, QSize

        # --- Bagian 4: Definisi Kelas (Kode Aplikasi Anda) ---

        # --- Halaman 1: Dashboard (Placeholder) ---
        class DashboardPage(QWidget):
            """Halaman placeholder untuk Dashboard Utama."""
            def __init__(self):
                super().__init__()
                layout = QVBoxLayout(self)
                
                self.label = QLabel("Halaman Dashboard")
                font = QFont("Roboto", 24)
                font.setBold(True)
                self.label.setFont(font)
                self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                layout.addWidget(self.label)
                self.setLayout(layout)

        # --- Halaman 2: Asset Monitoring ---
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
                # NANTI: Kita akan buat ini pindah ke halaman detail mesin

            def clear_layout(self, layout):
                """Menghapus semua widget dari layout."""
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            def load_machines(self):
                """Mengambil data dari GET /api/Machines dan menampilkannya."""
                self.clear_layout(self.scroll_layout)
                
                API_URL = "http://localhost:5042/api/Machines" 
                
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
                            machine_id = machine.get("id", "NO_ID")
                            machine_name = machine.get("machineName", "Nama Tidak Ditemukan")
                            
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

        # --- Halaman 3: Maintenance History ---
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
                """Menghapus semua widget dari layout."""
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            def load_history(self):
                """Mengambil data API, meratakannya, dan menampilkannya."""
                self.clear_layout(self.scroll_layout)
                
                API_URL = "http://localhost:5042/api/Machines"
                
                try:
                    response = requests.get(API_URL, timeout=5)
                    if response.status_code != 200:
                        raise Exception(f"Gagal memuat: Status {response.status_code}")
                    
                    all_machines = response.json()
                    
                    flat_history_list = []
                    for machine in all_machines:
                        machine_name = machine.get("machineName", "N/A")
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
                        header_label.setStyleSheet("color: #003366;")
                        
                        detail_text = f"Tugas: {item['task']} (Penanggung Jawab: {item['person']})"
                        detail_label = QLabel(detail_text)
                        detail_label.setFont(QFont("Roboto", 14))
                        detail_label.setWordWrap(True)

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
                """Helper untuk menampilkan pesan error di frame."""
                self.clear_layout(self.scroll_layout)
                error_label = QLabel(message)
                error_label.setStyleSheet("color: red;")
                error_label.setFont(QFont("Roboto", 14))
                error_label.setWordWrap(True)
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_layout.addWidget(error_label)

        # --- Aplikasi Utama ---
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

                self.main_layout.addWidget(self.sidebar_frame, 1) # proporsi 1
                self.main_layout.addWidget(self.content_frame, 4) # proporsi 4

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

                sidebar_layout.addWidget(self.btn_dashboard)
                sidebar_layout.addWidget(self.btn_asset_monitoring)
                sidebar_layout.addWidget(self.btn_history)
                
                sidebar_layout.addStretch() # Mendorong semua ke atas

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

                self.stacked_widget.addWidget(self.dashboard_page)
                self.stacked_widget.addWidget(self.asset_page)
                self.stacked_widget.addWidget(self.history_page)

                self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))
                self.btn_asset_monitoring.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.asset_page))
                self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.history_page))

                self.stacked_widget.setCurrentWidget(self.dashboard_page)

        # --- CSS Global (QSS) ---
        GLOBAL_STYLESHEET = """
        QWidget#sidebar {
            background-color: #E8E8E8; /* Warna abu-abu muda untuk sidebar */
        }

        QWidget#sidebar QLabel {
            color: #333333;
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

        /* Area Konten Utama */
        QWidget#contentArea {
            background-color: #F4F4F4; /* Latar belakang utama yang sangat muda */
            font-family: Roboto;
        }

        /* Tombol di dalam daftar mesin */
        QPushButton#machineButton {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 5px;
            font-size: 15px;
        }
        QPushButton#machineButton:hover {
            background-color: #F0F0F0;
        }

        /* Frame untuk item riwayat */
        QFrame#historyItemFrame {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 8px;
        }

        /* Area Scroll */
        QScrollArea {
            border: none;
            background-color: #F4F4F4;
        }

        /* Konten di dalam area scroll */
        QWidget {
            /* Ini adalah pengaturan default untuk semua QWidget.
            Kita set ke #F4F4F4 agar sesuai dengan contentArea.
            QSS spesifik (seperti #sidebar) akan menimpanya.
            */
            background-color: #F4F4F4; 
        }
        """

        # --- Bagian 5: Peluncuran Aplikasi ---
        
        app = QApplication(sys.argv)
        
        # Terapkan stylesheet global
        app.setStyleSheet(GLOBAL_STYLESHEET)
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    else:
        # --- Setup Gagal atau Selesai (Global) ---
        print("\nSkrip berhenti. Silakan ikuti instruksi di atas untuk mengaktifkan venv.")
        sys.exit(0)