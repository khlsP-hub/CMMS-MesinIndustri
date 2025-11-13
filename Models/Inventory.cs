// File: Models/Inventory.cs (Ganti file lama Anda dengan ini)

using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.Text.Json.Serialization; // <-- 1. TAMBAHKAN using ini

namespace APIIndustry.Models;

public class Inventory
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    [JsonPropertyName("_id")] // (Opsional, tapi konsisten)
    public string Id { get; set; } = string.Empty;

    [BsonElement("ID_Log")]
    [JsonPropertyName("ID_Log")] // <-- 2. TAMBAHKAN Atribut ini
    public string ID_Log { get; set; } = string.Empty;

    [BsonElement("ID_Items")]
    [JsonPropertyName("ID_Items")] // <-- 3. TAMBAHKAN Atribut ini
    public string ID_Items { get; set; } = string.Empty;

    [BsonElement("ID_Karyawan")]
    [JsonPropertyName("ID_Karyawan")] // <-- 4. TAMBAHKAN Atribut ini
    public string ID_Karyawan { get; set; } = string.Empty;

    [BsonElement("Transaction_Type")]
    [JsonPropertyName("Transaction_Type")] // <-- 5. PERBAIKAN UTAMA
    public string TransactionType { get; set; } = string.Empty; 

    [BsonElement("Quantity_Change")]
    [JsonPropertyName("Quantity_Change")] // <-- 6. PERBAIKAN UTAMA
    public int QuantityChange { get; set; }

    [BsonElement("Timestamp")]
    [JsonPropertyName("Timestamp")] // <-- 7. TAMBAHKAN Atribut ini
    public DateTime Timestamp { get; set; }

    [BsonElement("Reference_Doc")]
    [JsonPropertyName("Reference_Doc")] // <-- 8. PERBAIKAN UTAMA
    public string ReferenceDoc { get; set; } = string.Empty;
}