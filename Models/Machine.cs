// File: Models/Machine.cs
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.Collections.Generic;
using System.Linq;

namespace APIIndustry.Models;

public class Machine
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = string.Empty;

    [BsonElement("machine")]
    public string machine { get; set; } = string.Empty;

    [BsonElement("machine_id")]
    public string machine_id { get; set; } = string.Empty;

    [BsonElement("components")]
    public List<Component> Components { get; set; } = new();

    // (BARU) Properti ini menghitung health rata-rata
    // Properti ini TIDAK disimpan di DB, tapi akan dikirim via API
    [BsonElement("overallHealth")]
    public int OverallHealth
    {
        get
        {
            if (Components == null || !Components.Any())
            {
                return 100; // Jika tidak ada komponen, anggap 100%
            }
            // Hitung rata-rata health dari semua komponen
            return (int)Components.Average(c => c.Health);
        }
    }
}