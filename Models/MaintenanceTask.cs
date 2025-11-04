using MongoDB.Bson.Serialization.Attributes;

namespace APIIndustry.Models;
//terkhalis kalis
public class MaintenanceTask
{
    [BsonElement("task_name")]
    public string task_name { get; set; } = null!;

    [BsonElement("last_date")]
    public string last_date { get; set; } = null!;

    [BsonElement("person_in_charge")]
    public string person_in_charge { get; set; } = null!;

    [BsonElement("maintenance_count")]
    public int maintenance_count { get; set; }
}