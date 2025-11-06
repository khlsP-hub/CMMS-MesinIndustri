// Di file: Services/ProductionLineService.cs
using APIIndustry.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace APIIndustry.Services
{
    public class ProductionLineService
    {
        private readonly IMongoCollection<ProductionLine> _lineCollection;

        public ProductionLineService(IOptions<MongoDbSettings> mongoSettings)
        {
            var client = new MongoClient(mongoSettings.Value.ConnectionString);
            var database = client.GetDatabase(mongoSettings.Value.DatabaseName);

            // GANTI NAMA KOLEKSI DI SINI:
            _lineCollection = database.GetCollection<ProductionLine>("production_line");
        }
        
        public async Task UpdateAsync(int lineId, ProductionLine updatedLine)
{
    var existingLine = await _lineCollection.Find(line => line.Line_ID == lineId).FirstOrDefaultAsync();

    if (existingLine != null)
    {

        updatedLine.Id = existingLine.Id;

        await _lineCollection.ReplaceOneAsync(line => line.Line_ID == lineId, updatedLine);
    }
}

        // Untuk GET /api/ProductionLine
        public async Task<List<ProductionLine>> GetAllAsync() =>
            await _lineCollection.Find(_ => true).ToListAsync();

        // Untuk GET /api/ProductionLine/1 (berdasarkan Line_ID)
        public async Task<ProductionLine?> GetByLineIdAsync(int lineId) =>
            await _lineCollection.Find(line => line.Line_ID == lineId).FirstOrDefaultAsync();
    }
}