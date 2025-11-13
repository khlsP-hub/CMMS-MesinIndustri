// File: Models/MaintenanceTask.cs
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;
// 1. TAMBAHKAN using ini
using System.Text.Json.Serialization;

namespace APIIndustry.Models;

public class MaintenanceTask
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    [JsonPropertyName("id")] // 2. Tambahkan ini
    public string Id { get; set; } = ObjectId.GenerateNewId().ToString();

    [BsonElement("task_name")]
    [JsonPropertyName("task_name")] // 3. Tambahkan ini
    public string task_name { get; set; } = null!;

    [BsonElement("last_date")]
    [BsonIgnoreIfNull]
    [JsonPropertyName("last_date")] // 4. Tambahkan ini
    public string? last_date { get; set; }

    [BsonElement("completed_date")]
    [BsonIgnoreIfNull]
    [JsonPropertyName("completed_date")] // 5. Tambahkan ini
    public string? completed_date { get; set; }

    [BsonElement("scheduled_date")]
    [BsonIgnoreIfNull]
    [JsonPropertyName("scheduled_date")] // 6. Tambahkan ini
    public string? scheduled_date { get; set; }

    [BsonElement("person_in_charge")]
    [JsonPropertyName("person_in_charge")] // 7. Tambahkan ini
    public string person_in_charge { get; set; } = null!;

    [BsonElement("maintenance_count")]
    [JsonPropertyName("maintenance_count")] // 8. Tambahkan ini
    public int maintenance_count { get; set; }

    [BsonElement("status")]
    [BsonIgnoreIfNull] 
    [JsonPropertyName("status")] // 9. Tambahkan ini
    public string? Status { get; set; } = "Scheduled";
}