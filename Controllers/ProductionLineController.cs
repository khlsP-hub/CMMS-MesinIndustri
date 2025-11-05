// Di file: Controllers/ProductionLineController.cs
using APIIndustry.Models;
using APIIndustry.Services;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace APIIndustry.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProductionLineController : ControllerBase
    {
        private readonly ProductionLineService _lineService;

        public ProductionLineController(ProductionLineService lineService)
        {
            _lineService = lineService;
        }

        [HttpPut("{id:int}")]
        public async Task<IActionResult> Update(int id, ProductionLine updatedLine)
        {
            var existingLine = await _lineService.GetByLineIdAsync(id);
            if (existingLine is null)
            {
                return NotFound();
            }

            await _lineService.UpdateAsync(id, updatedLine);
            return NoContent();
        }

        // GET: /api/ProductionLine
        [HttpGet]
        public async Task<List<ProductionLine>> Get() =>
            await _lineService.GetAllAsync();

        // GET: /api/ProductionLine/1 (berdasarkan Line_ID: 1)
        [HttpGet("{id:int}")]
        public async Task<ActionResult<ProductionLine>> Get(int id)
        {
            var line = await _lineService.GetByLineIdAsync(id);

            if (line is null)
            {
                return NotFound();
            }

            return line;
        }
    }
}