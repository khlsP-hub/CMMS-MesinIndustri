// File: Models/MaintenanceTask.cs
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;

namespace APIIndustry.Models;

public class MaintenanceTask
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = ObjectId.GenerateNewId().ToString();

    [BsonElement("task_name")]
    public string task_name { get; set; } = null!;

    // (PERBAIKAN) Ini untuk membaca data LAMA dari database
    [BsonElement("last_date")]
    [BsonIgnoreIfNull] // Abaikan jika null
    public string? last_date { get; set; }

    // (FITUR BARU) Ini untuk data BARU
    [BsonElement("completed_date")]
    [BsonIgnoreIfNull] // Abaikan jika null
    public string? completed_date { get; set; }

    [BsonElement("scheduled_date")]
    [BsonIgnoreIfNull]
    public string? scheduled_date { get; set; }

    [BsonElement("person_in_charge")]
    public string person_in_charge { get; set; } = null!;

    [BsonElement("maintenance_count")]
    public int maintenance_count { get; set; }

    // (PERBAIKAN) Dibuat nullable agar data lama tidak crash
    [BsonElement("status")]
    [BsonIgnoreIfNull] 
    public string? Status { get; set; } = "Scheduled";
}