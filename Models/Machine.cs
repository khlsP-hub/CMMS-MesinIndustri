using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

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
}