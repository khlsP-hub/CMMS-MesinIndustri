// File: Services/MachineService.cs
using System;
using System.Linq;
using APIIndustry.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;
using System.Threading.Tasks;
using System.Collections.Generic;

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
        
        public async Task<List<Machine>> GetAllAsync() =>
            await _machines.Find(_ => true).ToListAsync();
        
        public async Task<List<MaintenanceTaskResult>> GetMaintenanceTasksForMachineAsync(string id)
        {
            var machine = await GetByIdAsync(id);
            if (machine == null || machine.Components == null)
            {
                return new List<MaintenanceTaskResult>(); 
            }
            
            var results = machine.Components
                .Where(c => c.MaintenanceTasks != null)
                .SelectMany(c => c.MaintenanceTasks.Select(t => new MaintenanceTaskResult
                {
                    machine = machine.machine,
                    component_name = c.ComponentName,
                    task_name = t.task_name,
                    
                    // --- (LOGIKA CERDAS) ---
                    last_date = t.completed_date ?? t.last_date, 
                    scheduled_date = t.scheduled_date,
                    status = t.Status ?? (t.last_date != null ? "Completed" : "Scheduled"),
                    // --- (AKHIR LOGIKA CERDAS) ---
                    
                    task_id = t.Id, 
                    person_in_charge = t.person_in_charge,
                    maintenance_count = t.maintenance_count
                }))
                .ToList();
            
            return results;
        }

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
            var machines = await _machines.Find(_ => true).ToListAsync();

            var results = machines
                .Where(m => m.Components != null)
                .SelectMany(m => m.Components
                    .Where(c => c.MaintenanceTasks != null)
                    .SelectMany(c => c.MaintenanceTasks.Select(t => new MaintenanceTaskResult
                    {
                        machine = m.machine,
                        machine_id = m.machine_id, 
                        component_name = c.ComponentName, 
                        task_id = t.Id, 
                        task_name = t.task_name,
                        
                        // --- (LOGIKA CERDAS) ---
                        last_date = t.completed_date ?? t.last_date,
                        scheduled_date = t.scheduled_date,
                        status = t.Status ?? (t.last_date != null ? "Completed" : "Scheduled"),
                        // --- (AKHIR LOGIKA CERDAS) ---

                        person_in_charge = t.person_in_charge,
                        maintenance_count = t.maintenance_count
                    })))
                .ToList();

            return results;
        }

        public async Task<bool> ScheduleTaskAsync(ScheduleTaskDto taskDto)
        {
            var filter = Builders<Machine>.Filter.Eq(m => m.machine_id, taskDto.MachineId);
            var machine = await _machines.Find(filter).FirstOrDefaultAsync();

            if (machine == null) return false; 

            var component = machine.Components.FirstOrDefault(c => c.ComponentName == taskDto.ComponentName);
            if (component == null) return false; 

            var newTask = new MaintenanceTask
            {
                task_name = taskDto.TaskName,
                person_in_charge = taskDto.PersonInCharge,
                scheduled_date = taskDto.ScheduledDate, 
                completed_date = null, // Data baru akan menggunakan 'completed_date'
                last_date = null, // Pastikan data lama null
                Status = "Scheduled", 
                maintenance_count = 1 
            };
            
            // "Rusak" komponen
            if (component.Health > 20)
            {
                component.Health = 20; 
            }

            component.MaintenanceTasks.Add(newTask);
            
            var updateResult = await _machines.ReplaceOneAsync(filter, machine);
            return updateResult.IsAcknowledged && updateResult.ModifiedCount > 0;
        }
        
        public async Task<bool> CompleteTaskAsync(string machineId, string componentName, string taskId)
        {
            var filter = Builders<Machine>.Filter.Eq(m => m.machine_id, machineId);
            var machine = await _machines.Find(filter).FirstOrDefaultAsync();

            if (machine == null) return false;

            var component = machine.Components.FirstOrDefault(c => c.ComponentName == componentName);
            if (component == null) return false;

            var task = component.MaintenanceTasks.FirstOrDefault(t => t.Id == taskId);
            if (task == null) return false;

            // Update status tugas
            task.Status = "Completed";
            task.completed_date = DateTime.UtcNow.ToString("yyyy-MM-dd");
            task.last_date = null; // Hapus data lama

            // Perbarui health komponen
            component.Health = 100; 
            component.LastServiceDate = DateTime.UtcNow;

            var updateResult = await _machines.ReplaceOneAsync(filter, machine);
            return updateResult.IsAcknowledged && updateResult.ModifiedCount > 0;
        }
    }

    public class MongoDbSettings
    {
        public string ConnectionString { get; set; } = string.Empty;
        public string DatabaseName { get; set; } = string.Empty;
    }
}