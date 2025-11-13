// File: Models/Component.cs
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;
// 1. TAMBAHKAN using ini
using System.Text.Json.Serialization;

namespace APIIndustry.Models;

public class Component
{
    [BsonElement("component_name")]
    [JsonPropertyName("component_name")] // 2. Tambahkan ini
    public string ComponentName { get; set; } = string.Empty;

    [BsonElement("health")]
    [JsonPropertyName("health")] // 3. Tambahkan ini
    public int Health { get; set; } = 100; 

    [BsonElement("last_service_date")]
    [JsonPropertyName("last_service_date")] // 4. Tambahkan ini
    public DateTime LastServiceDate { get; set; } = DateTime.UtcNow;

    [BsonElement("maintenance_tasks")]
    [JsonPropertyName("maintenance_tasks")] // 5. Tambahkan ini
    public List<MaintenanceTask> MaintenanceTasks { get; set; } = new();
}