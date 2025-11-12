using APIIndustry.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;

namespace APIIndustry.Services;

public class InventoryLogService
{
    private readonly IMongoCollection<Inventory> _logs;

    public InventoryLogService(IOptions<MongoDbSettings> mongoSettings)
    {
        var client = new MongoClient(mongoSettings.Value.ConnectionString);
        var database = client.GetDatabase(mongoSettings.Value.DatabaseName);
        _logs = database.GetCollection<Inventory>("inventory_manager");
    }

    public async Task<List<Inventory>> GetAllAsync() =>
        await _logs.Find(_ => true).ToListAsync();

    public async Task<Inventory?> GetByIdAsync(string id) =>
        await _logs.Find(l => l.Id == id).FirstOrDefaultAsync();

    public async Task CreateAsync(Inventory newLog) =>
        await _logs.InsertOneAsync(newLog);

    public async Task UpdateAsync(string id, Inventory updatedLog) =>
        await _logs.ReplaceOneAsync(l => l.Id == id, updatedLog);

    public async Task DeleteAsync(string id) =>
        await _logs.DeleteOneAsync(l => l.Id == id);

    // Extra filters
    public async Task<List<Inventory>> GetByItemAsync(string itemId) =>
        await _logs.Find(l => l.ID_Items == itemId).ToListAsync();

    public async Task<List<Inventory>> GetByKaryawanAsync(string karyawanId) =>
        await _logs.Find(l => l.ID_Karyawan == karyawanId).ToListAsync();

    public async Task<List<Inventory>> GetByTypeAsync(string type) =>
        await _logs.Find(l => l.TransactionType == type).ToListAsync();
}