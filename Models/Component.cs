using MongoDB.Bson.Serialization.Attributes;

namespace APIMongoDB.Models;

public class Component
{
    [BsonElement("component_name")]
    public string ComponentName { get; set; } = string.Empty;

    [BsonElement("maintenance_tasks")]
    public List<MaintenanceTask> MaintenanceTasks { get; set; } = new();
}