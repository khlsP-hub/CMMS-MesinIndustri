using System.Linq;
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
            _machines = database.GetCollection<Machine>("data_mesin");
        }
        //Halo Halis
        public async Task<List<Machine>> GetAllAsync() =>
            await _machines.Find(_ => true).ToListAsync();

        public async Task<Machine?> GetByIdAsync(string id) =>
            await _machines.Find(m => m.machine_id == id).FirstOrDefaultAsync();

        public async Task CreateAsync(Machine newMachine) =>
            await _machines.InsertOneAsync(newMachine);

        public async Task UpdateAsync(string id, Machine updated) =>
            await _machines.ReplaceOneAsync(m => m.machine_id == id, updated);

        public async Task DeleteAsync(string id) =>
            await _machines.DeleteOneAsync(m => m.machine_id == id);

        public async Task<Component?> GetComponentByNameAsync(string machineId, string componentName)
        {
            var machine = await GetByIdAsync(machineId);
            return machine?.Components.FirstOrDefault(c => c.ComponentName == componentName);
        }

        public async Task<MaintenanceTask?> GetTaskByNameAsync(string machineId, string componentName, string taskName)
        {
            var comp = await GetComponentByNameAsync(machineId, componentName);
            return comp?.MaintenanceTasks.FirstOrDefault(t => t.task_name == taskName);
        }
        public async Task<List<MaintenanceTaskResult>> GetAllMaintenanceTasksAsync()
        {
            // Fetch all machines and flatten components and their maintenance tasks in-memory to keep strong typing
            var machines = await _machines.Find(_ => true).ToListAsync();

            var results = machines
                .Where(m => m.Components != null)
                .SelectMany(m => m.Components
                    .Where(c => c.MaintenanceTasks != null)
                    .SelectMany(c => c.MaintenanceTasks.Select(t => new MaintenanceTaskResult
                    {
                        machine = m.machine,
                        component_name = c.ComponentName,
                        task_name = t.task_name,
                        last_date = t.last_date,
                        person_in_charge = t.person_in_charge,
                        maintenance_count = t.maintenance_count
                    })))
                .ToList();

            return results;
        }
        }
    }

    public class MongoDbSettings
    {
        public string ConnectionString { get; set; } = string.Empty;
        public string DatabaseName { get; set; } = string.Empty;
    }