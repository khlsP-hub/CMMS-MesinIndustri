// Di file: Models/MaintenanceTaskResult.cs
namespace APIIndustry.Models
{
    // Ini BUKAN koleksi. Ini HANYA class untuk menampung hasil API.
    public class MaintenanceTaskResult
    {
        public string machine { get; set; } = string.Empty;
        public string component_name { get; set; } = string.Empty;

        // Data dari MaintenanceTask.cs Anda
        public string task_name { get; set; } = null!;
        public string last_date { get; set; } = null!;
        public string person_in_charge { get; set; } = null!;
        public int maintenance_count { get; set; }
    }
}