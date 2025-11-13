// File: Models/ScheduleTaskDto.cs
// (Buat file baru ini)

using System.Text.Json.Serialization;
using System;

namespace APIIndustry.Models
{
    // Ini adalah DTO (Data Transfer Object)
    // Gunanya untuk menangkap data JSON dari form Python
    public class ScheduleTaskDto
    {
        [JsonPropertyName("machineId")]
        public string MachineId { get; set; } = string.Empty;

        [JsonPropertyName("componentName")]
        public string ComponentName { get; set; } = string.Empty;

        [JsonPropertyName("taskName")]
        public string TaskName { get; set; } = string.Empty;

        [JsonPropertyName("personInCharge")]
        public string PersonInCharge { get; set; } = string.Empty;

        [JsonPropertyName("scheduledDate")]
        public string ScheduledDate { get; set; } = string.Empty;
    }
}