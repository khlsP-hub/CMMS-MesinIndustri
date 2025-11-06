using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;
using System.Collections.Generic;

namespace APIIndustry.Models;

public class ProductionLine
{
    [BsonId] // Ini untuk _id
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; } = string.Empty;

        [BsonElement("Line_ID")] // Ini untuk Line_ID: 1
        public int Line_ID { get; set; }

        [BsonElement("Mesin")]
        // C# akan membaca object "Mesin" Anda sebagai Dictionary
        public Dictionary<string, MachineStatus> Mesin { get; set; } = new();

        [BsonElement("Updated_At")]
        public DateTime Updated_At { get; set; }
}

public class MachineStatus
{
    [BsonElement("Status")]
    public string Status { get; set; } = string.Empty;

    [BsonElement("IsRunning")]
    public bool IsRunning { get; set; }

    [BsonElement("Last_Updated")]
    public DateTime LastUpdated { get; set; }
}