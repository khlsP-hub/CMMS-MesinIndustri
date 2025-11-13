// File: Controllers/MaintenanceController.cs
using APIIndustry.Models;
using APIIndustry.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks; 
using System.Collections.Generic; 

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

        // GET: /api/Maintenance (Untuk halaman riwayat)
        [HttpGet]
        public async Task<List<MaintenanceTaskResult>> Get()
        {
            return await _machineService.GetAllMaintenanceTasksAsync();
        }

        // GET /api/Maintenance/{id} (Untuk pop-up dashboard)
        [HttpGet("{id}")]
        public async Task<ActionResult<List<MaintenanceTaskResult>>> GetByMachineId(string id)
        {
            var tasks = await _machineService.GetMaintenanceTasksForMachineAsync(id);
            return Ok(tasks);
        }

        // POST: /api/Maintenance/schedule (Untuk form)
        [HttpPost("schedule")]
        public async Task<IActionResult> ScheduleTask([FromBody] ScheduleTaskDto taskDto)
        {
            if (taskDto == null)
            {
                return BadRequest("Data tugas tidak valid.");
            }
            try
            {
                var success = await _machineService.ScheduleTaskAsync(taskDto);
                if (!success)
                {
                    return NotFound($"Gagal menjadwalkan: Mesin ID '{taskDto.MachineId}' atau Komponen '{taskDto.ComponentName}' tidak ditemukan.");
                }
                return Ok(new { message = "Maintenance berhasil dijadwalkan." });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
        
        // PUT: /api/Maintenance/complete
        [HttpPut("complete")]
        public async Task<IActionResult> CompleteTask(
            [FromQuery] string machineId, 
            [FromQuery] string componentName, 
            [FromQuery] string taskId)
        {
            if (string.IsNullOrEmpty(machineId) || string.IsNullOrEmpty(componentName) || string.IsNullOrEmpty(taskId))
            {
                return BadRequest("Parameter machineId, componentName, dan taskId diperlukan.");
            }

            try
            {
                var success = await _machineService.CompleteTaskAsync(machineId, componentName, taskId);
                if (!success)
                {
                    return NotFound("Gagal menyelesaikan: Tugas, mesin, atau komponen tidak ditemukan.");
                }
                return Ok(new { message = "Tugas berhasil diselesaikan dan status mesin diperbarui." });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}