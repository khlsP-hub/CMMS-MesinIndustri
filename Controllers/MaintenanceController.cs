// Di file: Controllers/MaintenanceController.cs
using APIIndustry.Models;
using APIIndustry.Services;
using Microsoft.AspNetCore.Mvc;

namespace APIIndustry.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class MaintenanceController : ControllerBase
    {
        private readonly MachineService _machineService;

        public MaintenanceController(MachineService machineService)
        {
            _machineService = machineService;
        }

        // Ini endpoint LAMA Anda (GET: /api/Maintenance)
        // (Tetap biarkan untuk halaman Maintenance History)
        [HttpGet]
        public async Task<List<MaintenanceTaskResult>> Get()
        {
            return await _machineService.GetAllMaintenanceTasksAsync();
        }

        // --- TAMBAHKAN ENDPOINT BARU INI ---
        // Ini akan menangani: GET /api/Maintenance/4
        [HttpGet("{id}")]
        public async Task<ActionResult<List<MaintenanceTaskResult>>> GetByMachineId(string id)
        {
            // 1. Panggil fungsi baru di service
            var tasks = await _machineService.GetMaintenanceTasksForMachineAsync(id);
            
            // 2. Kirim hasilnya
            return Ok(tasks);
        }
    }
}