import customtkinter
import requests
import sys

# --- Halaman 1: Dashboard (Placeholder) ---
class DashboardFrame(customtkinter.CTkFrame):
    """Halaman placeholder untuk Dashboard Utama."""
    def __init__(self, master):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(self, text="Halaman Dashboard", font=("Roboto", 24))
        self.label.pack(pady=20, padx=20)

# --- Halaman 2: Asset Monitoring ---
class AssetMonitoringFrame(customtkinter.CTkFrame):
    """Menampilkan daftar semua mesin dari API."""
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Daftar Mesin")
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_machines()

    def on_machine_click(self, machine_id, machine_name):
        """Dipanggil saat tombol mesin di daftar diklik."""
        print(f"Tombol diklik! ID: {machine_id}, Nama: {machine_name}")
        # NANTI: Kita akan buat ini pindah ke halaman detail mesin
        
    def load_machines(self):
        """Mengambil data dari GET /api/Machines dan menampilkannya."""
        API_URL = "http://localhost:5042/api/Machines" 
        
        try:
            response = requests.get(API_URL) 
            
            if response.status_code == 200:
                machines_data = response.json()
                
                if not machines_data:
                    info_label = customtkinter.CTkLabel(self.scrollable_frame, 
                                                         text="Database terhubung.\nBelum ada data mesin untuk ditampilkan.",
                                                         font=("Roboto", 16))
                    info_label.pack(pady=20, padx=20)
                    return

                for machine in machines_data:
                    machine_id = machine.get("id", "NO_ID")
                    machine_name = machine.get("machineName", "Nama Tidak Ditemukan")
                    
                    machine_button = customtkinter.CTkButton(
                        self.scrollable_frame, 
                        text=machine_name,
                        font=("Roboto", 16),
                        anchor="w"
                    )
                    machine_button.configure(
                        command=lambda id=machine_id, name=machine_name: self.on_machine_click(id, name)
                    )
                    machine_button.pack(fill="x", padx=10, pady=5)
                    
            else:
                self.show_error(f"Gagal memuat: Status {response.status_code}")

        except requests.exceptions.ConnectionError as e:
            self.show_error(f"Error Koneksi:\n{e}\n\nPastikan Windows Firewall mengizinkan python.exe.")
        except Exception as e:
            self.show_error(f"Terjadi error: {e}")

    def show_error(self, message):
        """Helper untuk menampilkan pesan error di frame."""
        error_label = customtkinter.CTkLabel(self.scrollable_frame, text=message, text_color="red")
        error_label.pack(pady=10, padx=10)

# --- Halaman 3: Maintenance History ---
class MaintenanceHistoryFrame(customtkinter.CTkFrame):
    """Menampilkan semua riwayat task dari semua mesin."""
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Riwayat Maintenance (Semua Mesin)")
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.load_history()

    def load_history(self):
        """Mengambil data API, meratakannya, dan menampilkannya."""
        API_URL = "http://localhost:5042/api/Machines"
        
        try:
            response = requests.get(API_URL)
            if response.status_code != 200:
                raise Exception(f"Gagal memuat: Status {response.status_code}")
            
            all_machines = response.json()
            
            # "Meratakan" data dari struktur JSON bersarang
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
                info_label = customtkinter.CTkLabel(self.scrollable_frame, 
                                                     text="Tidak ada riwayat maintenance untuk ditampilkan.")
                info_label.pack(pady=20, padx=20)
                return

            # Tampilkan data yang sudah "rata"
            for item in flat_history_list:
                item_frame = customtkinter.CTkFrame(self.scrollable_frame, fg_color="transparent")
                item_frame.pack(fill="x", padx=5, pady=4)
                
                header_text = f"{item['date']} — {item['machine']}"
                header_label = customtkinter.CTkLabel(item_frame, text=header_text, font=("Roboto", 16, "bold"), anchor="w")
                header_label.pack(fill="x")
                
                detail_text = f"Tugas: {item['task']} (Penanggung Jawab: {item['person']})"
                detail_label = customtkinter.CTkLabel(item_frame, text=detail_text, font=("Roboto", 14), anchor="w")
                detail_label.pack(fill="x")

        except requests.exceptions.ConnectionError as e:
            self.show_error(f"Error Koneksi: {e}")
        except Exception as e:
            self.show_error(f"Terjadi error: {e}")

    def show_error(self, message):
        """Helper untuk menampilkan pesan error di frame."""
        error_label = customtkinter.CTkLabel(self.scrollable_frame, text=message, text_color="red")
        error_label.pack(pady=10, padx=10)


# --- Aplikasi Utama ---
class App(customtkinter.CTk):
    """Kelas Aplikasi Utama yang menampung sidebar dan halaman."""
    
    def __init__(self):
        super().__init__()

        self.title("CMMS Dashboard - Mesin Industri")
        self.geometry("1100x720")
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_content_frame()

        # Tampilkan halaman pertama
        self.select_frame_by_name("dashboard")

    def setup_sidebar(self):
        """Membuat frame navigasi di sebelah kiri."""
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) 

        self.sidebar_label = customtkinter.CTkLabel(self.sidebar_frame, text="CMMS Menu", font=("Roboto", 20))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=20)

        self.btn_dashboard = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.select_frame_by_name("dashboard"))
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_asset_monitoring = customtkinter.CTkButton(self.sidebar_frame, text="Asset Monitoring", command=lambda: self.select_frame_by_name("asset_monitoring"))
        self.btn_asset_monitoring.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_history = customtkinter.CTkButton(self.sidebar_frame, text="Maintenance History", command=lambda: self.select_frame_by_name("maintenance_history"))
        self.btn_history.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    def setup_main_content_frame(self):
        """Membuat container untuk menampung semua halaman."""
        self.main_content_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Loop untuk membuat instance dari setiap halaman
        for F in (DashboardFrame, AssetMonitoringFrame, MaintenanceHistoryFrame):
            frame_name = F.__name__.lower().replace("frame", "")
            frame = F(master=self.main_content_frame)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

    def select_frame_by_name(self, name):
        """Mengangkat frame yang dipilih ke depan."""
        # Sesuaikan nama
        if name == "asset_monitoring": name = "assetmonitoring"
        if name == "maintenance_history": name = "maintenancehistory"
        
        frame_to_show = self.frames[name]
        frame_to_show.tkraise()

# --- Titik Masuk Aplikasi ---
if __name__ == "__main__":
    app = App()
    app.mainloop()

