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
        // Controller ini pakai MachineService
        private readonly MachineService _machineService;

        public MaintenanceController(MachineService machineService)
        {
            _machineService = machineService;
        }

        // GET: /api/Maintenance
        [HttpGet]
        public async Task<List<MaintenanceTaskResult>> Get()
        {
            // Panggil metode baru & kembalikan List<MaintenanceTaskResult>
            return await _machineService.GetAllMaintenanceTasksAsync();
        }
    }
}