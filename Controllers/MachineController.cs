using APIIndustry.Models;
using APIIndustry.Services;
using Microsoft.AspNetCore.Mvc;

namespace APIIndustry.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class MachinesController : ControllerBase
    {
        private readonly MachineService _machineService;

        public MachinesController(MachineService service)
        {
            _machineService = service;
        }

        [HttpGet]
        public async Task<ActionResult<List<Machine>>> GetAll() =>
            Ok(await _machineService.GetAllAsync());

        [HttpGet("{id}")]
        public async Task<ActionResult<Machine>> GetById(string id)
        {
            var machine = await _machineService.GetByIdAsync(id);
            if (machine is null) return NotFound();
            return Ok(machine);
        }

        [HttpPost]
        public async Task<ActionResult> Create(Machine newMachine)
        {
            await _machineService.CreateAsync(newMachine);
            return CreatedAtAction(nameof(GetById), new { id = newMachine.Id }, newMachine);
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> Update(string id, Machine updated)
        {
            var machine = await _machineService.GetByIdAsync(id);
            if (machine is null) return NotFound();

            updated.Id = machine.Id;
            await _machineService.UpdateAsync(id, updated);
            return NoContent();
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(string id)
        {
            var machine = await _machineService.GetByIdAsync(id);
            if (machine is null) return NotFound();

            await _machineService.DeleteAsync(id);
            return NoContent();
        }

        [HttpGet("{id}/components/{componentName}")]
        public async Task<ActionResult<Component>> GetComponent(string id, string componentName)
        {
            var comp = await _machineService.GetComponentByNameAsync(id, componentName);
            if (comp is null) return NotFound();
            return Ok(comp);
        }

        [HttpGet("{id}/components/{componentName}/tasks/{taskName}")]
        public async Task<ActionResult<MaintenanceTask>> GetTask(string id, string componentName, string taskName)
        {
            var task = await _machineService.GetTaskByNameAsync(id, componentName, taskName);
            if (task is null) return NotFound();
            return Ok(task);
        }
    }
}
