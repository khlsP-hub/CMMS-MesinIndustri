// File: Models/Component.cs
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;

namespace APIIndustry.Models;

public class Component
{
    [BsonElement("component_name")]
    public string ComponentName { get; set; } = string.Empty;

    // (BARU) Tambahkan status health untuk komponen
    [BsonElement("health")]
    public int Health { get; set; } = 100; // Asumsi 100% saat baru

    // (BARU) Tambahkan kapan terakhir diservis
    [BsonElement("last_service_date")]
    public DateTime LastServiceDate { get; set; } = DateTime.UtcNow;

    [BsonElement("maintenance_tasks")]
    public List<MaintenanceTask> MaintenanceTasks { get; set; } = new();
}