using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace APIIndustry.Models;

public class Inventory
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = string.Empty;

    [BsonElement("ID_Log")]
    public string ID_Log { get; set; } = string.Empty;

    [BsonElement("ID_Items")]
    public string ID_Items { get; set; } = string.Empty;

    [BsonElement("ID_Karyawan")]
    public string ID_Karyawan { get; set; } = string.Empty;

    [BsonElement("Transaction_Type")]
    public string TransactionType { get; set; } = string.Empty; // e.g., "IN" or "OUT"

    [BsonElement("Quantity_Change")]
    public int QuantityChange { get; set; }

    [BsonElement("Timestamp")]
    public DateTime Timestamp { get; set; }

    [BsonElement("Reference_Doc")]
    public string ReferenceDoc { get; set; } = string.Empty;
}