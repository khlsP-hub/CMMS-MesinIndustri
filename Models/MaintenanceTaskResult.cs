// File: Models/MaintenanceTaskResult.cs
namespace APIIndustry.Models
{
    // Ini BUKAN koleksi. Ini HANYA class untuk menampung hasil API.
    public class MaintenanceTaskResult
    {
        public string machine { get; set; } = string.Empty;
        public string component_name { get; set; } = string.Empty;

        // (BARU) Tambahkan ini agar Python tahu ID-nya
        public string machine_id { get; set; } = string.Empty;
        public string task_id { get; set; } = string.Empty;
        public string? status { get; set; } // Dibuat nullable

        public string task_name { get; set; } = null!;
        
        // 'last_date' sekarang adalah 'completed_date' (nullable)
        public string? last_date { get; set; } 
        public string? scheduled_date { get; set; } // Dibuat nullable
        
        public string person_in_charge { get; set; } = null!;
        public int maintenance_count { get; set; }
    }
}