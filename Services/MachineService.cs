using APIIndustry.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;

namespace APIIndustry.Services
{
    public class MachineService
    {
        private readonly IMongoCollection<Machine> _machines;

        public MachineService(IOptions<MongoDbSettings> mongoSettings)
        {
            var client = new MongoClient(mongoSettings.Value.ConnectionString);
            var database = client.GetDatabase(mongoSettings.Value.DatabaseName);
            _machines = database.GetCollection<Machine>("machines");
        }

        public async Task<List<Machine>> GetAllAsync() =>
            await _machines.Find(_ => true).ToListAsync();

        public async Task<Machine?> GetByIdAsync(string id) =>
            await _machines.Find(m => m.Id == id).FirstOrDefaultAsync();

        public async Task CreateAsync(Machine newMachine) =>
            await _machines.InsertOneAsync(newMachine);

        public async Task UpdateAsync(string id, Machine updated) =>
            await _machines.ReplaceOneAsync(m => m.Id == id, updated);

        public async Task DeleteAsync(string id) =>
            await _machines.DeleteOneAsync(m => m.Id == id);

        public async Task<Component?> GetComponentByNameAsync(string machineId, string componentName)
        {
            var machine = await GetByIdAsync(machineId);
            return machine?.Components.FirstOrDefault(c => c.ComponentName == componentName);
        }

        public async Task<MaintenanceTask?> GetTaskByNameAsync(string machineId, string componentName, string taskName)
        {
            var comp = await GetComponentByNameAsync(machineId, componentName);
            return comp?.MaintenanceTasks.FirstOrDefault(t => t.TaskName == taskName);
        }
    }

    public class MongoDbSettings
    {
        public string ConnectionString { get; set; } = string.Empty;
        public string DatabaseName { get; set; } = string.Empty;
    }
}