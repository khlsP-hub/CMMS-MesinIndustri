using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace APIMongoDB.Models;

public class Machine
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = string.Empty;

    [BsonElement("machine")]
    public string MachineName { get; set; } = string.Empty;

    [BsonElement("components")]
    public List<Component> Components { get; set; } = new();
}