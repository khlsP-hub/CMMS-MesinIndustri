// File: Models/Machine.cs
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.Collections.Generic;
using System.Linq;
// 1. TAMBAHKAN using ini
using System.Text.Json.Serialization;

namespace APIIndustry.Models;

public class Machine
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    [JsonPropertyName("_id")] // 2. Tambahkan ini
    public string Id { get; set; } = string.Empty;

    [BsonElement("machine")]
    [JsonPropertyName("machine")] // 3. Tambahkan ini
    public string machine { get; set; } = string.Empty;

    [BsonElement("machine_id")]
    [JsonPropertyName("machine_id")] // 4. Tambahkan ini
    public string machine_id { get; set; } = string.Empty;

    [BsonElement("components")]
    [JsonPropertyName("components")] // 5. Tambahkan ini
    public List<Component> Components { get; set; } = new();

    [BsonElement("overallHealth")]
    [JsonPropertyName("overallHealth")] // 6. Tambahkan ini
    public int OverallHealth
    {
        get
        {
            if (Components == null || !Components.Any())
            {
                return 100;
            }
            return (int)Components.Average(c => c.Health);
        }
    }
}