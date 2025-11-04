using MongoDB.Bson.Serialization.Attributes;

namespace APIIndustry.Models;
//terkhalis kalis
public class MaintenanceTask
{
    [BsonElement("task_name")]
    public string TaskName { get; set; } = null!;

    [BsonElement("last_date")]
    public string LastDate { get; set; } = null!;

    [BsonElement("person_in_charge")]
    public string PersonInCharge { get; set; } = null!;

    [BsonElement("maintenance_count")]
    public int MaintenanceCount { get; set; }
}