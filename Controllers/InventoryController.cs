using APIIndustry.Models;
using APIIndustry.Services;
using Microsoft.AspNetCore.Mvc;

namespace APIIndustry.Controllers;

[ApiController]
[Route("api/[controller]")]
public class InventoryLogsController : ControllerBase
{
    private readonly InventoryLogService _logService;

    public InventoryLogsController(InventoryLogService service)
    {
        _logService = service;
    }

    [HttpGet]
    public async Task<ActionResult<List<Inventory>>> GetAll() =>
        Ok(await _logService.GetAllAsync());

    [HttpGet("{id}")]
    public async Task<ActionResult<Inventory>> GetById(string id)
    {
        var log = await _logService.GetByIdAsync(id);
        if (log is null) return NotFound();
        return Ok(log);
    }

    [HttpPost]
    public async Task<ActionResult> Create(Inventory newLog)
    {
        await _logService.CreateAsync(newLog);
        return CreatedAtAction(nameof(GetById), new { id = newLog.Id }, newLog);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult> Update(string id, Inventory updated)
    {
        var existing = await _logService.GetByIdAsync(id);
        if (existing is null) return NotFound();

        updated.Id = existing.Id;
        await _logService.UpdateAsync(id, updated);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> Delete(string id)
    {
        var log = await _logService.GetByIdAsync(id);
        if (log is null) return NotFound();

        await _logService.DeleteAsync(id);
        return NoContent();
    }

    [HttpGet("item/{itemId}")]
    public async Task<ActionResult<List<Inventory>>> GetByItem(string itemId) =>
        Ok(await _logService.GetByItemAsync(itemId));

    [HttpGet("karyawan/{karyawanId}")]
    public async Task<ActionResult<List<Inventory>>> GetByKaryawan(string karyawanId) =>
        Ok(await _logService.GetByKaryawanAsync(karyawanId));

    [HttpGet("type/{type}")]
    public async Task<ActionResult<List<Inventory>>> GetByType(string type) =>
        Ok(await _logService.GetByTypeAsync(type));
}