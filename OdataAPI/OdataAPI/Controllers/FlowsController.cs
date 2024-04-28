using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.OData.Query;
using Microsoft.AspNetCore.OData.Routing.Controllers;
using OdataAPI.Data;
using OdataAPI.Models;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace OdataAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlowsController : ODataController
    {
        private readonly AlphaAnalyticsDbContext _context;

        public FlowsController(AlphaAnalyticsDbContext context)
        {
            _context = context;
        }

        // GET: api/<FlowsController>
        [EnableQuery]
        [HttpGet]
        public async Task<IQueryable<Flow>> GetAsync()
        {
            return _context.Flows;
        }
    }
}
